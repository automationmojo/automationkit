"""
.. module:: landscape
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

from os.path import basename
from typing import List, Optional, Union

import copy
import inspect
import json
import os
import shutil
import threading
import traceback
import yaml

import pprint

from akit.compat import import_by_name

from akit.environment.variables import AKIT_VARIABLES
from akit.environment.context import Context

from akit.exceptions import AKitConfigurationError, AKitRuntimeError, AKitSemanticError

from akit.paths import get_expanded_path, get_path_for_output

from akit.xformatting import split_and_indent_lines
from akit.xlogging.foundations import getAutomatonKitLogger

from akit.integration.credentials.credentialmanager import CredentialManager

from akit.integration.coordinators.powercoordinator import PowerCoordinator
from akit.integration.coordinators.serialcoordinator import SerialCoordinator

from akit.integration.landscaping.landscapedescription import LandscapeDescription
from akit.integration.landscaping.landscapedevice import LandscapeDevice
from akit.integration.landscaping.landscapedeviceextension import LandscapeDeviceExtension
from akit.integration.landscaping.topologydescription import TopologyDescription

PASSWORD_MASK = "(hidden)"

def mask_passwords (context):
    """
        Takes a dictionary context object and will recursively mask any password members found
        in the dictionary.
    """
    for key, val in context.items():
        if (key == "password" or key == "secret"):
            context[key] = PASSWORD_MASK

        if isinstance(val, dict):
            mask_passwords(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    mask_passwords(item)

    return

def filter_credentials(device_info, credential_lookup, category):
    """
        Looks up the credentials associated with a device and returns the credentials found
        that match a given category.

        :param device_info: Device information dictionary with credential names to reference.
        :param credential_lookup: A credential lookup dictionary that is used to convert credential
                                  names into credential objects loaded from the landscape.
        :param category: The category of credentials to return when filtering credentials.
    """
    cred_found_list = []

    cred_name_list = device_info["credentials"]
    for cred_name in cred_name_list:
        if cred_name in credential_lookup:
            credential = credential_lookup[cred_name]
            if credential.category == category:
                cred_found_list.append(credential)
        else:
            error_lines = [
                "The credential '{}' was not found in the credentials list.",
                "DEVICE:"
            ]

            dev_repr_lines = pprint.pformat(device_info, indent=4).splitlines(False)
            for dline in dev_repr_lines:
                error_lines.append("    " + dline)

            error_lines.append("CREDENTIALS:")
            cred_available_list = [cname for cname in credential_lookup.keys()]
            cred_available_list.sort()
            for cred_avail in cred_available_list:
                error_lines.append("    " + cred_avail)

            errmsg = os.linesep.join(error_lines)
            raise AKitConfigurationError(errmsg) from None

    return cred_found_list

# ====================================================================================
#
#                                     CONFIGURATION LAYER
#
# ====================================================================================
class _LandscapeConfigurationLayer:
    """
        The :class:`LandscapeConfigurationLayer` serves as the base layer for the :class:`Landscape` object.  The
        :class:`LandscapeConfigurationLayer` contains the data and method that are initilized as part of the
        initialization of the Landscape object.  It allows access to the processed data pulled from the
        "landscape.yaml" file which details the static declarations for the devices and resources that
        are the landscape file declares.
    """
    context = Context()

    logger = getAutomatonKitLogger()
    landscape_lock = threading.RLock()

    landscape_description = LandscapeDescription
    landscape_device = LandscapeDevice
    landscape_device_extension = LandscapeDeviceExtension

    topology_description = TopologyDescription

    _configured_gate = None

    def __init__(self):
        """
            The :class:`LandscapeConfigurationLayer` object should not be instantiated directly.
        """
        self._landscape_info = None
        self._landscape_file = None

        self._topology_info = None
        self._topology_file = None

        self._environment_info = None
        self._environment_label = None
        self._environment_muse = None
     
        self._runtime_info = None

        self._has_muse_devices = False
        self._has_upnp_devices = False
        self._has_ssh_devices = False

        self._all_devices = {}

        self._credentials = {}

        self._serial_config_lookup_table = {}

        self._initialize()
        return

    @property
    def databases(self) -> dict:
        """
            Returns the database configuration information from the landscape file.
        """
        db_info = self.landscape_info["databases"]
        return db_info

    @property
    def credentials(self) -> dict:
        return self._credentials

    @property
    def environment(self) -> dict:
        """
            Returns the environment section of the landscape configuration.
        """
        return self._environment_info

    @property
    def environment_label(self) -> str:
        """
            Returns the environment.label section of the landscape configuration.
        """
        return self._environment_label

    @property
    def environment_muse(self) -> dict:
        """
            Returns the environment.muse section of the landscape configuration or None.
        """
        return self._environment_muse

    @property
    def landscape_info(self):
        """
            Returns the root landscape configuration dictionary.
        """
        return self._landscape_info

    @property
    def has_muse_devices(self) -> bool:
        """
            Returns a boolean indicating if the landscape contains muse devices.
        """
        return self._has_muse_devices

    @property
    def has_ssh_devices(self) -> bool:
        """
            Returns a boolean indicating if the landscape contains ssh devices.
        """
        return self._has_ssh_devices

    @property
    def has_upnp_devices(self) -> bool:
        """
            Returns a boolean indicating if the landscape contains upnp devices.
        """
        return self._has_upnp_devices

    @property
    def name(self) -> str:
        """
            Returns the name associated with the landscape.
        """
        lname = None
        if "name" in self.landscape_info:
            lname = self.landscape_info["name"]
        return lname

    @property
    def networking(self) -> dict:
        """
            Returns the configuration/networking section of the runtime configuration.
        """
        netinfo = None
        if "networking" in self._runtime_info:
            netinfo = self._runtime_info["networking"]
        return netinfo

    def get_devices(self) -> List[LandscapeDevice]:
        """
            Returns the list of devices from the landscape.  This will
            skip any device that has a "skip": true member.
        """
        device_list = None

        self.landscape_lock.acquire()
        try:
            device_list = [dev for dev in self._all_devices.values()]
        finally:
            self.landscape_lock.release()

        return device_list

    def get_device_configs(self) -> List[dict]:
        """
            Returns the list of device configurations from the landscape.  This will
            skip any device that has a "skip": true member.
        """
        device_config_list = self._internal_get_device_configs()

        return device_config_list

    def get_muse_device_configs(self, exclude_upnp=False) -> List[dict]:
        """
            Returns a list of devices that support Sonos muse protocol.
        """
        muse_device_config_list = []

        for devinfo in self._internal_get_device_configs():
            dev_type = devinfo["deviceType"]

            if exclude_upnp and dev_type == "network/upnp":
                continue

            if "muse" in devinfo:
                muse_device_config_list.append(devinfo)

        return muse_device_config_list

    def get_ssh_device_configs(self, exclude_upnp=False) -> List[dict]:
        """
            Returns a list of devices that support ssh.
        """
        ssh_device_config_list = []

        for devinfo in self._internal_get_device_configs():
            dev_type = devinfo["deviceType"]

            if exclude_upnp and dev_type == "network/upnp":
                continue

            if "ssh" in devinfo:
                ssh_device_config_list.append(devinfo)

        return ssh_device_config_list

    def get_ssh_device_list(self) -> List[dict]:
        """
            Returns a list of SSH devices.
        """

        ssh_device_list = []

        for device in self._all_devices.values():
            device_type = device.device_type
            if device_type == "network/ssh":
                ssh_device_list.append(device)
            elif device_type == "network/upnp":
                if device.has_ssh_credential:
                    ssh_device_list.append(device)

        return ssh_device_list

    def get_upnp_device_configs(self, ssh_only=False) -> List[dict]:
        """
            Returns a list of UPNP device information dictionaries.
        """
        upnp_device_config_list = self._internal_get_upnp_device_configs(ssh_only=ssh_only)

        return upnp_device_config_list

    def get_upnp_device_config_lookup_table(self) -> dict:
        """
            Returns a USN lookup table for upnp devices.
        """
        upnp_device_table = self._internal_get_upnp_device_config_lookup_table()

        return upnp_device_table

    def get_serial_config(self, serial_service_name: str):
        """
            Looks up the configuration dictionary for the serial service specified.
        """
        serial_config = None

        pod_config = self._landscape_info["pod"]

        if "serial" in pod_config:
            if self._serial_config_lookup_table is not None:
                serial_config_lookup_table = self._serial_config_lookup_table
            else:
                serial_config_lookup_table = {}

                serial_config_list = pod_config["serial"]
                for serial_config in serial_config_list:
                    cfgname = serial_config["name"]
                    serial_config_lookup_table[cfgname] = serial_config

            if serial_service_name in self._serial_config_lookup_table:
                serial_config = self._serial_config_lookup_table[serial_service_name]

        return serial_config

    def _create_landscape_device(self, keyid: str, dev_type: str, dev_config_info: dict):
        device = None

        self.landscape_lock.acquire()
        try:
            if keyid in self._all_devices:
                device = self._all_devices[keyid]
            else:
                device = LandscapeDevice(self, keyid, dev_type, dev_config_info)
                self._all_devices[keyid] = device
        finally:
            self.landscape_lock.release()

        return device

    def _enhance_landscape_device(self, landscape_device, primary_dev_extension):
        return landscape_device

    def _initialize(self):
        """
            Called by '__init__' once at the beginning of the lifetime of a Landscape derived
            type.  This allows the derived types to participate in a customized intialization
            process.
        """

        context = Context()

        self._runtime_info = context.lookup("/environment/configuration")

        log_landscape_declaration = context.lookup("/environment/behaviors/log-landscape-declaration")

        try:
            self._landscape_file = get_expanded_path(context.lookup("/environment/configuration/paths/landscape"))

            lscape_desc = self.landscape_description()
            self._landscape_info = lscape_desc.load(self._landscape_file)
        except AKitConfigurationError:
            raise
        except Exception as xcpt:
            err_msg = "Error loading the landscape file from (%s)%s%s" % (
                self._landscape_file, os.linesep, traceback.format_exc())
            raise AKitConfigurationError(err_msg) from xcpt

        try:
            if log_landscape_declaration:
                results_dir = get_path_for_output()

                landscape_file_basename = os.path.basename(self._landscape_file)
                landscape_file_basename, landscape_file_ext = os.path.splitext(landscape_file_basename)

                landscape_file_copy = os.path.join(results_dir, "{}-declared{}".format(landscape_file_basename, landscape_file_ext))
                shutil.copy2(self._landscape_file, landscape_file_copy)

                # Create a json copy of the landscape file until the time when we can
                # parse yaml in the test summary javascript.
                landscape_info_copy = copy.deepcopy(self._landscape_info)

                landscape_file_copy = os.path.join(results_dir, "{}-declared{}".format(landscape_file_basename, ".json"))
                with open(landscape_file_copy, 'w') as lsf:
                    json.dump(landscape_info_copy, lsf, indent=4)
        except Exception as xcpt:
            err_msg = "Error while logging the landscape file (%s)%s%s" % (
                self._landscape_file, os.linesep, traceback.format_exc())
            raise AKitRuntimeError(err_msg) from xcpt

        try:
            self._topology_file = get_expanded_path(context.lookup("/environment/configuration/paths/topology"))

            topology_desc = self.topology_description()
            self._topology_info = topology_desc.load(self._topology_file)
        except AKitConfigurationError:
            raise
        except Exception as xcpt:
            err_msg = "Error loading the topology file from (%s)%s%s" % (
                self._topology_file, os.linesep, traceback.format_exc())
            raise AKitConfigurationError(err_msg) from xcpt

        try:
            topology_file_basename = os.path.basename(self._topology_file)
            topology_file_basename, topology_file_ext = os.path.splitext(topology_file_basename)

            topology_file_copy = os.path.join(results_dir, "{}-declared{}".format(topology_file_basename, topology_file_ext))
            shutil.copy2(self._topology_file, topology_file_copy)
        except Exception as xcpt:
            err_msg = "Error while logging the topology file (%s)%s%s" % (
                self._topology_file, os.linesep, traceback.format_exc())
            raise AKitRuntimeError(err_msg) from xcpt

        if "environment" not in self._landscape_info:
            err_msg = "The landscape file must have an 'environment' decription. (%s)" % self._landscape_file
            raise AKitConfigurationError(err_msg) from None

        self._environment_info = self._landscape_info["environment"]
        if "label" not in self._environment_info:
            err_msg = "The landscape 'environment' decription must have a 'label' member (development, production, test). (%s)" % self._landscape_file
            raise AKitConfigurationError(err_msg) from None

        self._environment_label = self._environment_info["label"]

        if "muse" in self._environment_info:
            self._environment_muse = self._environment_info["muse"]
            if ("authhost" not in self._environment_muse) or ("ctlhost" not in self._environment_muse) or ("version" not in self._environment_muse):
                err_msg = "The landscape 'environment/muse' decription must have both a 'envhost' and 'version' members. (%s)" % self._landscape_file
                raise AKitConfigurationError(err_msg) from None

        self._initialize_credentials()

        # Initialize the devices so we know what they are, this will create a LandscapeDevice object for each device
        # and register it in the all_devices table where it can be found by the device coordinators for further activation
        self._initialize_devices()

        # Set the landscape_initialized even to allow other threads to use the APIs of the Landscape object
        self._configured_gate.set()

        return

    def _initialize_credentials(self):
        """
        """
        credmgr = CredentialManager()

        self._credentials = credmgr.credentials
        return

    def _initialize_devices(self):

        for dev_config_info in self._internal_get_device_configs():
            dev_type = dev_config_info["deviceType"]
            keyid = None
            device = NotImplemented
            if dev_type == "network/upnp":
                upnp_info = dev_config_info["upnp"]
                keyid = upnp_info["USN"]
                device = LandscapeDevice(self, keyid, dev_type, dev_config_info)
            elif dev_type == "network/ssh":
                keyid = dev_config_info["host"]
                device = LandscapeDevice(self, keyid, dev_type, dev_config_info)
            else:
                errmsg_lines = [
                    "Unknown device type %r in configuration file." % dev_type,
                    "DEVICE INFO:"
                ]
                errmsg_lines.extend(split_and_indent_lines(pprint.pformat(dev_config_info, indent=4), 1))

                errmsg = os.linesep.join(errmsg_lines)
                raise AKitConfigurationError(errmsg) from None
            
            if keyid not in self._all_devices:
                self._all_devices[keyid] = device
            else:
                errmsg_lines = [
                    "Devices found with duplicate identifiers.",
                    "FIRST DEVICE:"
                ]
                errmsg_lines.extend(split_and_indent_lines(pprint.pformat(self._all_devices[keyid], indent=4), 1))
                errmsg_lines.append("DUPLICATE DEVICE:")
                errmsg_lines.extend(split_and_indent_lines(pprint.pformat(dev_config_info, indent=4), 1))

                errmsg = os.linesep.join(errmsg_lines)
                raise AKitConfigurationError(errmsg) from None

        return

    def _internal_get_device_configs(self) -> List[dict]:
        """
            Returns the list of devices from the landscape.  This will
            skip any device that has a "skip": true member.

            .. note:: The _internal_ methods do not guard against calls prior to
            landscape initialization so they should only be called with care.  This
            should not be called until after the _landscape_info variable has been
            loaded and contains the configuration data from the landscape.yaml file.
        """

        device_config_list = []

        self.landscape_lock.acquire()
        try:
            pod_info = self._landscape_info["pod"]
            for dev_config_info in pod_info["devices"]:
                if "skip" in dev_config_info and dev_config_info["skip"]:
                    continue
                device_config_list.append(dev_config_info)
        finally:
            self.landscape_lock.release()

        return device_config_list

    def _internal_get_ssh_device_configs(self) -> List[dict]:
        """
            Returns a list of SSH device information dictionaries.
        """

        ssh_device_config_list = []

        for device_config in self._internal_get_device_configs():
            dev_type = device_config["deviceType"]

            if dev_type == "network/ssh":
                ssh_device_config_list.append(device_config)

        return ssh_device_config_list

    def _internal_get_upnp_device_configs(self, ssh_only=False) -> List[dict]:
        """
            Returns a list of UPNP device information dictionaries.
        """

        upnp_device_config_list = []

        for device_config in self._internal_get_device_configs():
            dev_type = device_config["deviceType"]

            if dev_type != "network/upnp":
                continue

            if ssh_only and "ssh" in device_config:
                upnp_device_config_list.append(device_config)
            else:
                upnp_device_config_list.append(device_config)

        return upnp_device_config_list

    def _internal_get_upnp_device_list(self) -> List[dict]:
        """
            Returns a list of UPNP devices.
        """

        upnp_device_list = []

        for device in self._all_devices.values():
            if device.device_type == "network/upnp":
                upnp_device_list.append(device)

        return upnp_device_list

    
    def _internal_get_upnp_device_config_lookup_table(self) -> dict:
        """
            Returns a USN lookup table for upnp devices.

            .. note:: The _internal_ methods do not guard against calls prior to
            landscape initialization so they should only be called with care.  This
            should not be called until after the _landscape_info variable has been
            loaded and contains the configuration data from the landscape.yaml file.
        """

        upnp_device_config_list = self._internal_get_upnp_device_configs()

        upnp_device_config_table = {}
        for device_config in upnp_device_config_list:
            usn = device_config["upnp"]["USN"]
            upnp_device_config_table[usn] = device_config

        return upnp_device_config_table

    def _internal_lookup_device_by_keyid(self, keyid) -> Optional[LandscapeDevice]:
        """
            Looks up a device by keyid.
        """

        self.landscape_lock.acquire()
        try:
            device = None
            if keyid in self._all_devices:
                device = self._all_devices[keyid]
        finally:
            self.landscape_lock.release()

        return device


# ====================================================================================
#
#                                   ACTIVATION LAYER
#
# ====================================================================================

class _LandscapeActivationLayer(_LandscapeConfigurationLayer):
    """

    """

    _activated_gate = None

    def __init__(self):
        _LandscapeConfigurationLayer.__init__(self)

        self._ordered_roles = []

        self._integration_points_registered = {}

        self._integration_point_registration_counter = 0

        # We need to wait till we have initialized the landscape configuration
        # layer before we start registering integration points
        self.landscape_description.register_integration_points(self)

        return
    

    def register_integration_point(self, role: str, coupling: type):
        """
            This method should be called from the attach_to_environment methods from individual couplings
            in order to register the base level integrations.  Integrations can be hierarchical so it
            is only necessary to register the root level integration couplings, the descendant couplings can
            be called from the root level couplings.

            :param role: The name of a role to assign for a coupling.
            :param coupling: The coupling to register for the associated role.
        """
        thisType = type(self)

        self.landscape_lock.acquire()
        try:
            if role not in self._integration_points_registered:
                self._ordered_roles.append(role)
                self._integration_points_registered[role] = coupling

                self._integration_point_registration_counter += 1
            else:
                raise AKitSemanticError("A coupling with the role %r was already registered." % role) from None
        finally:
            self.landscape_lock.release()

        return

    def transition_to_activation(self):
        """
            Called in order to mark the configuration process as complete in order
            for the activation stage to begin and to make the activation level methods
            callable.
        """
        self._landscape_configured = True
        return

    
# ====================================================================================
#
#                               OPERATIONAL LAYER
#
# ====================================================================================

class _LandscapeOperationalLayer(_LandscapeActivationLayer):
    """

    """

    _operational_gate = None

    def __init__(self):
        _LandscapeActivationLayer.__init__(self)

        self._power_coord = None
        self._serial_coord = None

        self._muse_coord = None
        self._upnp_coord = None
        self._ssh_coord = None

        self._active_devices = {}

        self._device_pool = {}

        self._activation_errors = []

        self._first_contact_results = None

        self._integration_points_activated = {}
        self._integration_point_activation_counter = 0

        return

    @property
    def muse_coord(self):
        """
            Returns a the :class:`MuseCoordinator` that is used to manage muse devices.
        """
        self._ensure_activation()
        return self._muse_coord

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

    def transition_to_operational(self, allow_missing_devices: bool = False, upnp_recording: bool = False):

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

                    self._establish_connectivity(allow_missing_devices=allow_missing_devices, upnp_recording=upnp_recording)

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

    def _internal_activate_device(self, keyid):
        """
            Activates a device by copying a reference to the device from the all_devices
            pool to the active_devices and device_pool tables to make the device available
            for active use.
        """
        errmsg = None

        self.landscape_lock.acquire()
        try:
            # Add the device to all devices, all devices does not change
            # based on check-out or check-in activity
            if keyid in self._all_devices:
                device = self._all_devices[keyid]

            if device is not None:
                # Add the device to the device pool, the device pool is used
                # for tracking device availability for check-out
                self._active_devices[keyid] = device
                self._device_pool[keyid] = device
            else:
                errmsg = "Attempt made to activate an unknown device. keyid=%s" % keyid

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

        keyid = device.keyid
        if keyid not in self._device_pool:
            raise AKitSemanticError("A device is being checked out, that is not in the device pool.") from None

        rtn_device = self._device_pool[keyid]
        del self._device_pool[keyid]

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
        context = Context()
        log_landscape_scan = context.lookup("/environment/behaviors/log-landscape-scan")
        if log_landscape_scan:

            landscape_scan_result_file = os.path.join(get_path_for_output(), "landscape-startup-scan.json")
            with open(landscape_scan_result_file, 'w') as srf:
                json.dump(scan_results, srf, indent=4)

        return


class Landscape(_LandscapeOperationalLayer):
    """
        The base class for all derived :class:`Landscape` objects.  The :class:`Landscape`
        object is a singleton object that provides access to the resources and test
        environment level methods.
    """

    _landscape_type = None
    _instance = None

    def __new__(cls):
        """
            Constructs new instances of the Landscape object from the :class:`Landscape`
            type or from a derived type that is found in the module specified in the
            :module:`akit.environment.variables` module or by setting the
            'AKIT_LANDSCAPE_MODULE' environment variable.
        """
        if cls._instance is None:
            if cls._landscape_type is None:
                cls._instance = super(Landscape, cls).__new__(cls)
            else:
                cls._instance = super(Landscape, cls._landscape_type).__new__(cls._landscape_type)
            # Put any initialization here.
        return cls._instance

    def __init__(self):
        """
            Creates an instance or reference to the :class:`Landscape` singleton object.  On the first call to this
            constructor the :class:`Landscape` object is initialized and the landscape configuration is loaded.
        """

        thisType = type(self)

        self.landscape_lock.acquire()
        try:

            if thisType._configured_gate is None:
                thisType._configured_gate = threading.Event()
                thisType._configured_gate.clear()

                # We don't need to hold the landscape lock while initializing
                # the Landscape because no threads calling the constructor can
                # exit without the landscape initialization being finished.
                self.landscape_lock.release()

                try:
                    _LandscapeOperationalLayer.__init__(self)
                finally:
                    self.landscape_lock.acquire()

            else:

                # Don't hold the landscape like while we wait for the
                # landscape to be initialized
                self.landscape_lock.release()
                try:
                    # Because the landscape is a global singleton and because
                    # we were not the first thread to call the contructor, wait
                    # for the first calling thread to finish initializing the
                    # Landscape before we return and try to use the returned
                    # Landscape reference
                    self._configured_gate.wait()
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

        keyid = device.keyid

        self.landscape_lock.acquire()
        try:
            self._device_pool[keyid] = device
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

    def lookup_credential(self, credential_name) -> Union[str, None]:
        """
            Looks up a credential.
        """
        cred_info = None
        
        if credential_name in self._credentials:
            cred_info = self._credentials[credential_name]

        return cred_info

    def lookup_device_by_keyid(self, keyid) -> Optional[LandscapeDevice]:
        """
            Looks up a single device that is found to correspond to the keyid.
        """
        found_device = None

        device_list = self.get_devices()
        for device in device_list:
            if device.keyid == keyid:
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


def is_subclass_of_landscape(cand_type):
    """
        Returns a boolean value indicating if the candidate type is a subclass
        of :class:`Landscape`.
    """
    is_scol = False
    if inspect.isclass(cand_type) and issubclass(cand_type, Landscape):
        is_scol = True
    return is_scol

def load_and_set_landscape_type(lscape_module):
    """
        Scans the module provided for :class:`Landscape` derived classes and will
        take the first one and assign it as the current runtime landscape type.
    """
    class_items = inspect.getmembers(lscape_module, is_subclass_of_landscape)
    for _, cls_type in class_items:
        type_module_name = cls_type.__module__
        if type_module_name == lscape_module.__name__:
            Landscape._landscape_type = cls_type # pylint: disable=protected-access
            break
    return

if AKIT_VARIABLES.AKIT_LANDSCAPE_MODULE is not None:
    lscape_module_override = import_by_name(AKIT_VARIABLES.AKIT_LANDSCAPE_MODULE)
    load_and_set_landscape_type(lscape_module_override )
    check_landscape = Landscape()
