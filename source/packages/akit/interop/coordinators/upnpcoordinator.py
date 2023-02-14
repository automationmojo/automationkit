"""
.. module:: upnpcoordinator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the UpnpCoordinator which is used for managing connectivity upnp devices visible in the automation landscape.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Dict, List, Optional, TYPE_CHECKING, Union

import os
import socket
import threading
import traceback
import uuid
import weakref

from http import HTTPStatus
from io import BytesIO, SEEK_END

import netifaces
import yaml

from requests.exceptions import ConnectionError

from akit.environment.variables import AKIT_VARIABLES
from akit.exceptions import AKitConfigurationError, AKitRuntimeError, AKitSemanticError, AKitTimeoutError
from akit.friendlyidentifier import FriendlyIdentifier

from akit.networking.constants import AKitHttpHeaders, HTTP1_1_LINESEP, HTTP1_1_END_OF_HEADER
from akit.networking.interfaces import get_interface_for_ip
from akit.networking.multicast import create_multicast_socket
from akit.networking.resolution import get_arp_table, refresh_arp_table
from akit.networking.trafficcapturecontext import TrafficCaptureContext

from akit.interop import upnp as upnp_module
from akit.interop.landscaping.landscapedevice import LandscapeDevice

from akit.interop.upnp.devices.upnprootdevice import UpnpRootDevice
from akit.interop.upnp.devices.upnprootdevice import device_description_load
from akit.interop.upnp.devices.upnprootdevice import device_description_find_components

from akit.interop.upnp.upnpfactory import UpnpFactory
from akit.interop.upnp.upnpprotocol import msearch_query_host, msearch_scan, notify_parse_request
from akit.interop.upnp.upnpprotocol import MSearchKeys, MSearchRouteKeys, UpnpProtocol
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy
from akit.interop.upnp.xml.upnpdevice1 import UPNP_DEVICE1_NAMESPACE

from akit.interop.coordinators.coordinatorbase import CoordinatorBase

from akit.networking.interfaces import get_ipv4_address

from akit.paths import get_path_for_output

# Types imported only for type checking purposes
if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

EMPTY_LIST = []

UPNP_DIR = os.path.dirname(upnp_module.__file__)

UPNP_SUBSCRIPTION_NOTIFY_RESPONSE_OK = HTTP1_1_LINESEP.join([
    b'HTTP/1.1 200 OK',
    b'Connection: close',
    b'Content-Length: 0',
    b'Content-Type: text/html',
    b'Server: %s,UPnP/1.0' % AKitHttpHeaders.SERVER.encode(),
    b''
])

def http_parse_header(header_content):
    headers = {}
    header_lines = header_content.splitlines(False)

    assert len(header_lines) > 0, "The header content was not a valid HTTP request header."
    req_line = header_lines[0]
    for hline in header_lines[1:]:
        name_end = hline.find(b":")
        if name_end > -1:
            hname = hline[:name_end].upper().decode().strip()
            hval = hline[name_end + 1:].decode().strip()
            headers[hname] = hval
    return req_line, headers


class UpnpCoordinator(CoordinatorBase):
    """
        The UpnpCoordinator utilizes the expected device declarations of type 'network/upnp' to establish and maintain connectivity
        and interoperability with UPNP based network devices.  The UpnpCoordinator will scan all interfaces except for the excluded
        interfaces.  It also creates a general broadcast monitor thread and a subscription dispatch thread for each interface it
        is monitoring.
    """
    # pylint: disable=attribute-defined-outside-init

    UPNP_CACHE_DIR = os.path.join(AKIT_VARIABLES.AKIT_HOME_DIRECTORY, "cache", "upnp")

    def __init__(self, lscape: "Landscape", control_point=None, workers: int = 5):
        super(UpnpCoordinator, self).__init__(lscape, control_point=control_point, workers=workers)

        self._local_udn = uuid.getnode()

        return

    def _initialize(self, *_args, control_point=None, workers: int = 5, **_kwargs):
        """
            Called by the CoordinatorBase constructor to perform the one time initialization of the coordinator Singleton
            of a given type.

            :param control_point: An object that acts as a UPNP control point.
            :param workers: The number of worker threads to spin up for handling work packets.
        """
        # pylint: disable=arguments-differ

        # ============================ Fixed Variables ============================
        # These variables are fixed at the start of the UpnpCoordinator and because
        # they are fixed, we don't protect them with the all.

        self._control_point = control_point
        self._worker_count = workers

        self._factory = UpnpFactory()

        self._running = False
        self._allow_unknown_devices = False
        self._upnp_recording = True

        # The count for the shutdown gate semaphore is set at startup so we don't
        # need to lock protect it.  Once it is set, it is fixed for the lifespan
        # of the UpnpCoordinator
        self._shutdown_gate = None

        # ======================= Coordinator Lock Variables =======================
        # These variables are protected and read/write synchronized by the coordinator
        # lock.  They are all prefixed with _cl_ so it is easy to identify in code
        # if the lock is being held properly when the variables are being accessed.

        # Callback threads are created on a per interface basis so we use a list
        # to manage them.
        self._cl_callback_threads = []

        # We don't want our threads that are answering requests or filtering traffic
        # to do extensive amounts of work, so we have a pool of worker threads that
        # that work is dispatched to for incoming requests and information processing.
        self._cl_worker_threads = []

        # A lookup table from USN -> devinfo for devices that were declared as
        # watched devices, the watched devices are devices that will be monitored
        # under special constraints and the coordinator will ensure they are found
        # during startup and will expend thread resources to ensure they are updated
        self._cl_watched_devices = {}

        self._cl_iface_callback_addr_lookup = None

        # A lookup table that store device registrations for differen subscription id(s)
        # The UpnpCoordinator spins up one thread per interface that needs to be monitored
        # for callback traffic from devices and provides a callback URL for subscriptions
        # to the devices,  the callback threads use this table to dispatch subscription
        # callbacks on given interfaces to the appropriate device. So UpnpEventVar instances
        # can be updated.
        self._cl_subscription_id_to_device = {}

        # A reverse lookup table that can lookup the device hint from its USN
        self._cl_usn_to_hint = {}

        # Callback capture management dictionaries
        self._cl_callback_traffic_capture_from = {}

        # =========================== Queue Lock Variables ==========================
        # Variables that manage the work queue and dispatching of work to worker threads
        self._queue_lock = threading.RLock()
        self._queue_available = threading.Semaphore(0)
        self._queue_work = []

        self._match_table = {
            "modelName": ('upnp', UpnpRootDevice._matches_model_name), # pylint: disable=protected-access
            "modelNumber": ('upnp', UpnpRootDevice._matches_model_number) # pylint: disable=protected-access
        }

        self._excluded_interfaces = ["lo"]

        self._cl_callback_interface_sockets = {}

        return

    @property
    def local_udn(self) -> str:
        """
            Returns a local UDN for this device.
        """
        return self._local_udn

    @property
    def watch_devices(self) -> List[LandscapeDevice]:
        """
            Returns a list of the devices being watched by the UPNP coordinator.
        """
        wlist = []

        self._coord_lock.acquire()
        try:
            wlist = [wd for wd in self._cl_watched_devices.values()]
        finally:
            self._coord_lock.release()

        return wlist

    def create_callback_traffic_capture_context(self, fromip: str):
        
        identifier = uuid.uuid4()
        context = TrafficCaptureContext(self, identifier, fromip, self.destroy_callback_traffic_capture_context)

        self._coord_lock.acquire()
        try:
            if fromip in self._cl_callback_traffic_capture_from:
                self._cl_callback_traffic_capture_from[fromip][context.identifier] = context
            else:
                self._cl_callback_traffic_capture_from[fromip] = {context.identifier: context}
        finally:
            self._coord_lock.release()

        return context

    def destroy_callback_traffic_capture_context(self, context: TrafficCaptureContext):

        fromip = context.fromip
        identifier = context.identifier

        self._coord_lock.acquire()
        try:
            if fromip in self._cl_callback_traffic_capture_from:
                fromip_table = self._cl_callback_traffic_capture_from[fromip]
                if identifier in fromip_table:
                    del fromip_table[identifier]
        finally:
            self._coord_lock.release()

        return

    def establish_presence(self):
        watched_devices = self.watch_devices

        for wdev in watched_devices:
            wdev.upnp.set_auto_subscribe(True, factory=self._factory)

        return

    def lookup_callback_url_for_interface(self, ifname: str) -> str:
        """
            The callback url that is utilized by devices to determine the URL that should be used as a callback
            for a given network interface.

            :param ifname: The interface name of the interface to get the callback url for.

            :returns: Returns the callback url being monintored by the coordinator for a given interface.
        """
        callback_url = None

        self._coord_lock.acquire()
        try:
            if ifname in self._cl_iface_callback_addr_lookup:
                callback_url = "<http://{}/notify>".format(self._cl_iface_callback_addr_lookup[ifname])
        finally:
            self._coord_lock.release()

        return callback_url

    def lookup_device_by_mac(self, mac: str) -> Union[LandscapeDevice, None]:
        """
            Lookup a UPNP device by its MAC address.

            :param mac: The mac address of the device to search for.

            :returns: The device found with the associated MAC address or None
        """

        found = None

        self._coord_lock.acquire()
        try:
            for nxtdev in self._cl_children.values():
                if mac == nxtdev.MACAddress:
                    found = nxtdev.basedevice
                    break
        finally:
            self._coord_lock.release()

        return found

    def lookup_device_by_upnp_hint(self, hint: str) -> Union[UpnpRootDevice, None]:
        """
            Lookup a UPNP device by its hint id.

            :param hint: The hint of the device to search for.

            :returns: The device found with the associated hint address or None
        """

        found = None

        self._coord_lock.acquire()
        try:
            for nxtdev in self._cl_children.values():
                if nxtdev.USN.find(hint) > -1:
                    found = nxtdev
                    break
            
            if found is None:
                errmsg_lines = [
                    "lookup_device_by_upnp_hint did not find a device for hint={}.".format(hint),
                    "DEVICE USN(s):"
                ]
                for nxtdev in self._cl_children.values():
                    errmsg_lines.append(nxtdev.USN)
                errmsg = os.linesep.join(errmsg_lines)
                self._logger.debug(errmsg)

        finally:
            self._coord_lock.release()

        return found
    
    def lookup_device_by_upnp_usn(self, usn: str) -> Union[UpnpRootDevice, None]:
        """
            Lookup a UPNP device by its USN id.

            :param usn: The USN of the device to search for.

            :returns: The device found with the associated USN address or None
        """

        found = None

        self._coord_lock.acquire()
        try:
            for nxtdev in self._cl_children.values():
                if nxtdev.USN.find(usn) > -1:
                    found = nxtdev
                    break
            
            if found is None:
                errmsg_lines = [
                    "lookup_device_by_upnp_usn did not find a device for usn={}.".format(usn),
                    "DEVICE USN(s):"
                ]
                for nxtdev in self._cl_children.values():
                    errmsg_lines.append(nxtdev.USN)
                errmsg = os.linesep.join(errmsg_lines)
                self._logger.debug(errmsg)

        finally:
            self._coord_lock.release()

        return found

    def lookup_device_list_by_usn(self, usnlist: List[str]) -> List[LandscapeDevice]:
        """
            Lookup a list of UPNP devices by thier USN id.

            :param usn: A list of USN identifiers for devices to search for.

            :returns: A list of devices found with USN(s) in the usn search list.
        """
        found = []

        self._coord_lock.acquire()
        try:
            for usn in usnlist:
                for nxtdev in self._cl_children.values():
                    if usn == nxtdev.USN:
                        found.append(nxtdev)
        finally:
            self._coord_lock.release()

        return found

    def lookup_device_instance_for_sid(self, sid: str) -> UpnpServiceProxy:
        """
            Lookup a device instance that has been registered with a subscription id.

            :param sid: The sid of a service device to search for.

            :returns: A device found to be associated with the sid provided.
        """
        device_inst = None

        self._coord_lock.acquire()
        try:
            if sid in self._cl_subscription_id_to_device:
                device_inst = self._cl_subscription_id_to_device[sid]
        finally:
            self._coord_lock.release()

        return device_inst

    def register_subscription_for_device(self, sid: str, device: LandscapeDevice):
        """
            Registers a service instance for event callbacks via a 'sid'.

            :param sid: The service subscription id to register a device with.
            :param device: The device to register as a handler for notifications for the sid provided.
        """

        self._coord_lock.acquire()
        try:
            self._cl_subscription_id_to_device[sid] = device
        finally:
            self._coord_lock.release()

        return

    def startup_scan(self, query_devices: Dict[str, dict], required_devices: Optional[List[str]] = None,
                           watchlist: Optional[List[str]] = None, exclude_interfaces: List = [],
                            response_timeout: float = 20, pre_msearch_timeout=20, retry: int = 2, 
                            upnp_recording: bool = False, allow_unknown_devices: bool = False):
        """
            Starts up and initilizes the UPNP coordinator by utilizing a hint list to determine
            what network interfaces to setup UPNP monitoring on.

            :param query_devices: A list of upnp USN(s) to search for.
            :param required_devices: A list of required USN(s) that we will setup watching and updates for.
            :param exclude_interfaces: Network interfaces that will be excluded from the search for devices.
            :param response_timeout: A timeout to wait for a response.
            :param retry: The number of retry attempts to make before giving up on finding devices.
            :param upnp_recording: Forces the updating or recording of device descriptions from devices found on the network.
        """
        # pylint: disable=dangerous-default-value

        self._allow_unknown_devices = allow_unknown_devices
        self._upnp_recording = upnp_recording
        self._excluded_interfaces = exclude_interfaces

        lscape = self.landscape

        if self._running:
            raise AKitRuntimeError("UpnpCoordinator.startup_scan called twice, The UpnpCoordinator is already running.") from None

        # Because we only allow this method to be called once, We don't need to lock the UpnpCoordinator
        # for most of this activity because the only thread with a reference to use is the caller.  At
        # the end of this function when we startup all the callback and worker threads is when we need to
        # start using the lock.
        if query_devices is None:
            query_devices = []

        interface_list = [ifname for ifname in netifaces.interfaces()]
        for exif in exclude_interfaces:
            if exif in interface_list:
                interface_list.remove(exif)

        found_devices = {}
        matching_devices = {}
        missing_devices = []

        remaining_query_devices = [ usn for usn in query_devices]

        pre_msearch_found = self._device_scan_pre_msearch_query(lscape, remaining_query_devices, pre_msearch_timeout, retry)
        if len(pre_msearch_found) > 0:
            found_devices.update(pre_msearch_found)
            matching_devices.update(pre_msearch_found)
            
            devices_to_remove = []
            for qdev_usn in remaining_query_devices:
                if qdev_usn in found_devices:
                    devices_to_remove.append(qdev_usn)
            
            # Remove the devices that we found and successfully queried from the list of device to query
            for fdev_usn in devices_to_remove:
                remaining_query_devices.remove(fdev_usn)

        # ======================== M-SEARCH ========================
        # We have to first attempt to msearch for the devices because we need the latest
        # device info to create devices with.
        if len(remaining_query_devices) > 0:
            msearch_found, msearch_matching = self._device_msearch_scan(
                remaining_query_devices, interface_list=interface_list,
                response_timeout=response_timeout, retry=retry)

            found_devices.update(msearch_found)
            matching_devices.update(msearch_matching)

            # Remove the devices that we found from the list of device to query for
            for match_hint in msearch_matching:
                if match_hint in remaining_query_devices:
                    remaining_query_devices.remove(match_hint)

        # ====================== UPNP CACHE & DIRECT QUERY ===================
        # If we didn't find a device with an M-SEARCH, look in the UPNP cache
        # and try to query the device directly to get its info.  We only use the
        # cached info to get the IP of the device, we don't use it for other data
        # because some of the data might be out of date.
        if len(remaining_query_devices) > 0:
            # When we look in the cache, the found devices are also the matching devices
            cache_found = self._device_cache_scan(remaining_query_devices)
            found_devices.update(cache_found)
            matching_devices.update(cache_found)

            devices_to_remove = []
            for qdev_usn in remaining_query_devices:
                if qdev_usn in cache_found:
                    cdev_info = cache_found[qdev_usn]
                    cached_ipaddr = cdev_info[MSearchKeys.IP]
                    qdev_info = msearch_query_host(qdev_usn, cached_ipaddr)
                    if qdev_info is not None:
                        found_devices[fdev_usn] = qdev_info
                        devices_to_remove.append(fdev_usn)

            # Remove the devices that we found and successfully queried from the list of device to query
            for fdev_usn in devices_to_remove:
                remaining_query_devices.remove(fdev_usn)

        # ====================== LAST RESULT, TRY USING THE ARP TABLE ===================
        if len(remaining_query_devices) > 0:
            final_found, final_matching = self._device_scan_final_alternatives(remaining_query_devices,
                interface_list=interface_list, response_timeout=response_timeout,
                retry=retry)

        missing_devices = []
        if required_devices is not None:
            for devhint in required_devices:
                if devhint not in matching_devices:
                    missing_devices.append(devhint)

        if len(missing_devices) > 0:
            errmsg_list = [
                "Error devices missing from configuration.",
                "MISSING DEVICES:"
            ]
            for devhint in missing_devices:
                errmsg_list.append("    %s" % devhint)
            errmsg = os.linesep.join(errmsg_list)
            self._logger.error(errmsg)
            raise AKitConfigurationError(errmsg) from None

        config_lookup = lscape._internal_get_upnp_device_config_lookup_table() # pylint: disable=protected-access

        for dhint, dval in matching_devices.items():
            addr = dval[MSearchKeys.IP]
            location = dval[MSearchKeys.LOCATION]
            self._update_root_device(lscape, config_lookup, addr, location, dhint, dval)

        if watchlist is not None and len(watchlist) > 0:
            for hint in watchlist:
                wdev = self.lookup_device_by_upnp_hint(hint)
                self._cl_watched_devices[hint] = wdev.basedevice

        self._log_scan_results(found_devices, matching_devices, missing_devices)

        self._device_cache_update(matching_devices)

        self._start_all_threads()

        self._found_devices = found_devices
        self._available_devices = matching_devices
        self._unavailable_devices = missing_devices

        return found_devices, matching_devices, missing_devices

    def wakeup_device(self, usn, dev_hint):
        self._logger.info("TODO: Implement an overload for UpnpCoordinatorIntegration:wakeup_device.")
        return

    def _create_root_device(self, manufacturer: str, model_number: str, model_description: str) -> UpnpRootDevice:
        """
            Create a root UPNP device using the provided manufacturer and modelNumber provided.  If no
            device is found for the provided manufacturer and model_number then a generic UPNP root device
            will be instantiated using the manufacturer, model_number and model_description.

            :param manufacturer: The manufacturer of the root device to instantiate.
            :param model_number: The model_number of the root device to instantiate.
            :param model_description: The description to give to a device when it is instantiated.

            :returns: A upnp root device instance.
        """
        dev = self._factory.create_root_device_instance(manufacturer, model_number, model_description)
        return dev

    def _device_cache_scan(self, query_devices: list):

        found_devices = {}

        for qdev_hint in query_devices:
            qdev_filename = os.path.join(self.UPNP_CACHE_DIR, qdev_hint)

            if os.path.exists(qdev_filename):
                dev_info = None
                with open(qdev_filename, 'r') as qdf:
                    dicontent = qdf.read()
                    dev_info = yaml.safe_load(dicontent)

                if dev_info is not None:
                    verified = self._device_cache_verify_device_info(qdev_hint, qdev_filename, dev_info)
                    if verified:
                        found_devices[qdev_hint] = dev_info

        return found_devices

    def _device_cache_update(self, found_device: dict):

        if not os.path.exists(self.UPNP_CACHE_DIR):
            os.makedirs(self.UPNP_CACHE_DIR)

        for fdev_usn in found_device:
            fdev_info = found_device[fdev_usn]
            fdev_filename = os.path.join(self.UPNP_CACHE_DIR, fdev_usn)
            with open(fdev_filename, 'w') as dcf:
                yaml.dump(fdev_info, dcf)

        return

    def _device_cache_verify_device_info(self, device_hint: str, device_filename: str, device_info: dict):
        valid = False

        if MSearchKeys.USN_DEV in device_info and "LOCATION" in device_info:
            location_url = device_info["LOCATION"]

            try:
                dev_desc = device_description_load(location_url)
                if dev_desc is not None:
                    namespaces = {"": UPNP_DEVICE1_NAMESPACE}

                    root_element = dev_desc.getroot()
                    udn_element = root_element.find("device/UDN", namespaces=namespaces)
                    if udn_element is not None:
                        udn_full = udn_element.text.lstrip("uuid:")
                        if udn_full.find(device_hint) < 0:
                            os.remove(device_filename)
                        else:
                            valid = True
            except ConnectionError:
                pass
        else:
            os.remove(device_filename)

        return valid

    def _device_msearch_scan(self, query_devices: list, interface_list: list, response_timeout: float = 20, 
                             retry: int = 2, custom_headers: Optional[dict]=None):

        found_devices = {}
        matching_devices = {}

        show_progress = False
        if self._interactive_mode:
            show_progress = True

        remaining_to_find = [hint for hint in query_devices]

        for ridx in range(0, retry):
            if ridx > 0:
                self._logger.info("MSEARCH: Not all devices found, retrying (count=%d)..." % ridx)
            iter_found_devices, iter_matching_devices = msearch_scan(remaining_to_find,
                interface_list=interface_list, response_timeout=response_timeout, custom_headers=custom_headers,
                show_progress=show_progress)
            found_devices.update(iter_found_devices)
            matching_devices.update(iter_matching_devices)

            for devusn in matching_devices.keys():
                if devusn in remaining_to_find:
                    remaining_to_find.remove(devusn)

            if len(remaining_to_find) == 0:
                break

        return found_devices, matching_devices

    def _device_scan_final_alternatives(self, query_devices: list, interface_list: list, response_timeout: float = 20, retry: int = 2):

        found_devices = {}
        matching_devices = {}

        missing_devices_checklist = [d for d in query_devices]

        # If we are missing some devices, lets try to wake them up and also attempt to find
        # them in the ARP table.
        self._logger.info("* Forcing the ARP table to refresh.")
        refresh_arp_table()

        # Try to use the ARP table to hint about the device
        self._logger.info("* Looking for device and interface hints in the APR table.")
        requery_devices = []
        arp_table = get_arp_table(normalize_hwaddr=True)
        for dmac, dinfo in arp_table.items():
            usn_match = None
            for usn in missing_devices_checklist:
                usn_norm = usn.replace(":", "").upper()
                if usn_norm.find(dmac) > -1:
                    usn_match = usn
                    break

            if usn_match is not None:
                missing_devices_checklist.remove(usn_match)
                requery_devices.append((usn_match, dinfo))

        self._logger.info("* Trying to requery the missing devices.")
        # As a last resort, rescan for the missing devices directly via unicast.
        for expusn, dev_hint in requery_devices:
            try:
                self.wakeup_device(expusn, dev_hint)

                requery_ip = None
                if dev_hint is not None:
                    requery_ip=dev_hint["ip"]

                device_info = msearch_query_host(requery_ip, query_usn=expusn, response_timeout=response_timeout)
                if device_info is not None:
                    found_devices[expusn] = device_info
                    query_devices.remove(expusn)

            except AKitTimeoutError:
                pass

        return found_devices, matching_devices

    def _device_scan_pre_msearch_query(self, lscape: "Landscape", query_devices: list, timeout: float, interval: float):
        """
            This method can be used by derived coordinators to find devices via other protocols
            prior to the use of the msearch protocol.
        """
        return []

    def _log_scan_results(self, found_devices: dict, matching_devices:dict , missing_devices: list):
        """
            Logs the results of the device scan.

            :param found_devices: A list of found devices.
            :param matching_devices: A list of devices matching the expected devices listed in the upnp_hint_list.
            :param missing_devices: A list of USN(s) for devices that were not found.
        """
        devmsg_lines = ["FOUND DEVICES:"]
        for dkey, _ in found_devices.items():
            devmsg_lines.append("    %s" % dkey)
        devmsg_lines.append("")

        devmsg_lines.append("MATCHING DEVICES:")
        for dkey, _ in matching_devices.items():
            devmsg_lines.append("    %s" % dkey)
        devmsg_lines.append("")

        if len(missing_devices) > 0:
            devmsg_lines.append("MISSING DEVICES:")
            for dkey in missing_devices:
                devmsg_lines.append("    %s" % dkey)
            devmsg_lines.append("")

        devmsg = os.linesep.join(devmsg_lines)
        self._logger.info(devmsg)

        return

    def _normalize_name(self, name: str) -> str:
        """
            Normalizes a name by removing non-alphanumeric characters.

            :param name: A name to normalize.

            :returns: The normalized name with all the non-alphanumeric characters removed.
        """
        # pylint: disable=no-self-use

        normal_chars = [ nc for nc in name if str.isalnum(nc) ]
        normal_name = ''.join(normal_chars)

        return normal_name

    def _process_device_alive_notification(self, ip_addr, usn_device: str, host: str, request_info: dict):
        """
            Processes a device alive notification when given the USN and dictionary of header keys and values.

            :param usn: The USN of the device which the notification is from.
            :param request_info: The headers from the notification request.
        """

        ip_addr = request_info[MSearchKeys.IP]
        location = request_info[MSearchKeys.LOCATION]

        # Get a reference to the landscape
        lscape = self.landscape

        self._activate_root_device(lscape, usn_device, ip_addr, location, request_info)

        return

    def _process_device_byebye_notification(self, ip_addr, usn_device: str, host: str, request_info: dict):
        """
            Processes a device byebye notification when given the USN and dictionary of header keys and values.

            :param usn: The USN of the device which the notification is from.
            :param request_info: The headers from the notification request.
        """

        ip_addr = request_info[MSearchKeys.IP]

        location = "Unknown"
        if MSearchKeys.LOCATION in request_info:
            location = request_info[MSearchKeys.LOCATION]

        # Get a reference to the landscape
        lscape = self.landscape

        self._deactivate_root_device(lscape, usn_device, ip_addr, location, request_info)

        return

    def _process_service_alive_notification(self, ip_addr, usn_device: str, usn_class: str, host: str, request_info: dict):
        return

    def _process_service_byebye_notification(self, ip_addr, usn_device: str, usn_class: str, host: str, request_info: dict):
        return

    def _process_subscription_callback(self, ifname: str, claddr: str, asock: socket):
        """
            Processes a callback request on the specified interface and address request.

            :param ifname: The name of the ifname the request came from.
            :param claddr: The address of the client that made the callback.
            :param request: The content of the callback request.
        """
        # pylint: disable=unused-argument

        cbbuffer = BytesIO()

        req_headers = None

        headers_length = None
        content_length = None

        message_length = None
        read_so_far = 0
        remaining_length = 1024
        try:
            # Read To Header
            while self._running and remaining_length > 0:
                # Process the requests
                nxtbuff = asock.recv(remaining_length)
                read_so_far += len(nxtbuff)

                # If we didn't get anything from recv, it means we hit the end of
                # the pipe.  We can exit the read loop.
                if len(nxtbuff) == 0:
                    break

                cbbuffer.write(nxtbuff)

                if req_headers is None:
                    current_content = cbbuffer.getvalue()
                    header_end = current_content.find(HTTP1_1_END_OF_HEADER)
                    if header_end > -1:
                        header_content = current_content[:header_end]
                        headers_length = len(header_content) + len(HTTP1_1_END_OF_HEADER)
                        req_line, req_headers = http_parse_header(header_content)
                        if "CONTENT-LENGTH" in req_headers:
                            content_length = int(req_headers["CONTENT-LENGTH"])
                            message_length = headers_length + content_length
                
                if message_length is not None:
                    remaining_length = message_length - read_so_far

        finally:
            asock.sendall(UPNP_SUBSCRIPTION_NOTIFY_RESPONSE_OK)
            asock.close()

        request = cbbuffer.getvalue()

        cbbuffer.truncate(0)
        cbbuffer.seek(0)

        req_body = request[headers_length:]

        capture_to = None
        self._coord_lock.acquire()
        try:
            if claddr in self._cl_callback_traffic_capture_from:
                capture_to = [cc for cc in self._cl_callback_traffic_capture_from[claddr].values()]
        finally:
            self._coord_lock.release()

        if capture_to is not None:
            for cc in capture_to:
                cc.append_capture(req_headers, req_body)

        if "SID" in req_headers:
            sid = req_headers["SID"]

            device = None
            #lookup the device that needs to handle this subscription
            self._coord_lock.acquire()
            try:
                if sid in self._cl_subscription_id_to_device:
                    device = self._cl_subscription_id_to_device[sid]
            finally:
                self._coord_lock.release()

            if device is not None:
                device.process_subscription_callback(claddr, sid, req_headers, req_body)
            else:
                errmsg = "Received subscription notification for unknown sid.  claddr={} sid={}".format(claddr, sid)
                self._logger.error(errmsg)
        else:
            dbgmsg_lines = [
                "Received subscription notification without an SID. claddr={}".format(claddr),
                "REQUEST HEADERS:"
            ]

            for hdr_key, hdr_val in req_headers.items():
                dbgmsg_lines.append("    {}:{}".format(hdr_key, hdr_val))

            dbgmsg_lines.append("REQUEST BODY:")
            dbgmsg_lines.append(req_body.decode("utf-8"))

            dbgmsg = os.linesep.join(dbgmsg_lines)

            self._logger.debug(dbgmsg)

        return

    def _process_request_for_msearch(self, addr: str, request: str):
        """
            Process an msearch request from the given address.

            :param addr: The address of machine making the msearch request.
            :param request: The request content of the msearch request to process.
        """
        #reqinfo = msearch_parse_request(request)
        self._logger.debug("RESPONDING TO MSEARCH")

        return

    def _process_request_for_notify(self, addr: str, request: str):
        """
            Process a notify request.

            :param addr: The address of machine making the notify request.
            :param request: The request content of the notify request to process.
        """
        req_headers, _ = notify_parse_request(request)

        usn = req_headers["USN"]
        host = req_headers["HOST"]
        subtype = req_headers["NTS"]

        ip_addr, _ = addr
        if MSearchKeys.IP not in req_headers:
            req_headers[MSearchKeys.IP] = ip_addr

        if usn.find("::") > -1:
            usn_device, usn_class = usn.split("::")
            usn_device = usn_device.lstrip("uuid:")

            ifname = get_interface_for_ip(ip_addr)

            req_headers[MSearchKeys.USN_DEV] = usn_device
            req_headers[MSearchKeys.USN_CLS] = usn_class
            req_headers[MSearchKeys.ROUTES] = {
                ifname:
                {
                    MSearchRouteKeys.IFNAME: ifname,
                    MSearchRouteKeys.IP: ip_addr
                }
            }

            if subtype == "ssdp:alive":
                if usn_class == "upnp:rootdevice":
                    self._process_device_alive_notification(ip_addr, usn_device, host, req_headers)
                else:
                    self._process_service_alive_notification(ip_addr, usn_device, usn_class, host, req_headers)
            elif subtype == "ssdp:byebye":
                if usn_class == "upnp:rootdevice":
                    self._process_device_byebye_notification(ip_addr, usn_device, host, req_headers)
                else:
                    self._process_service_byebye_notification(ip_addr, usn_device, usn_class, host, req_headers)
            else:
                self._logger.info("UNKNOWNK NOTIFY - USN: %s HOST: %s SUBTYPE: %s" % (usn, host, subtype))

        return

    def _start_all_threads(self):
        """
            Starts up all the thread the UPNP coordinator uses for monitoring, callback notification servicing and
            the worker threads used for processing work packges from notifications and callbacks.
        """

        ifacelist = []
        for wdev in self.watch_devices:
            primary_route = wdev.upnp.primary_route
            ifname = primary_route[MSearchRouteKeys.IFNAME]
            if ifname not in ifacelist:
                ifacelist.append(ifname)
        ifacecount = len(ifacelist)

        self._coord_lock.acquire()
        try:
            sgate = threading.Event()

            self._running = True

            self._shutdown_gate = threading.Semaphore(self._worker_count + ifacecount + 1)

            # Spin-up the worker threads first so they will be ready to handle work packets
            for wkrid in range(0, self._worker_count):
                sgate.clear()
                wthread = threading.Thread(name="UpnpCoordinator - Worker(%d)" % wkrid, target=self._thread_entry_worker,
                                                   daemon=True, args=(sgate,))
                self._cl_worker_threads.append(wthread)

                # Release the coordinator lock while starting up the thread so we are not holding it
                # so the new thread can get access to register itself with internal UpnpCoordinator state
                self._coord_lock.release()
                try:
                    wthread.start()
                    sgate.wait()
                finally:
                    self._coord_lock.acquire()

            # Spin-up the Monitor thread so it can monitor notification traffic
            sgate.clear()
            self._monitor_thread = threading.Thread(name="UpnpCoordinator - Monitor", target=self._thread_entry_monitor,
                                                   daemon=True, args=(sgate,))
            self._monitor_thread.start()
            sgate.wait()

            # Spin-up a Callback thread for each interface
            self._cl_iface_callback_addr_lookup = {}

            for ifaceidx in range(0, ifacecount):
                ifname = ifacelist[ifaceidx]
                sgate.clear()
                cbthread = threading.Thread(name="UpnpCoordinator - Callback(%s)" % ifname, target=self._thread_entry_callback,
                                                    daemon=True, args=(sgate, ifname))
                self._cl_callback_threads.append(cbthread)

                # Release the coordinator lock while starting up the thread so we are not holding it
                # so the new thread can get access to register itself with internal UpnpCoordinator state
                self._coord_lock.release()
                try:
                    cbthread.start()
                    sgate.wait()
                finally:
                    self._coord_lock.acquire()

        except:
            self._running = False

            for _ in range(0, self._worker_count + ifacecount + 1):
                self._shutdown_gate.release()

            raise
        finally:
            self._coord_lock.release()

        return

    def _thread_entry_callback(self, sgate: threading.Event, ifname: str):
        """
            The entry point for callback processing threads.

            :param sgate: The startup gate that is used to indicate to the thread spinning up the coordinator
                          that the callback thread has started.
            :param ifname: The interface name of interface this thread is assigned to process callbacks for.
        """
        self._shutdown_gate.acquire()

        try:
            service_addr = ""

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind to port zero so we can get an ephimeral port address
            sock.bind((service_addr, 0))

            _, port = sock.getsockname()
            host = get_ipv4_address(ifname)

            iface_callback_addr = "%s:%s" % (host, port)

            self._cl_iface_callback_addr_lookup[ifname] = iface_callback_addr
            self._cl_callback_interface_sockets[ifname] = sock

            # Set the start gate to allow the thread spinning us up to continue
            sgate.set()

            sock.listen(1)

            while self._running:
                asock, claddr = sock.accept()

                # Queue the callback workpacket for dispatching by a worker thread
                wkpacket = (self._process_subscription_callback, (ifname, claddr, asock))

                self._queue_lock.acquire()
                try:
                    self._queue_work.append(wkpacket)
                    self._queue_available.release()
                finally:
                    self._queue_lock.release()

        finally:
            self._shutdown_gate.release()

        return

    def _thread_entry_monitor(self, sgate: threading.Event):
        """
            The entry point for monitor thread.  The monitor thread sets up monitoring on all interfaces.

            :param sgate: The startup gate that is used to indicate to the thread spinning up the coordinator
                          that the monitor thread has started.
        """
        self._shutdown_gate.acquire()

        multicast_address = UpnpProtocol.MULTICAST_ADDRESS
        multicast_port = UpnpProtocol.PORT

        try:
            # Set the start gate to allow the thread spinning us up to continue
            sgate.set()

            while self._running:

                sock = create_multicast_socket(multicast_address, multicast_port)

                try:
                    request, addr = sock.recvfrom(1024)

                    if request.startswith(b"M-SEARCH"):
                        if self._control_point:
                            wkpacket = (self._process_request_for_msearch, (addr, request))
                            self._queue_lock.acquire()
                            try:
                                self._queue_work.append(wkpacket)
                                self._queue_available.release()
                            finally:
                                self._queue_lock.release()
                    elif request.startswith(b"NOTIFY"):
                        wkpacket = (self._process_request_for_notify, (addr, request))
                        self._queue_lock.acquire()
                        try:
                            self._queue_work.append(wkpacket)
                            self._queue_available.release()
                        finally:
                            self._queue_lock.release()
                    else:
                        dbgmsg = b"UNKNOWN REQUEST TYPE:\n" + request
                        dbgmsg = dbgmsg.decode("utf-8")
                        self._logger.debug(dbgmsg)

                finally:
                    sock.close()

        finally:
            self._shutdown_gate.release()

        return

    def _thread_entry_worker(self, sgate: threading.Event):
        """
            The entry point for worker threads.  Worker threads process work packets queued up by other threads.

            :param sgate: The startup gate that is used to indicate to the thread spinning up the coordinator
                          that this worker thread has started.
        """
        try:
            # Set the start gate to allow the thread spinning us up to continue
            sgate.set()

            while self._running:
                self._queue_available.acquire()

                self._queue_lock.acquire()
                try:
                    wkfunc, wkargs = self._queue_work.pop(0)
                    wkfunc(*wkargs)
                except: # pylint: disable=bare-except
                    self._logger.exception("UpnpCoordinator: Worker exception.")
                finally:
                    self._queue_lock.release()

        finally:
            self._shutdown_gate.release()

        return

    def _activate_root_device(self, lscape: "Landscape", usn_device: str, ip_addr: str, location: str, deviceinfo: dict):
        """
        """

        dev = self.lookup_device_by_upnp_usn(usn_device)
        if dev is not None:
            # Mark the device active
            dev.mark_alive()
        elif self._allow_unknown_devices:
            config_lookup = lscape._internal_get_upnp_device_config_lookup_table() # pylint: disable=protected-access

            usn_dev = deviceinfo[MSearchKeys.USN_DEV]

            marked_as_skip = False
            if usn_dev in config_lookup:
                configinfo = config_lookup[usn_dev]
                if "skip" in configinfo and configinfo["skip"]:
                    marked_as_skip = True

            if not marked_as_skip:
                devhint = None
                self._coord_lock.acquire()
                try:
                    devhint = self._cl_usn_to_hint[usn_device]
                finally:
                    self._coord_lock.release()

                self._update_root_device(lscape, config_lookup, ip_addr, location, devhint, deviceinfo)

        return

    def _deactivate_root_device(self, lscape: "Landscape", usn_device: str, ip_addr: str, location: str, deviceinfo: dict):
        """
        """
        dev = self.lookup_device_by_upnp_usn(usn_device)
        if dev is not None:
            # Mark the device active
            dev.mark_byebye()

        return

    def _update_root_device(self, lscape, config_lookup: dict, ip_addr: str, location: str, devhint: str, deviceinfo: dict):
        """
            Updates a UPNP root device.

            :param lscape: The landscape singleton instance.
            :param config_lookup: A configuration lookup table that can be used to lookup configuration information for upnp devices.
            :param ip_addr: The IP address of the device to update.
            :param location: The location URL associated with the device.
            :param deviceinfo: The device information from the msearch response headers.
            :param devhint: The identifier hint used to identify the device.
        """

        if MSearchKeys.USN_DEV in deviceinfo:
            try:
                usn_dev = deviceinfo[MSearchKeys.USN_DEV]
                usn_cls = deviceinfo[MSearchKeys.USN_CLS]

                configinfo = None
                if usn_dev in config_lookup:
                    configinfo = config_lookup[usn_dev]

                docTree = device_description_load(location)

                try:
                    # {urn:schemas-upnp-org:device-1-0}root
                    namespaces = {"": UPNP_DEVICE1_NAMESPACE}

                    deviceDescParts = device_description_find_components(location, docTree, namespaces=namespaces)
                    devNode, urlBase, manufacturer, modelName, modelNumber, modelDescription = deviceDescParts

                    dev_extension = None
                    skip_device = False
                    try:
                        # Acquire the lock before we decide if the location exists in the children table
                        self._coord_lock.acquire()
                        if location not in self._cl_children:
                            try:
                                # Unlock while we do some expensive stuff, we have already decided to
                                # create the device
                                self._coord_lock.release()

                                try:
                                    # We create the device
                                    dev_extension = self._create_root_device(manufacturer, modelNumber, modelDescription)
                                except:
                                    errmsg = "ERROR: Unable to create device mfg=%s model=%s desc=%s\nTRACEBACK:\n" % (manufacturer, modelNumber, modelDescription)
                                    errmsg += traceback.format_exc()
                                    self._logger.error(errmsg)
                                    raise

                                if isinstance(dev_extension, UpnpRootDevice):
                                    dev_extension.record_description(ip_addr, urlBase, manufacturer, modelName, docTree, devNode, namespaces=namespaces, upnp_recording=self._upnp_recording)

                                coord_ref = weakref.ref(self)

                                basedevice: LandscapeDevice = lscape._internal_lookup_device_by_hint(devhint)
                                if basedevice is None:
                                    if self._allow_unknown_devices:
                                        dev_type = "network/upnp"
                                        dev_config_info = {
                                            "deviceType": dev_type,
                                            "deviceClass": "unknown",
                                            "upnp": {
                                                "hint": usn_dev,
                                                "modelName": modelName,
                                                "modelNumber": modelNumber
                                            },
                                            "USN_DEV": usn_dev,
                                            "USN_CLS": usn_cls
                                        }
                                        dfid = FriendlyIdentifier(usn_dev, devhint)
                                        basedevice = lscape._create_landscape_device(dfid, dev_type, dev_config_info)
                                    else:
                                        skip_device = True

                                if basedevice is not None:
                                    basedevice.update_full_identifier(usn_dev)
                                    basedevice = lscape._enhance_landscape_device(basedevice, dev_extension)

                                    basedevice_ref = weakref.ref(basedevice)

                                    dev_extension.initialize(coord_ref, basedevice_ref, usn_dev, location, configinfo, deviceinfo)

                                    # Refresh the description
                                    dev_extension.refresh_description(ip_addr, self._factory, docTree.getroot(), namespaces=namespaces)
                                    dev_extension.mark_alive()

                                    basedevice.attach_extension("upnp", dev_extension)

                                    basedevice.initialize_features()
                                    basedevice.update_match_table(self._match_table)

                                    lscape._internal_activate_device(devhint)
                            finally:
                                self._coord_lock.acquire()

                            if skip_device:
                                infomsg = "Skipping device usn={} location={}".format(usn_dev, location)
                                self._logger.info(infomsg)
                            # If the device is still not in the table, add it
                            elif location not in self._cl_children:
                                self._cl_children[location] = dev_extension

                            self._cl_usn_to_hint[usn_dev] = devhint

                        else:
                            dev_extension = self._cl_children[location]
                            # Refresh the description
                            dev_extension.refresh_description(ip_addr, self._factory, docTree.getroot(), namespaces=namespaces)
                    finally:
                        self._coord_lock.release()

                except AKitSemanticError:
                    # Always allow semantic errors to propagate, semantic errors represent
                    # misuse of a test framework API and can be definitively classified
                    # as a test code bug that needs to be fixed.
                    raise

                except:  # pylint: disable=bare-except
                    exmsg = traceback.format_exc()
                    errmsg_lines = [
                        "ERROR: Unable to parse description for. IP: %s LOCATION: %s" % (ip_addr, location),
                        exmsg
                    ]
                    for k, v in deviceinfo.items():
                        errmsg_lines.append("    %s: %s" % (k, v))

                    errmsg = os.linesep.join(errmsg_lines)
                    self._logger.debug(errmsg)

            except AKitSemanticError:
                # Always allow semantic errors to propagate, semantic errors represent
                # misuse of a test framework API and can be definitively classified
                # as a test code bug that needs to be fixed.
                raise

            except:  # pylint: disable=bare-except
                exmsg = traceback.format_exc()
                errmsg_lines = [
                    "ERROR: Unable to parse description for. IP: %s LOCATION: %s" % (ip_addr, location),
                    exmsg
                ]
                for k, v in deviceinfo.items():
                    errmsg_lines.append("    %s: %s" % (k, v))

                errmsg = os.linesep.join(errmsg_lines)
                self._logger.debug(errmsg)

        return
