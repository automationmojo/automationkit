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

from typing import List, Optional

import inspect
import json
import os
import threading

from akit.exceptions import AKitConfigurationError, AKitSemanticError

from akit.paths import get_path_for_output

from akit.interop.coordinators.powercoordinator import PowerCoordinator
from akit.interop.coordinators.serialcoordinator import SerialCoordinator

from akit.interop.landscaping.landscapedevice import LandscapeDevice

class LandscapeOperationalLayer:
    """
    """

    _operational_gate = None

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