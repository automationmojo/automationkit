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


from typing import List, Optional, Union

import os
import pprint
import shutil
import threading

from akit.exceptions import AKitConfigurationError
from akit.friendlyidentifier import FriendlyIdentifier
from akit.paths import get_filename_for_landscape, get_filename_for_runtime, get_filename_for_topology, get_path_for_output

from akit.xformatting import split_and_indent_lines

from akit.interop.credentials.credentialmanager import CredentialManager

from akit.xfeature import FeatureFilter, FeatureTag, FeatureMask
from akit.interop.landscaping.landscapedescription import LandscapeDescription
from akit.interop.landscaping.landscapedevice import LandscapeDevice
from akit.interop.landscaping.landscapedeviceextension import LandscapeDeviceExtension
from akit.interop.landscaping.topologydescription import TopologyDescription

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
class LandscapeConfigurationLayer:
    """
        The :class:`LandscapeConfigurationLayer` serves as the base layer for the :class:`Landscape` object.  The
        :class:`LandscapeConfigurationLayer` contains the data and method that are initilized as part of the
        initialization of the Landscape object.  It allows access to the processed data pulled from the
        "landscape.yaml" file which details the static declarations for the devices and resources that
        are the landscape file declares.
    """

    landscape_description = LandscapeDescription
    landscape_device = LandscapeDevice
    landscape_device_extension = LandscapeDeviceExtension

    topology_description = TopologyDescription

    _configured_gate = threading.Event()
    _configuring_thread_id = None

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
     
        self._runtime_info = None

        self._has_upnp_devices = False
        self._has_ssh_devices = False

        self._all_devices = {}

        self._credentials = {}

        self._serial_config_lookup_table = {}

        super().__init__()

        return

    @property
    def databases(self) -> dict:
        """
            Returns the database configuration information from the landscape file.
        """
        db_info = self._runtime_info["databases"]
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
    def landscape_info(self):
        """
            Returns the root landscape configuration dictionary.
        """
        return self._landscape_info

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

    def activate_configuration(self):
        """
            Called once at the beginning of the lifetime of a Landscape derived type.  This
            allows the derived types to participate in a customized intialization process.
        """

        lscapeType = type(self)

        lscapeType.landscape_lock.acquire()
        try:

            if lscapeType._configuring_thread_id is None:
                init_thread = threading.current_thread()
                lscapeType._configuring_thread_id = init_thread.ident

                # We don't need to hold the landscape lock while initializing
                # the Landscape because no threads calling the constructor can
                # exit without the landscape initialization being finished.
                lscapeType.landscape_lock.release()

                try:
                    log_to_directory = None

                    log_landscape_declaration = lscapeType.context.lookup("/environment/behaviors/log-landscape-declaration")
                    if log_landscape_declaration:
                        log_to_directory = get_path_for_output()

                    self._load_runtime(log_to_directory=log_to_directory)

                    self._load_landscape(log_to_directory=log_to_directory)

                    self._load_topology(log_to_directory=log_to_directory)

                    self._initialize_landscape()

                    # Set the landscape_initialized even to allow other threads to use the APIs of the Landscape object
                    self._configured_gate.set()

                finally:
                    lscapeType.landscape_lock.acquire()

            else:

                # Don't hold the landscape like while we wait for the
                # landscape to be initialized
                lscapeType.landscape_lock.release()
                try:
                    # Because the landscape is a global singleton and because
                    # we were not the first thread to call the contructor, wait
                    # for the first calling thread to finish initializing the
                    # Landscape before we return and try to use the returned
                    # Landscape reference
                    self._configured_gate.wait()
                finally:
                    lscapeType.landscape_lock.acquire()

        finally:
            lscapeType.landscape_lock.release()

        return

    def get_device_configs(self) -> List[dict]:
        """
            Returns the list of device configurations from the landscape.  This will
            skip any device that has a "skip": true member.
        """
        device_config_list = self._internal_get_device_configs()

        return device_config_list

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

    def get_devices_with_feature(self, feature: Union[FeatureTag, str]) -> List[LandscapeDevice]:
        """
            Returns the list of devices from the landscape.  This will
            skip any device that has a "skip": true member.
        """
        device_list = None

        if isinstance(feature, FeatureTag):
            feature = feature.ID

        self.landscape_lock.acquire()
        try:
            device_list = []
            for dev in self._all_devices.values():
                if dev.has_feature(feature):
                    device_list.append(dev)
        finally:
            self.landscape_lock.release()

        return device_list

    def get_devices_with_feature_mask(self, feature_mask: FeatureMask) -> List[LandscapeDevice]:
        """
            Returns the list of devices from the landscape.  This will
            skip any device that has a "skip": true member.
        """

        all_devices = self.get_devices()

        feature_filter = FeatureFilter(**feature_mask)

        filtered_devices = feature_filter.filter()

        return filtered_devices

    def get_ssh_device_configs(self, exclude_upnp=False) -> List[dict]:
        """
            Returns a list of devices that support ssh.
        """
        ssh_device_config_list = []

        for devinfo in self._internal_get_device_configs():
            dev_type = devinfo["deviceType"]

            if exclude_upnp and dev_type == "network/upnp":
                continue

            if dev_type == "network/ssh":
                ssh_device_config_list.append(devinfo)

        return ssh_device_config_list

    def get_ssh_device_list(self) -> List[dict]:
        """
            Returns a list of SSH devices.
        """

        ssh_device_list = []

        for device in self.get_devices():
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

    def get_upnp_device_list(self) -> List[dict]:
        """
            Returns a list of UPNP devices.
        """

        upnp_device_list = []

        for device in self.get_devices():
            device_type = device.device_type
            if device_type == "network/upnp":
                upnp_device_list.append(device)

        return upnp_device_list

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

    def _create_landscape_device(self, friendly_id: FriendlyIdentifier, dev_type: str, dev_config_info: dict) -> LandscapeDevice:
        device = None

        self.landscape_lock.acquire()
        try:
            identity = friendly_id.identity
            if identity in self._all_devices:
                device = self._all_devices[identity]
            else:
                lscape = self
                device = LandscapeDevice(lscape, friendly_id, dev_type, dev_config_info)
                self._all_devices[identity] = device
        finally:
            self.landscape_lock.release()

        return device

    def _enhance_landscape_device(self, landscape_device, primary_dev_extension):
        return landscape_device

    def _initialize_credentials(self):
        """
        """
        credmgr = CredentialManager()

        self._credentials = credmgr.credentials

        return

    def _initialize_devices(self):

        for dev_config_info in self._internal_get_device_configs():
            dev_type = dev_config_info["deviceType"]
            
            self._initialize_device_of_type(dev_type, dev_config_info)

        return

    def _initialize_device_of_type(self, dev_type: str, dev_config_info: dict):

        if dev_type == "network/upnp":
            upnp_info = dev_config_info["upnp"]

            devhint = None
            if "hint" in upnp_info:
                devhint = upnp_info["hint"]
            elif "USN" in upnp_info:
                devhint = upnp_info["USN"]
                if "hint" not in upnp_info:
                    upnp_info["hint"] = devhint

            fdid = FriendlyIdentifier(devhint, devhint)
            self._create_landscape_device(fdid, dev_type, dev_config_info)
        elif dev_type == "network/ssh":
            devhint = dev_config_info["host"]
            fdid = FriendlyIdentifier(devhint, devhint)
            self._create_landscape_device(fdid, dev_type, dev_config_info)
        else:
            errmsg_lines = [
                "Unknown device type %r in configuration file." % dev_type,
                "DEVICE INFO:"
            ]
            errmsg_lines.extend(split_and_indent_lines(pprint.pformat(dev_config_info, indent=4), 1))

            errmsg = os.linesep.join(errmsg_lines)
            raise AKitConfigurationError(errmsg) from None

        return

    def _initialize_landscape(self):

        self._initialize_credentials()

        # Initialize the devices so we know what they are, this will create a LandscapeDevice object for each device
        # and register it in the all_devices table where it can be found by the device coordinators for further activation
        self._initialize_devices()

        self._topology_overlay()

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
            upnp_info = device_config["upnp"]

            dkey = None
            if "hint" in upnp_info:
                dkey = upnp_info["hint"]
            elif "USN" in upnp_info:
                dkey = upnp_info["USN"]
            else:
                errmsg = "The UPNP configuration error should contain either a 'hint' or 'USN' field."
                raise AKitConfigurationError(errmsg)

            upnp_device_config_table[dkey] = device_config

        return upnp_device_config_table

    def _internal_lookup_device_by_identity(self, identity: str) -> Optional[LandscapeDevice]:
        """
            Looks up a device by identity.
        """

        self.landscape_lock.acquire()
        try:
            device = None
            if identity in self._all_devices:
                device = self._all_devices[identity]
        finally:
            self.landscape_lock.release()

        return device
    
    def _internal_lookup_device_by_hint(self, hint: str) -> Optional[LandscapeDevice]:
        """
            Looks up a device by identity.
        """

        self.landscape_lock.acquire()
        try:
            device = None
            for identity, dev in self._all_devices.items():
                if identity.find(hint) > -1:
                    device = dev
                    break
        finally:
            self.landscape_lock.release()

        return device

    def _load_landscape(self, log_to_directory: Optional[str]=None):

        self._landscape_file = get_filename_for_landscape()

        landscape_desc = self.landscape_description()
        self._landscape_info = landscape_desc.load(self._landscape_file, log_to_directory=log_to_directory)

        if "environment" not in self._landscape_info:
            err_msg = "The landscape file must have an 'environment' decription. (%s)" % self._landscape_file
            raise AKitConfigurationError(err_msg) from None

        self._environment_info = self._landscape_info["environment"]
        if "label" not in self._environment_info:
            err_msg = "The landscape 'environment' decription must have a 'label' member (development, production, test). (%s)" % self._landscape_file
            raise AKitConfigurationError(err_msg) from None

        return

    def _load_runtime(self, log_to_directory: Optional[str]=None):

        lscapeType = type(self)

        if log_to_directory is not None:
            # Log the runtime file used to startup the landscape configuration
            runtime_file = get_filename_for_runtime()
            if os.path.exists(runtime_file):
                runtime_basename = os.path.basename(runtime_file)
                runtime_logged_file = os.path.join(log_to_directory, runtime_basename)

                shutil.copy(runtime_file, runtime_logged_file)

        self._runtime_info = lscapeType.context.lookup("/configuration")

        return

    def _load_topology(self, log_to_directory: Optional[str]=None):
        """
            Loads the topology file.
        """

        self._topology_file = get_filename_for_topology()

        topology_desc = self.topology_description()
        self._topology_info = topology_desc.load(self._topology_file, log_to_directory=log_to_directory)

        return

    def _topology_overlay(self):
        return

    def _topology_validate_specification(self, topology_info):
        return