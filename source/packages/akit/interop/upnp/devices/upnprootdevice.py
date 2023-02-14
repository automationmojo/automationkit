"""
.. module:: upnprootdevice
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`UpnpRootDevice` class and associated diagnostic.

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

from optparse import Option
from typing import Dict, List, Optional, Tuple, Union, TYPE_CHECKING

import os
import re
import threading
import traceback
import uuid
import weakref

from datetime import datetime, timedelta
from urllib.parse import urlparse

from xml.etree.ElementTree import tostring as xml_tostring
from xml.etree.ElementTree import fromstring as xml_fromstring
from xml.etree.ElementTree import Element, ElementTree
from xml.etree.ElementTree import register_namespace

import requests

from requests.compat import urljoin

from akit.exceptions import AKitCommunicationsProtocolError, AKitHTTPRequestError, AKitNotOverloadedError, AKitRuntimeError
from akit.extensible import generate_extension_key
from akit.interop.upnp.upnperrors import UpnpError
from akit.paths import normalize_name_for_path

from akit.interop.landscaping.landscapedeviceextension import LandscapeDeviceExtension

from akit.interop.upnp.aliases import StrSvcId, StrSvcType, StrSubId
from akit.interop.upnp.upnpconstants import TIMEDELTA_RENEWAL_WINDOW
from akit.interop.upnp.upnpprotocol import MSearchRouteKeys
from akit.interop.upnp.devices.upnpdevice import UpnpDevice
from akit.interop.upnp.devices.upnpembeddeddevice import UpnpEmbeddedDevice
from akit.interop.upnp.xml.upnpdevice1 import UPNP_DEVICE1_NAMESPACE, UpnpDevice1Device, UpnpDevice1SpecVersion
from akit.interop.upnp.soap import NS_UPNP_EVENT

from akit.interop.upnp.paths import DIR_UPNP_SCAN_INTEGRATION_EMBEDDEDDEVICES
from akit.interop.upnp.paths import DIR_UPNP_SCAN_INTEGRATION_ROOTDEVICES
from akit.interop.upnp.paths import DIR_UPNP_SCAN_INTEGRATION_SERVICES
from akit.interop.upnp.upnpprotocol import MSearchKeys

from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

from akit.interop import upnp as upnp_module

from akit.networking.constants import AKitHttpHeaders
from akit.raisefor import raise_for_http_status

# Types imported only for type checking purposes
if TYPE_CHECKING:
    from akit.interop.upnp.upnpfactory import UpnpFactory

UPNP_DIR = os.path.dirname(upnp_module.__file__)

REGEX_SUBSCRIPTION_TIMEOUT = re.compile("^Second-([0-9]+|infinite)", flags=re.IGNORECASE)

def device_description_load(location: str) -> Union[ElementTree, None]:
    """
        Gets the description document from the specified URL and loads the contents into an XML ElementTree.

        :param location: The url of where to get the device description.

        :returns: The XML ElementTree for the XML content from the device description or None.
    """
    docTree = None

    resp = requests.get(location)
    if resp.status_code == 200:
        xmlcontent = resp.content

        docTree = ElementTree(xml_fromstring(xmlcontent))

    return  docTree


def device_description_find_components(location: str, docTree: ElementTree, namespaces: dict = {"": UPNP_DEVICE1_NAMESPACE}) -> Tuple[Element, str, str, str, str, str]:
    """
        Processes the device description and find the device description components.  The device
        description components are the manufacturer, modelName, modelNumber, modelDescription
        and the device description node.

        :param location: The URL location of where the device description document was obtained.
        :param docTree: The XML document ElementTree object.
        :param namespaces: A dictionary of namespaces to use when processing the device description document.

        :returns: A tuple with the (device node, urlBase, manufacturer, modelName, modelNumber, modelDescription)
    """
    # pylint: disable=dangerous-default-value

    devNode = docTree.find("device", namespaces=namespaces)

    urlBase = None
    baseURLNode = devNode.find("URLBase", namespaces=namespaces)
    if baseURLNode is not None:
        urlBase = baseURLNode.text

    url_parts = urlparse(location)
    host = url_parts.netloc

    # If urlBase was not set we need to try to use the schema and host as the urlBase
    if urlBase is None:
        urlBase = "%s://%s" % (url_parts.scheme, host)

    manufacturer = None
    modelName = None
    modelNumber = None
    modelDescription = None

    manufacturerNode = devNode.find("manufacturer", namespaces=namespaces)
    if manufacturerNode is not None:
        manufacturer = manufacturerNode.text

    modelNameNode = devNode.find("modelName", namespaces=namespaces)
    if modelNameNode is not None:
        modelName = modelNameNode.text

    modelNumberNode = devNode.find("modelNumber", namespaces=namespaces)
    if modelNumberNode is not None:
        modelNumber = modelNumberNode.text

    modelDescNode = devNode.find("modelDescription", namespaces=namespaces)
    if modelDescNode is not None:
        modelDescription = modelDescNode.text

    return devNode, urlBase, manufacturer, modelName, modelNumber, modelDescription

class UpnpRootDevice(UpnpDevice, LandscapeDeviceExtension):
    """
        The UPNP Root device is the base device for the hierarchy that is
        associated with a unique network devices location.  The :class:`UpnpRootDevice`
        and its subdevices are linked by thier location url.

        http://www.upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0.pdf
    """

    MANUFACTURER = "unknown"
    MODEL_NUMBER = "unknown"
    MODEL_DESCRIPTION = "unknown"

    SERVICE_NAMES = []

    def __init__(self, manufacturer: str, modelNumber: str, modelDescription):
        """
            Creates a root device object.
        """
        super(UpnpRootDevice, self).__init__()

        if self.MANUFACTURER != manufacturer:
            self.MANUFACTURER = manufacturer
        if self.MODEL_NUMBER != modelNumber:
            self.MODEL_NUMBER = modelNumber
        if self.MODEL_DESCRIPTION != modelDescription:
            self.MODEL_DESCRIPTION = modelDescription

        self._extra = {}
        self._cachecontrol = None
        self._ext = None
        self._server = None
        self._st = None
        self._usn = None
        self._usn_dev = None
        self._usn_cls = None

        self._specVersion = None

        self._host = None
        self._ip_address = None
        self._routes = None
        self._primary_route = None

        self._devices = {}
        self._device_descriptions = {}

        self._auto_subscribe = False
        self._mode = None

        self._root_device_lock = threading.RLock()

        self._subscriptions: Dict[StrSvcType, Tuple[StrSvcId, datetime]] = {}
        self._sid_to_service_lookup: Dict[str, UpnpServiceProxy] = {}
        self._variables = {}

        self._last_alive = datetime.min
        self._last_byebye = datetime.min
        self._available = False
        return

    @property
    def available(self) -> bool:
        """
            Returns the status of the device.
        """
        return self._available

    @property
    def cachecontrol(self) -> str:
        """
            The cache control timeout for the device from the MSEARCH response.
        """
        return self._cachecontrol

    @property
    def description(self) -> UpnpDevice1Device:
        """
            The UpnpDevice1Device device description.
        """
        desc = self._description
        return desc

    @property
    def embedded_device_descriptions(self) -> List[UpnpDevice1Device]:
        """
            Returns the list of descriptions for the embedded device that are declared for this root device.
        """
        dev_desc_list = []

        dev_desc = self._device_descriptions
        if dev_desc is not None:
            dev_desc_list = [devdesc for devdesc in dev_desc.values()]

        return dev_desc_list

    @property
    def embedded_devices(self) -> List[UpnpEmbeddedDevice]:
        """
            Returns the list of embedded devices that are declared for this root device.
        """
        devices_list = None

        devices = self._devices
        if devices is not None:
            devices_list = [dev for dev in devices]

        return devices_list

    @property
    def ext(self) -> str:
        """
            Returns the EXT header reported by the device in the MSEARCH response.
        """
        return self._ext

    @property
    def extra(self) -> dict:
        """
            Returns a dictionary that contains the extra thirdparty headers attached to UPNP MSEARCH responses.
        """
        return self._extra

    @property
    def IPAddress(self) -> str:
        """
            Returns the ip address of the root device that was found when the device responded with its MSEARCH response.
        """
        return self._ip_address

    @property
    def last_alive(self) -> datetime:
        """
            The datetime marker of the last time a UPNP alive or MSEARCH response was received
            from this device.
        """
        return self._last_alive

    @property
    def last_byebye(self) -> datetime:
        """
            The datetime marker of the last time a UPNP byebye was received from this device.
        """
        return self._last_byebye

    @property
    def MACAddress(self) -> Union[str, None]:
        """
            The MAC address of the device if specified in the device description or None.
        """
        macaddr = None
        desc = self.description
        if desc is not None:
            macaddr = desc.MACAddress
        return macaddr

    @property
    def mode(self) -> str:
        """
            The virtual mode assocatied with a device.  A device might present a different set of
            services depending on its current mode of operation.
        """
        return self._mode

    @property
    def modelName(self) -> Union[str, None]:
        """
            The model name of the device as found in the device description or None.
        """
        mname = None
        desc = self.description
        if desc is not None:
            mname = desc.modelName
        return mname

    @property
    def modelNumber(self )-> Union[str, None]:
        """
            The model number of the device as found in the device description or None.
        """
        mnumber = None
        desc = self.description
        if desc is not None:
            mnumber = desc.modelNumber
        return mnumber

    @property
    def primary_route(self):
        """
            Returns the primary rout for this UPNP devices.
        """
        return self._primary_route

    @property
    def routes(self) -> list:
        """
            A list of routes that can be used to communicate with the device.
        """
        return self._routes

    @property
    def server(self) -> str:
        """
            The 'SERVER' key specified in the MSEARCH response for this device.
        """
        return self._server

    @property
    def services(self) -> List[UpnpServiceProxy]:
        services_list = None

        services = self._services
        if services is not None:
            services_list = [svc for svc in services]

        return services_list

    @property
    def serialNumber(self) -> str:
        """
            The serial number number of the device as found in the device description.
        """
        desc = self.description
        return desc.serialNumber

    @property
    def specVersion(self) -> UpnpDevice1SpecVersion:
        """
            Returns the spec version of the device description.
        """
        return self._specVersion

    @property
    def USN(self) -> str:
        """
            The USN identifier specified in the MSEARCH response for this device.
        """
        return self._usn

    @property
    def USN_DEV(self) -> str:
        """
            The device component of the USN identifier specified in the MSEARCH response for this device.
        """
        return self._usn_dev

    @property
    def USN_CLS(self) -> str:
        """
            The class component of the USN identifier specified in the MSEARCH response for this device.
        """
        return self._usn_cls

    def get_custom_subscribe_headers(self) -> Optional[Dict[str, str]]:
        """
            An override-able method that allows for customization of the subscribe headers.
        """
        return None

    def initialize(self, coord_ref: weakref.ReferenceType, basedevice_ref: weakref.ReferenceType, extid: str, location: str, configinfo: dict, devinfo: dict):
        """
            Initializes the landscape device extension.

            :param coord_ref: A weak reference to the coordinator that is managing interactions through this
                              device extension.
            :param extid: A unique reference that can be used to identify this device via the coordinator even if its location changes.
            :param location: The location reference where this device can be found via the coordinator.
            :param configinfo: The UPNP configuration information associated with a device in the landscape configuration file.
            :param devinfo:  The device configuration information from the landscape configuration file.
        """
        # pylint: disable=arguments-differ

        LandscapeDeviceExtension.initialize(self, coord_ref, basedevice_ref, extid, location, configinfo)

        # We have to make a copy of the dictionary because we use
        # pop semantics to remove the items so we can pass on remaining
        # items to `_consume_upnp_extra`
        devinfo = devinfo.copy()

        self._cachecontrol = None
        if MSearchKeys.CACHE_CONTROL in devinfo:
            self._cachecontrol = devinfo.pop(MSearchKeys.CACHE_CONTROL)

        self._ext = None
        if MSearchKeys.EXT in devinfo:
            self._ext = devinfo.pop(MSearchKeys.EXT)

        self._server = None
        if MSearchKeys.SERVER in devinfo:
            self._server = devinfo.pop(MSearchKeys.SERVER)

        self._st = None
        if MSearchKeys.ST in devinfo:
            self._st = devinfo.pop(MSearchKeys.ST)

        self._usn = None
        if MSearchKeys.USN in devinfo:
            self._usn = devinfo.pop(MSearchKeys.USN)

        self._usn_dev = None
        if MSearchKeys.USN_DEV in devinfo:
            self._usn_dev = devinfo.pop(MSearchKeys.USN_DEV)

        self._usn_cls = None
        if MSearchKeys.USN_CLS in devinfo:
            self._usn_cls = devinfo.pop(MSearchKeys.USN_CLS)

        self._routes = [r for r in devinfo.pop(MSearchKeys.ROUTES).values()]

        self._primary_route = self._routes[0]

        self._consume_upnp_extra(devinfo)
        return

    def lookup_device(self, device_type: str) -> Union[UpnpEmbeddedDevice, None]:
        """
            Looks up an embedded device by its device type identifier.

            :param device_type: The device type identifier of the embedded device to find.

            :returns: The specified UpnpEmbeddedDevice or None
        """
        device = None

        self._device_lock.acquire()
        try:
            device = self._devices[device_type]
        finally:
            self._device_lock.release()

        return device

    def mark_alive(self):

        self._device_lock.acquire()
        try:
            self._last_alive = datetime.now()
            self._available = True
        finally:
            self._device_lock.release()

        return

    def mark_byebye(self):

        self.mark_unavailable(reason="byebye", byebye=True)

        return

    def mark_unavailable(self, reason: str="mark_unavailable", byebye: bool=False):
        """
            :param byebye: Indicates this method is being called from 'mark_byebye' as a result
                           of a byebye message being received.
        """

        self._device_lock.acquire()
        try:
            if byebye:
                self._last_byebye = datetime.now()

            if self._available:

                device_identity = self.basedevice.identity

                self._available = False

                subscription_type_list = [st for st in self._subscriptions.keys()]

                for svc_type in subscription_type_list:
                    sub_sid, _ = self._subscriptions[svc_type]

                    if sub_sid in self._sid_to_service_lookup:
                        svc_obj = self._sid_to_service_lookup[sub_sid]

                    # Call notify_byebye on each service object so we can mark all the
                    # references to variables as expired.
                    svc_obj.invalidate_subscription()

                    # Since we got a byebye, remove the subscription information
                    dbgmsg = "Removing subscription for device {} service {}, because of {}.".format(
                        device_identity, svc_type, reason
                    )
                    self._logger.debug(dbgmsg)
                    del self._subscriptions[svc_type]

        finally:
            self._device_lock.release()

        return

    def process_subscription_callback(self, sender_ip, sid: str, headers: dict, body: str):
        """
            This is used by the subscription callback thread to handoff work packets to the a worker thread
            and completes the processing of the subscription callback and routing to a UpnpRootDevice and
            UpnpServiceProxy instance.

            :param sender_ip: The IP address of the entity sending the update
            :param sid: The Subscription ID (sid) associated with the subscription callback
            :param headers: The HTTP headers contained in the callback response.
            :param body: The body content of the HTTP subscription callback.
        """
        # pylint: disable=unused-argument

        service = None

        self._device_lock.acquire()
        try:
            if sid in self._sid_to_service_lookup:
                service = self._sid_to_service_lookup[sid]
        finally:
            self._device_lock.release()

        if service is not None:
            docTree = ElementTree(xml_fromstring(body))

            psetNode = docTree.getroot()

            if psetNode is not None and psetNode.tag == "{%s}propertyset" % NS_UPNP_EVENT:
                propertyNodeList = psetNode.findall("{%s}property" % NS_UPNP_EVENT)

                service._update_event_variables(sender_ip, self._usn_dev, propertyNodeList) # pylint: disable=protected-access

        return

    def query_device_description(self):
        """
            Queries the UPnP device for its description.
        """
        desc = device_description_load(self._location)
        return desc


    def record_description(self, ip_addr: str, urlBase: str, manufacturer: str, modelName: str, docTree: ElementTree, devNode: Element, namespaces: str, upnp_recording: bool = False):
        """
            Called to record a description of a UPNP root device.

            :param urlBase: The base url as detailed in the description document or if not specified as determined by looking at the host information.
            :param manufacturer: The manufacturer of the device.
            :param modelName: The model name of the device.
            :param docTree: The XML document tree from the root of the device description.
            :param devNode: The 'device' element node from the device description.
            :param namespaces: A dictionary of namespaced to use when processing the XML document.
            :param upnp_recording: Force the recording of the device description and will overwrite existing device descriptions.
        """
        manufacturerNormalized = normalize_name_for_path(manufacturer)
        modelName = normalize_name_for_path(modelName)

        root_dev_dir = os.path.join(DIR_UPNP_SCAN_INTEGRATION_ROOTDEVICES, manufacturerNormalized)
        if not os.path.exists(root_dev_dir):
            os.makedirs(root_dev_dir)

        root_dev_def_file = os.path.join(root_dev_dir, modelName + ".xml")

        if upnp_recording:
            console_msg_lines = [
                "================================================================",
                " Recording Device: {}".format(ip_addr),
                "------------------------- Detail -------------------------------",
                "     Manufacturer: {}".format(manufacturer),
                "            Model: {}".format(modelName),
                "      Device File: {}".format(root_dev_def_file)
            ]
            console_msg = os.linesep.join(console_msg_lines)
            print(console_msg)

        if upnp_recording or not os.path.exists(root_dev_def_file):
            docNode = docTree.getroot()
            register_namespace('', namespaces[''])
            pretty_dev_content = xml_tostring(docNode, short_empty_elements=False)
            with open(root_dev_def_file, 'wb') as rddf:
                rddf.write(pretty_dev_content)

        indent = "    "
        next_indent = indent + "    "
        embDevList = devNode.find("deviceList", namespaces=namespaces)
        if embDevList is not None:
            if upnp_recording:
                print("{}[ Embedded Devices ]".format(indent))

            for embDevNode in embDevList:
                self._record_embedded_device(urlBase, manufacturerNormalized, embDevNode, namespaces, upnp_recording=upnp_recording, indent=next_indent)

            if upnp_recording:
                print("")

        svcList = devNode.find("serviceList", namespaces=namespaces)
        if svcList is not None:
            if upnp_recording:
                print("{}[ Services ]".format(indent))

            for svcNode in svcList:
                self._record_service( urlBase, manufacturerNormalized, svcNode, namespaces, upnp_recording=upnp_recording, indent=next_indent)

            if upnp_recording:
                print("")


        if upnp_recording:
            print()

        return

    def refresh_description(self, ipaddr: str, factory: "UpnpFactory", docNode: Element, namespaces=Optional[dict]):
        """
            Called by the UPNP coordinator to refresh the decription information for a device.

            :param ipaddr: IP address of the device to update the description for.
            :param factory: The UpnpFactory that can be used to instantiate devices.
            :param docNode: The root node of the description document.
            :param namespaces: A dictionary of namespaces to use when processing the device description.
        """
        try:
            if self._ip_address is not None and self._ip_address != ipaddr:
                self._logger.debug("UpnpRootDevice - IP Address change for device usn={} location={}.".format(
                    self._usn, self._ip_address
                ))

            self._ip_address = ipaddr

            specVerNode = docNode.find("specVersion", namespaces=namespaces)
            if specVerNode is not None:
                self._locked_process_version_node(specVerNode, namespaces=namespaces)

            baseURLNode = docNode.find("URLBase", namespaces=namespaces)
            if baseURLNode is not None:
                self._locked_process_urlbase_node(baseURLNode, namespaces=namespaces)

            url_parts = urlparse(self._location)
            self._host = url_parts.netloc

            # If urlBase was not set we need to try to use the schema and host as the urlBase
            if self._urlBase is None:
                self._urlBase = "%s://%s" % (url_parts.scheme, self._host)

            devNode = docNode.find("device", namespaces=namespaces)
            if devNode is not None:
                self._process_device_node(factory, devNode, namespaces=namespaces)

            self._enhance_device_detail()

        except Exception:
            err_msg = traceback.format_exc()
            print(err_msg)
            raise

        return

    def set_auto_subscribe(self, val, factory: Optional["UpnpFactory"] = None):
        self._auto_subscribe = val
        return

    def subscribe_to_all_services(self, factory: Optional["UpnpFactory"] = None):
        """
            The 'subscribe_to_all_services' method is overriden by derived objects in order
            to allow for bulk subscription to device services.

            ..note: Use with caution, if auto_subscribe is turned on, subscriptions are automatically
            created when the values of variables are attempted to be consumed via 'wait_for_value' and
            'wait_for_update'
        """

        for svc_name in self.SERVICE_NAMES:
            svc = self.lookup_service(self.MANUFACTURER, svc_name, allow_none=True, factory=factory)
            if svc is not None:
                try:
                    self.subscribe_to_events(svc)
                except:
                    errmsg = traceback.format_exc()
                    self._logger.debug(errmsg)
            else:
                errmsg = "Lookup service failed for mfg={} svc={}".format(self.MANUFACTURER, svc_name)
                self._logger.debug(errmsg)

        return

    def subscribe_to_events(self, service: UpnpServiceProxy, renew: bool=False, timeout: Optional[float] = None):
        """
            Creates a subscription to the event name specified and returns a
            UpnpEventVar object that can be used to read the current value for
            the given event.

            :param service: A :class:`akit.interop.upnp.services.upnpserviceproxy.UpnpServiceProxy`
                            for which to subscribe to events.
            :param timeout: The timeout to pass as a header when creating the subscription.
        """
        sub_sid = None
        sub_expires = None

        if len(service.SERVICE_EVENT_VARIABLES) > 0:

            service_type = service.SERVICE_TYPE

            new_subscription = False
            self._device_lock.acquire()
            try:
                if service_type not in self._subscriptions:
                    new_subscription = True
                    self._subscriptions[service_type] = (None, None)
                else:
                    sub_sid, sub_expires = self._subscriptions[service_type]

                    if sub_sid is None and sub_expires is None:
                        # The service was unsubscribed so this is the same as a new
                        # subscription.
                        new_subscription = True
            finally:
                self._device_lock.release()

            check_time = datetime.now() + timedelta(seconds=TIMEDELTA_RENEWAL_WINDOW)
            if sub_expires is not None and check_time > sub_expires:
                renew = True

            if new_subscription or renew:
                # If we created an uninitialized variable and added it to the subsciptions table
                # we need to statup the subsciption here.  If the startup process fails, we can
                # later remove the subscription from the subscription table.

                serviceManufacturer = normalize_name_for_path(self.MANUFACTURER)
                svckey = generate_extension_key(serviceManufacturer, service_type)
                service = self._services[svckey]

                subscribe_url = urljoin(self.URLBase, service.eventSubURL)
                subscribe_auth = ""

                coord = self._coord_ref()

                ifname = self._primary_route[MSearchRouteKeys.IFNAME]

                callback_url = coord.lookup_callback_url_for_interface(ifname)
                if callback_url is None:
                    errmsg = "No callback url found for ifname={}".format(ifname)
                    raise AKitRuntimeError(errmsg) from None

                headers = { "HOST": self._host, "User-Agent": AKitHttpHeaders.USER_AGENT, "CALLBACK": callback_url, "NT": "upnp:event"}
                if timeout is not None:
                    headers["TIMEOUT"] = "Seconds-%s" % timeout

                custom_headers = self.get_custom_subscribe_headers()
                if custom_headers is not None:
                    headers.update(custom_headers)

                resp = requests.request(
                    "SUBSCRIBE", subscribe_url, headers=headers, auth=subscribe_auth
                )

                if resp.status_code == 200:
                    #============================== Expected Response Headers ==============================
                    # SID: uuid:RINCON_7828CA09247C01400_sub0000000207
                    # TIMEOUT: Second-86400
                    # Server: Linux UPnP/1.0 Sonos/62.1-82260-monaco_dev (ZPS13)
                    # Connection: close
                    resp_headers = {k.upper(): v for k, v in resp.headers.items()}

                    nxtheader = None
                    try:
                        nxtheader = "SID"
                        sub_sid = resp_headers[nxtheader]

                        nxtheader = "TIMEOUT"
                        sub_timeout_str = resp_headers[nxtheader]
                    except KeyError as kerr:
                        errmsg = "Event subscription response was missing in %r header." % nxtheader
                        raise AKitCommunicationsProtocolError(errmsg) from kerr

                    sub_timeout = None
                    mobj = REGEX_SUBSCRIPTION_TIMEOUT.match(sub_timeout_str)
                    if mobj is not None:
                        timeout_str = mobj.groups()[0]
                        sub_timeout = 86400 if timeout_str == "infinite" else int(timeout_str)

                    if sub_sid is not None:
                        sub_expires = datetime.now() + timedelta(seconds=sub_timeout)
                        self._device_lock.acquire()
                        try:
                            self._sid_to_service_lookup[sub_sid] = service
                            self._subscriptions[service_type] = (sub_sid, sub_expires)
                        finally:
                            self._device_lock.release()

                        # Notify the coordinator which device has this subscription, we need to
                        # register the subscription ID so the coordinator can forward along
                        # notify message content
                        coord.register_subscription_for_device(sub_sid, self)
                    else:
                        self._device_lock.acquire()
                        try:
                            if service_type in self._subscriptions:
                                del self._subscriptions[service_type]
                        finally:
                            self._device_lock.release()

                else:
                    context_msg = "SUBSCRIBING at {}:".format(subscribe_url)
                    details = {
                        "SERVICE_KEY:": svckey,
                        "URL_BASE": self.URLBase,
                        "EVENT_SUB_URL": service.eventSubURL
                    }
                    raise_for_http_status(context_msg, resp, details=details)

        return sub_sid, sub_expires

    def unsubscribe_to_events(self, service: UpnpServiceProxy, subscription_id: Optional[str]=None):
        """
        """

        if len(service.SERVICE_EVENT_VARIABLES) > 0:
            if subscription_id is None:
                subscription_id = service.subscriptionId

            service._clear_subscription()

            subscribe_url = urljoin(self.URLBase, service.eventSubURL)
            subscribe_auth = ""
            headers = { "HOST": self._host, "User-Agent": AKitHttpHeaders.USER_AGENT, "SID": subscription_id}
                
            resp = requests.request(
                    "UNSUBSCRIBE", subscribe_url, headers=headers, auth=subscribe_auth
                )
            if resp.status_code != 200 and resp.status_code != 412:
                errmsg = "Error while unsubscribing from service."
                raise UpnpError(resp.status_code, errmsg)

        return

    def switchModes(self, mode: str):
        """
            Called to trigger the switching of a devices mode of operation.  This function is
            device specific and needs to be overloaded by custom UPNP device implementations.
        """
        self._mode = mode
        raise AKitNotOverloadedError("UpnpRootDevice.switchModes must be overloaded by custom UPNP devices.") from None

    def to_dict(self, brief=False) -> dict:
        """
            Returns a description of this device as a python dictionary.

            :param brief: A booliean value which indicates if a brief or full description is desired.

            :returns: The python dictionary description of the device.
        """
        dval = super(UpnpRootDevice, self).to_dict(brief=brief)
        dval["IPAddress"] = self.IPAddress
        dval["USN"] = self.USN
        dval["USN_DEV"] = self.USN_DEV
        dval["USN_CLS"] = self.USN_CLS
        return dval

    def to_json(self, brief=False) -> str:
        """
            Returns a description of this device in JSON format.

            :param brief: A booliean value which indicates if a brief or full description is desired.

            :returns: The JSON description of the device.
        """
        json_str = super(UpnpRootDevice, self).to_json(brief=brief)
        return json_str

    def _consume_upnp_extra(self, extrainfo: dict):
        """
            Called during the processing of MSEARCH responses for the device with
            a dictionary of any non-standard HTTP headers.

            :param extrainfo: A dictionary of extra headers found in the devices responses.  This
                              allows custom devices to overload this method and consume these extra
                              device response headers.
        """
        # pylint: disable=no-self-use

        self._extra = extrainfo
        return

    def _create_device_description_node(self, devNode: Element, namespaces: Optional[dict] = None):
        """
            Called in order for a device description to be created.  This could be overloaded by
            custom UPNP devices in order to create custome device description objects.

            :param devNode: The XML element of the root node of the device description document.
            :param namespaces: A dictionary of namespaces to use when processing the device description.
        """
        # pylint: disable=no-self-use
        dev_desc_node = UpnpDevice1Device(devNode, namespaces=namespaces)
        return dev_desc_node

    def _enhance_device_detail(self):
        """
            Can be implemented by custom devices in order to be able query for and enhance a devices
            information during the device update process.
        """
        # pylint: disable=no-self-use
        return

    def _locked_populate_embedded_device_descriptions(self, factory: "UpnpFactory", description: UpnpDevice1Device):
        """
            Called in order to process embedded device descriptions and to instantiate embedded device instances.

            NOTE: This method should be called with the device lock held.
        """
        for deviceInfo in description.deviceList:
            manufacturer = deviceInfo.manufacturer.strip()
            modelNumber = deviceInfo.modelNumber.strip()
            modelDescription = deviceInfo.modelDescription.strip()

            devkey = ":".join([manufacturer, modelNumber, modelDescription])

            if devkey not in self._device_descriptions:
                dev_inst = factory.create_embedded_device_instance(manufacturer, modelNumber, modelDescription)
                self._device_descriptions[devkey] = dev_inst

                self._locked_populate_services_descriptions(factory, deviceInfo)
            else:
                dev_inst = self._device_descriptions[devkey]

            dev_inst.update_description(self._host, self._urlBase, deviceInfo)
        return

    def _locked_process_urlbase_node(self, urlBaseNode: Element, namespaces: Optional[dict] = None):
        """
            Called in order to process the base url information from the device description.

            :param urlBaseNode: The XML Element node that contains the urlBaseNode information.
            :param namespaces: A dictionary of namespaces to use when processing the device description.

            NOTE: This method should be called with the device lock held.
        """
        # pylint: disable=unused-argument

        self._urlBase = urlBaseNode.text.rstrip("/")
        return

    def _locked_process_version_node(self, verNode: Element, namespaces: Optional[dict] = None):
        """
            Called in order to process the spec version information from the device description.

            :param verNode: The XML Element node of the version node.
            :param namespaces: A dictionary of namespaces to use when processing the device description.

            NOTE: This method should be called with the device lock held.
        """
        self._specVersion = UpnpDevice1SpecVersion(verNode, namespaces=namespaces)
        return

    def _matches_model_name(self, modelName: str) -> bool:
        """
            Method used to determine if the modelName passed matches the model name of this device.

            :param modelName: The modelName to evaluate for matching with this device.
        """
        matches = False
        if self.modelName == modelName:
            matches = True

        return matches

    def _matches_model_number(self, modelNumber: str)-> bool:
        """
            Method used to determine if the modelNumber passed matches the model number of this device.

            :param modelNumber: The modelNumber to evaluate for matching with this device.
        """
        matches = False
        if self.modelNumber == modelNumber:
            matches = True

        return matches

    def _process_device_node(self, factory: "UpnpFactory", devNode: Element, namespaces: Optional[dict] = None):
        """
            Method called for processing the 'device' node of the XML description of a device.

            :param factory: The UpnpFactory instance that is used to instantiate devices, embedded devices and service proxies.
            :param devNode: The XML Element node of the 'device' node.
            :param namespaces: A dictionary of namespaces to use when processing the device description.
        """
        description = self._create_device_description_node(devNode, namespaces=namespaces)

        self._device_lock.acquire()
        try:
            self._locked_populate_services_descriptions(factory, description)

            self._locked_populate_embedded_device_descriptions(factory, description)

            self._description = description
        finally:
            self._device_lock.release()

        return

    def _record_embedded_device(self, urlBase: str, manufacturer: str, embDevNode: Element, namespaces: Optional[dict] = None, upnp_recording: bool = False, indent="    "):
        """
            Method called for recording the description of an embedded device from a device description.

            :param manufacturer: The manufacturer of the device.
            :param embDevNode: The XML element node of the embedded device.
            :param namespaces: A dictionary of namespaces to use when processing the device description.
            :param upnp_recording: A boolean value indicating if the embedded device description should be recorded regardless of whether
                                    an existing description has been recorded.
        """
        # pylint: disable=no-self-use

        deviceTypeNode = embDevNode.find("deviceType", namespaces=namespaces)
        if deviceTypeNode is not None:
            deviceType = deviceTypeNode.text

            dyn_dev_dir = os.path.join(DIR_UPNP_SCAN_INTEGRATION_EMBEDDEDDEVICES, manufacturer)
            if not os.path.exists(dyn_dev_dir):
                os.makedirs(dyn_dev_dir)

            dyn_dev_filename = os.path.join(dyn_dev_dir, deviceType + ".xml")
            if upnp_recording or not os.path.exists(dyn_dev_filename):
                if upnp_recording:
                    dev_msg_lines = [
                        "{}Embedded Device Type: {}".format(indent, deviceType),
                        "{}Embedded Device File: {}".format(indent, dyn_dev_filename)
                    ]
                    dev_msg = os.linesep.join(dev_msg_lines)
                    print(dev_msg)

                pretty_sl_content = ""

                srcSvcListNode = embDevNode.find("serviceList", namespaces=namespaces)
                if srcSvcListNode is not None:
                    svcs_indent = indent + "    "
                    if upnp_recording:
                        print("{}[ Embedded Services ]".format(indent))

                    for svcNode in srcSvcListNode:
                        self._record_service( urlBase, manufacturer, svcNode, namespaces,
                                              upnp_recording=upnp_recording,
                                              indent=svcs_indent)

                    if upnp_recording:
                        print("")

                    register_namespace('', namespaces[''])
                    pretty_sl_content = xml_tostring(srcSvcListNode)

                with open(dyn_dev_filename, 'wb') as edf:
                    edf.write(b"<device>\n")
                    edf.write(pretty_sl_content)
                    edf.write(b"</device\n")

        return

    def _record_service(self, urlBase: str, manufacturer: str, svcNode: Element, namespaces: Optional[dict] = None, upnp_recording: bool = False, indent="    "):
        """
            Called to record the description of a device service.

            :param urlBase: The base url of the device which is used to request further information based on relative URLs from the device description.
            :param manufacturer: The manufacturer of the device.
            :param svcNode: The XML Element for the 'service' description node.
            :param namespaces: A dictionary of namespaces to use when processing the device description.
            :param upnp_recording: A boolean value indicating if the embedded device description should be recorded regardless of whether
                                    an existing description has been recorded.
        """
        # pylint: disable=broad-except

        serviceTypeNode = svcNode.find("serviceType", namespaces=namespaces)
        scpdUrlNode = svcNode.find("SCPDURL", namespaces=namespaces)
        if serviceTypeNode is not None and scpdUrlNode is not None:

            serviceType = serviceTypeNode.text

            scpdUrl = scpdUrlNode.text
            if urlBase is not None:
                scpdUrl = urlBase.rstrip("/") + "/" + scpdUrl.lstrip("/")

            dyn_service_dir = os.path.join(DIR_UPNP_SCAN_INTEGRATION_SERVICES, manufacturer)
            if not os.path.exists(dyn_service_dir):
                os.makedirs(dyn_service_dir)

            dyn_svc_filename = os.path.join(dyn_service_dir, "%s.xml" % (serviceType,))
            if upnp_recording or not os.path.exists(dyn_svc_filename):
                if upnp_recording:
                    svc_msg_lines = [
                        "{}Service Type: {}".format(indent, serviceType),
                        "{} Service URL: {}".format(indent, scpdUrl),
                        "{}Service File: {}".format(indent, dyn_svc_filename)
                    ]
                    svc_msg = os.linesep.join(svc_msg_lines)
                    print(svc_msg)

                try:
                    resp = requests.get(scpdUrl)
                    if resp.status_code == 200:
                        svc_content = resp.content
                        with open(dyn_svc_filename, 'wb') as sdf:
                            sdf.write(svc_content)
                    else:
                        self._logger.warn("Unable to retrieve service description for manf=%s st=%s url=%s" % (manufacturer, serviceType, scpdUrl))
                except Exception:
                    self._logger.exception("Exception while retreiving service description.")

        return

    def __str__(self):
        """
            Returns a brief description of the device as a string.
        """
        rtnstr = "%s: USN:%s MAC=%s IP=%s" % (self.modelName, self.USN, self.MACAddress, self.IPAddress)
        return rtnstr
