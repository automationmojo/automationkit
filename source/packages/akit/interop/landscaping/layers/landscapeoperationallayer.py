"""
.. module:: landscapeconfigurationlayer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the Landscape related classes.

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

# ====================================================================================
#
#                               OPERATIONAL LAYER
#
# ====================================================================================

from typing import List, Optional, Union

import inspect
import json
import os
import threading

import zeroconf

from akit.exceptions import AKitConfigurationError, AKitSemanticError
from akit.friendlyidentifier import FriendlyIdentifier
from akit.interop.landscaping.landscapedevice import LandscapeDevice

from akit.paths import get_path_for_output

from akit.interop.coordinators.powercoordinator import PowerCoordinator
from akit.interop.coordinators.serialcoordinator import SerialCoordinator

from akit.interop.landscaping.landscapedevice import LandscapeDevice

from akit.interop.dns.mdnsservicecatalog import MdnsServiceCatalog

class LandscapeOperationalLayer:
    """
    """

    _operational_gate = None

    MDNS_BROWSE_TYPES = ["_http._tcp.local.", "_sonos._tcp.local."]

    def __init__(self):
        self._power_coord = None
        self._serial_coord = None

        self._upnp_coord = None
        self._ssh_coord = None

        self._active_devices = {}

        self._device_pool = {}
        self._checked_out_devices = {}

        self._activation_errors = []

        self._first_contact_results = None

        self._integration_points_activated = {}
        self._integration_point_activation_counter = 0

        super().__init__()

        self._zeroconf = zeroconf.Zeroconf()
        self._zeroconf_catalog = MdnsServiceCatalog(self.logger)
        self._zeroconf_browser = zeroconf.ServiceBrowser(self._zeroconf, self.MDNS_BROWSE_TYPES, self._zeroconf_catalog)

        return

    @property
    def ssh_coord(self):
        """
            Returns a the :class:`SshPoolCoordinator` that is used to manage ssh devices.
        """
        self._ensure_activation()
        return self._ssh_coord

    @property
    def upnp_coord(self):
        """
            Returns a the :class:`UpnpCoordinator` that is used to manage upnp devices.
        """
        self._ensure_activation()
        return self._upnp_coord

    def activate_integration_point(self, role: str, coordinator_constructor: callable):
        """
            This method should be called from the attach_to_environment methods from individual couplings
            in order to register the base level integrations.  Integrations can be hierarchical so it
            is only necessary to register the root level integration couplings, the descendant couplings can
            be called from the root level couplings.

            :param role: The name of a role to assign for a coupling.
            :param coupling: The coupling to register for the associated role.
        """

        if role.startswith("coordinator/"):
            
            if "coordinator/serial" not in self._integration_points_activated:
                self._integration_points_activated["coordinator/serial"] = True

            if "coordinator/power" not in self._integration_points_activated:
                self._integration_points_activated["coordinator/power"] = True

            _, coord_type = role.split("/")
            if coord_type == "upnp" or coord_type == "ssh":
                if role not in self._integration_points_activated:
                    self._integration_points_activated[role] = coordinator_constructor
                else:
                    raise AKitSemanticError("Attempted to activate the UPNP coordinator twice.") from None
            else:
                raise AKitSemanticError("Unknown coordinator type '%s'." % role) from None
        else:
            raise AKitSemanticError("Don't know how to activate integration point of type '%s'." % role) from None

        return

    def activate_operations(self, allow_missing_devices: bool=False, allow_unknown_devices: bool=False, upnp_recording: bool=False,
                            validate_features: bool=True, validate_topology: bool=True):

        thisType = type(self)

        self.landscape_lock.acquire()
        try:

            if thisType._operational_gate is None:
                thisType._operational_gate = threading.Event()
                thisType._operational_gate.clear()

                # Don't hold the landscape like while we wait for the
                # landscape to be activated
                self.landscape_lock.release()
                try:
                    if "coordinator/serial" in self._integration_points_activated:
                        self._activate_serial_coordinator()
                    
                    if "coordinator/power" in self._integration_points_activated:
                        self._activate_power_coordinator()
                    
                    if "coordinator/upnp" in self._integration_points_activated:
                        coordinator_constructor = self._integration_points_activated["coordinator/upnp"]
                        self._activate_upnp_coordinator(coordinator_constructor)
                    
                    if "coordinator/ssh" in self._integration_points_activated:
                        coordinator_constructor = self._integration_points_activated["coordinator/ssh"]
                        self._activate_ssh_coordinator(coordinator_constructor)

                    self._establish_connectivity(allow_missing_devices=allow_missing_devices, 
                                                 allow_unknown_devices=allow_unknown_devices,
                                                 upnp_recording=upnp_recording)

                    self._zeroconf_browser.cancel()

                    if validate_features:
                        self._features_validate()

                    if validate_topology:
                        self._topology_validate()

                    self._operational_gate.set()

                finally:
                    self.landscape_lock.acquire()

            else:

                # Don't hold the landscape like while we wait for the
                # landscape to be activated
                self.landscape_lock.release()
                try:
                    # Because the landscape is a global singleton and because
                    # we were not the first thread to call the activate method,
                    # wait for the first calling thread to finish activating the
                    # Landscape before we return allowing other use of the Landscape
                    # singleton
                    self._operational_gate.wait()
                finally:
                    self.landscape_lock.acquire()

        finally:
            self.landscape_lock.release()

        return

    def checkin_device(self, device: LandscapeDevice):
        """
            Returns a landscape device to the the available device pool.
        """
        self._ensure_activation()

        identity = device.identity

        if identity not in self._checked_out_devices:
            errmsg = "Attempting to checkin a device that is not checked out. {}".format(device)
            raise AKitSemanticError(errmsg)

        self.landscape_lock.acquire()
        try:
            self._device_pool[identity] = device
            del self._checked_out_devices[identity]
        finally:
            self.landscape_lock.release()

        return
    
    def checkin_multiple_devices(self, devices: List[LandscapeDevice]):
        """
            Returns a landscape device to the the available device pool.
        """
        self._ensure_activation()

        checkin_errors = []

        self.landscape_lock.acquire()
        try:

            for dev in devices:
                identity = dev.identity

                if identity not in self._checked_out_devices:
                    self._device_pool[identity] = dev
                    checkin_errors.append(dev)

            if len(checkin_errors) > 0:
                err_msg_lines = [
                    "Attempting to checkin a device that is not checked out.",
                    "DEVICES:"
                ]
                for dev in checkin_errors:
                    err_msg_lines.append("    {}".format(dev))

                err_msg = os.linesep.join(err_msg_lines)
                raise AKitSemanticError(err_msg)

            for dev in devices:
                identity = dev.identity

                if identity in self._checked_out_devices:
                    self._device_pool[identity] = dev
                    del self._checked_out_devices[identity]

        finally:
            self.landscape_lock.release()

        return

    def checkout_a_device_by_modelName(self, modelName: str) -> Optional[LandscapeDevice]:
        """
            Checks out a single device from the available pool using the modelName match
            criteria provided.
        """
        self._ensure_activation()

        device = None

        device_list = self.checkout_devices_by_match("modelName", modelName, count=1)
        if len(device_list) > 0:
            device = device_list[0]

        return device

    def checkout_a_device_by_modelNumber(self, modelNumber: str) -> Optional[LandscapeDevice]:
        """
            Checks out a single device from the available pool using the modelNumber match
            criteria provided.
        """
        self._ensure_activation()

        device = None

        device_list = self.checkout_devices_by_match("modelNumber", modelNumber, count=1)
        if len(device_list) > 0:
            device = device_list[0]

        return device

    def checkout_device(self, device: LandscapeDevice):
        """
            Checks out the specified device from the device pool.
        """
        self._ensure_activation()

        self.landscape_lock.acquire()
        try:
            self._locked_checkout_device(device)
        finally:
            self.landscape_lock.release()

        return
    
    def checkout_device_list(self, device_list: List[LandscapeDevice]):
        """
            Checks out the list of specified devices from the device pool.
        """
        self._ensure_activation()

        self.landscape_lock.acquire()
        try:
            for device in device_list:
                self._locked_checkout_device(device)
        finally:
            self.landscape_lock.release()

        return

    def checkout_devices_by_match(self, match_type: str, *match_params, count=None) -> List[LandscapeDevice]:
        """
            Checks out the devices that are found to correspond with the match criteria provided.  If the
            'count' parameter is passed, then the number of devices that are checked out is limited to
            count matching devices.
        """
        self._ensure_activation()

        match_list = None

        self.landscape_lock.acquire()
        try:
            match_list = self.list_available_devices_by_match(match_type, *match_params, count=count)

            for device in match_list:
                self._locked_checkout_device(device)
        finally:
            self.landscape_lock.release()

        return match_list

    def checkout_devices_by_modelName(self, modelName:str , count=None) -> List[LandscapeDevice]:
        """
            Checks out the devices that are found to correspond with the modelName match criteria provided.
            If the 'count' parameter is passed, the the number of devices that are checked out is limited to
            count matching devices.
        """
        self._ensure_activation()

        device_list = self.checkout_devices_by_match("modelName", modelName, count=count)

        return device_list


    def checkout_devices_by_modelNumber(self, modelNumber: str, count=None) -> List[LandscapeDevice]:
        """
            Checks out the devices that are found to correspond with the modelNumber match criteria provided.
            If the 'count' parameter is passed, the the number of devices that are checked out is limited to
            count matching devices.
        """
        self._ensure_activation()

        device_list = self.checkout_devices_by_match("modelNumber", modelNumber, count=count)

        return device_list

    def diagnostic(self, diaglabel: str, diags: dict):
        """
            Can be called in order to perform a diagnostic capture across the test landscape.

            :param diaglabel: The label to use for the diagnostic.
            :param diags: A dictionary of diagnostics to run.
        """
        self._ensure_activation()

        return

    def first_contact(self) -> List[str]:
        """
            The `first_contact` method provides a mechanism for the verification of connectivity with
            enterprise resources that is seperate from the initial call to `establish_connectivity`.

            :returns list: list of failing entities
        """
        error_list = []
        return error_list

    def list_available_devices(self) -> List[LandscapeDevice]:
        """
            Returns the list of devices from the landscape device pool.  This will
            skip any device that has a "skip": true member.
        """
        self._ensure_activation()

        device_list = None

        self.landscape_lock.acquire()
        try:
            device_list = [dev for dev in self._device_pool.values()]
        finally:
            self.landscape_lock.release()

        return device_list

    def list_available_devices_by_match(self, match_type, *match_params, count=None) -> List[LandscapeDevice]:
        """
            Creates and returns a list of devices from the available devices pool that are found
            to correspond to the match criteria provided.  If a 'count' parameter is passed
            then the number of devices returned is limited to count devices.

            .. note:: This API does not perform a checkout of the devices returns so the
                      caller should not consider themselves to the the owner of the devices.
        """
        matching_devices = []
        device_list = self.list_available_devices()

        for dev in device_list:
            if dev.match_using_params(match_type, *match_params):
                matching_devices.append(dev)
                if count is not None and len(matching_devices) >= count:
                    break

        return matching_devices

    def list_devices_by_match(self, match_type, *match_params, count=None) -> List[LandscapeDevice]:
        """
            Creates and returns a list of devices that are found to correspond to the match
            criteria provided.  If a 'count' parameter is passed then the number of devices
            returned is limited to count devices.
        """
        matching_devices = []
        device_list = self.get_devices()

        for dev in device_list:
            if dev.match_using_params(match_type, *match_params):
                matching_devices.append(dev)
                if count is not None and len(matching_devices) >= count:
                    break

        return matching_devices

    def list_devices_by_modelName(self, modelName, count=None) -> List[LandscapeDevice]:
        """
            Creates and returns a list of devices that are found to correspond to the modelName
            match criteria provided.  If a 'count' parameter is passed then the number of devices
            returned is limited to count devices.
        """

        matching_devices = self.list_devices_by_match("modelName", modelName, count=count)

        return matching_devices

    def list_devices_by_modelNumber(self, modelNumber, count=None) -> List[LandscapeDevice]:
        """
            Creates and returns a list of devices that are found to correspond to the modelNumber
            match criteria provided.  If a 'count' parameter is passed then the number of devices
            returned is limited to count devices.
        """

        matching_devices = self.list_devices_by_match("modelNumber", modelNumber, count=count)

        return matching_devices

    def list_devices_from_hint_list(self, hint_list: List[str]) -> List[LandscapeDevice]:
        """
            Creates and returns a list of devices that are found that are matched from the list
            of hints provided.
        """
        matching_devices = []
        device_list = self.get_devices()

        remaining_hints = [hint for hint in hint_list]
        while len(remaining_hints) > 0:
            hint = remaining_hints.pop()

            for dev in device_list:
                if dev.friendly_id.match(hint):
                    matching_devices.append(dev)

        return matching_devices

    def lookup_credential(self, credential_name) -> Union[str, None]:
        """
            Looks up a credential.
        """
        cred_info = None
        
        if credential_name in self._credentials:
            cred_info = self._credentials[credential_name]

        return cred_info

    def lookup_device_by_identity(self, identity: Union[str, FriendlyIdentifier]) -> Optional[LandscapeDevice]:
        """
            Looks up a single device that is found to correspond to the identity.
        """
        found_device = None

        device_list = self.get_devices()
        for device in device_list:
            if device.friendly_id.match(identity):
                found_device = device
                break

        return found_device

    def lookup_device_by_modelName(self, modelName) -> Optional[LandscapeDevice]:
        """
            Looks up a single device that is found to correspond to the modelName match criteria
            provided.
        """
        found_device = None

        matching_devices = self.list_devices_by_match("modelName", modelName, count=1)
        if len(matching_devices) > 0:
            found_device = matching_devices[0]

        return found_device

    def lookup_device_by_modelNumber(self, modelNumber) -> Optional[LandscapeDevice]:
        """
            Looks up a single device that is found to correspond to the modelNumber match criteria
            provided.
        """
        found_device = None

        matching_devices = self.list_devices_by_match("modelNumber", modelNumber, count=1)
        if len(matching_devices) > 0:
            found_device = matching_devices[0]

        return found_device

    def lookup_power_agent(self, power_mapping: dict) -> Union[dict, None]:
        """
            Looks up a power agent by name.
        """
        power_agent = self._power_coord.lookup_agent(power_mapping)
        return power_agent

    def lookup_serial_agent(self, serial_mapping: str) -> Union[dict, None]:
        """
            Looks up a serial agent name.
        """
        serial_agent = self._serial_coordinator.lookup_agent(serial_mapping)
        return serial_agent

    def _activate_power_coordinator(self):
        """
            Initializes the power coordinator according the the information specified in the
            'power' portion of the configuration file.
        """
        pod_info = self._landscape_info["pod"]

        # We need to initialize the power before attempting to initialize any devices, so the
        # devices will be able to lookup serial connections as they are initialized
        if "power" in pod_info:
            coord_config = pod_info["power"]
            self._power_coord = PowerCoordinator(self, coord_config=coord_config)

        return

    def _activate_serial_coordinator(self):
        """
            Initializes the serial coordinator according the the information specified in the
            'serial' portion of the configuration file.
        """
        pod_info = self._landscape_info["pod"]

        # We need to initialize the serial before attempting to initialize any devices, so the
        # devices will be able to lookup serial connections as they are initialized
        if "serial" in pod_info:
            coord_config = pod_info["serial"]
            self._serial_coord = SerialCoordinator(self, coord_config=coord_config)

        return

    def _activate_ssh_coordinator(self, coordinator_constructor):
        """
            Initializes the ssh coordinator according the the information specified in the
            'devices' portion of the configuration file.
        """
        self._has_ssh_devices = True
        self._ssh_coord = coordinator_constructor(self)

        return

    def _activate_upnp_coordinator(self, coordinator_constructor):
        """
            Initializes the upnp coordinator according the the information specified in the
            'devices' portion of the configuration file.
        """

        self._has_upnp_devices = True        
        self._upnp_coord = coordinator_constructor(self)

        return

    def _ensure_activation(self):
        """
            Called by methods that require Landscape activation in order to make sure the 'activate' method
            has been called before the attempted use of the specified method.

            :param method: The name of the method guarding against the use of a Landscape that has not been
                           activated.
        """
        if self._operational_gate is not None:
            self._operational_gate.wait()
        else:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            guarded_method = calframe[1][3]

            errmsg = "The Landscape must be activated before calling the '%s' method." % guarded_method
            raise AKitSemanticError(errmsg) from None

        return
    
    def _establish_connectivity(self, allow_missing_devices: bool = False, allow_unknown_devices: bool = False, upnp_recording: bool = False) -> List[str]:
        """
            The `_establish_connectivity` method provides a mechanism for the verification of connectivity with
            enterprise resources.

            :returns list: list of failing entities
        """

        error_list = []
        connectivity_results = {}

        if self._has_upnp_devices:
            integration_cls = self._integration_points_registered["coordinator/upnp"]
            upnp_error_list, upnp_connectivity_results = integration_cls.establish_connectivity(allow_missing_devices=allow_missing_devices,
                upnp_recording=upnp_recording, allow_unknown_devices=allow_unknown_devices)
            error_list.extend(upnp_error_list)
            connectivity_results.update(upnp_connectivity_results)

        if self._has_ssh_devices:
            integration_cls = self._integration_points_registered["coordinator/ssh"]
            ssh_error_list, ssh_connectivity_results = integration_cls.establish_connectivity(allow_missing_devices=allow_missing_devices)
            error_list.extend(ssh_error_list)
            connectivity_results.update(ssh_connectivity_results)

        self._first_contact_results = connectivity_results

        self._log_scan_results(connectivity_results, )

        return error_list

    def _features_validate(self):
        """
            Validates the device features specified in the landscape configuration file.
        """
        return

    def _internal_activate_device(self, identity):
        """
            Activates a device by copying a reference to the device from the all_devices
            pool to the active_devices and device_pool tables to make the device available
            for active use.
        """
        errmsg = None

        self.landscape_lock.acquire()
        try:
            device = None

            # Add the device to all devices, all devices does not change
            # based on check-out or check-in activity
            if identity in self._all_devices:
                device = self._all_devices[identity]

            if device is not None:
                # Add the device to the device pool, the device pool is used
                # for tracking device availability for check-out
                self._active_devices[identity] = device
                self._device_pool[identity] = device
            else:
                errmsg = "Attempt made to activate an unknown device. identity=%s" % identity

        finally:
            self.landscape_lock.release()

        return errmsg

    def _internal_get_upnp_coord(self):
        """
            Internal method to get a reference to the upnp coordinator.  This provides access
            to the upnp coordinator reference in the middle of activation and bypasses normal
            activation thread synchronization mechanisms.  It should only be used after the upnp
            coordinator has been activated.
        """
        return self._upnp_coord

    def _intenal_scan_activated_devices_for_power(self) -> bool:
        """
            Go through all of the activated device types such as SSH and
            UPNP look for power automation requirements.
        """
        return

    def _intenal_scan_activated_devices_for_serial(self) -> bool:
        """
            Go through all of the activated device types such as SSH and
            UPNP look for power automation requirements.
        """
        return

    def _locked_checkout_device(self, device) -> Optional[LandscapeDevice]:

        rtn_device = None

        identity = device.identity
        if identity not in self._device_pool:
            raise AKitSemanticError("A device is being checked out, that is not in the device pool.") from None

        rtn_device = self._device_pool[identity]

        del self._device_pool[identity]
        self._checked_out_devices[identity] = rtn_device

        return rtn_device

    def _log_device_activation_results(self):

        landscape_first_contact_result_file = os.path.join(get_path_for_output(), "landscape-first-contact-results.json")
        with open(landscape_first_contact_result_file, 'w') as fcrf:
            json.dump(self._first_contact_results, fcrf, indent=4)

        if len(self._activation_errors) > 0:
            errmsg_lines = [
                "Encountered device activation errors.",
                "ACTIVATION ERROR LIST:"
            ]
            for aerror in self._activation_errors:
                errmsg_lines.append("    %s" % aerror)

            errmsg = os.linesep.join(errmsg_lines)
            raise AKitConfigurationError(errmsg) from None

        return
    
    def _log_scan_results(self, scan_results: dict,):
        """
            Logs the results of the device scan.
            :param scan_results: A combined dictionary of scan results.
        """
        log_landscape_scan = self.context.lookup("/environment/behaviors/log-landscape-scan")
        if log_landscape_scan:

            landscape_scan_result_file = os.path.join(get_path_for_output(), "landscape-startup-scan.json")
            with open(landscape_scan_result_file, 'w') as srf:
                json.dump(scan_results, srf, indent=4)

        return

    def _topology_validate(self):
        return