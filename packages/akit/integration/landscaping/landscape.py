"""
.. module:: landscape
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`TestLandscape` class and associated diagnostic.

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
import threading
import traceback
import yaml

import pprint

from akit.compat import import_by_name

from akit.environment.variables import VARIABLES
from akit.environment.context import Context

from akit.exceptions import AKitConfigurationError, AKitSemanticError
from akit.integration.credentials.basiccredential import BasicCredential

from akit.paths import get_expanded_path, get_path_for_output


from akit.xformatting import split_and_indent_lines
from akit.xlogging.foundations import getAutomatonKitLogger

from akit.integration.coordinators.powercoordinator import PowerCoordinator
from akit.integration.credentials.musecredential import MuseCredential
from akit.integration.credentials.sshcredential import SshCredential
from akit.integration.landscaping.landscapedescription import LandscapeDescription
from akit.integration.landscaping.landscapedevice import LandscapeDevice
from akit.integration.landscaping.landscapedeviceextension import LandscapeDeviceExtension

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
            raise AKitConfigurationError(errmsg)

    return cred_found_list

class Landscape:
    """
        The base class for all derived :class:`Landscape` objects.  The :class:`Landscape`
        object is a singleton object that provides access to the resources and test
        environment level methods.
    """
    landscape_description = LandscapeDescription
    landscape_device = LandscapeDevice
    landscape_device_extension = LandscapeDeviceExtension

    landscape_lock = threading.RLock()
    landscape_initialized = threading.Event()

    _landscape_type = None
    _instance = None
    _initialized = False

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

            if not thisType._initialized:
                thisType._initialized = True

                self._landscape_info = None
                self._landscape_file = None

                self._environment_info = None
                self._environment_label = None
                self._environment_muse = None

                self._logger = getAutomatonKitLogger()

                self._has_muse_devices = False
                self._has_upnp_devices = False
                self._has_ssh_devices = False

                self._muse_coord = None
                self._upnp_coord = None
                self._ssh_coord = None

                self._all_devices = {}

                self._device_pool = {}

                self._credentials = {}

                self._serial_config_lookup_table = {}

                self._power_coordinator = None
                self._serial_coordinator = None

                self._initialize()
        finally:
            self.landscape_lock.release()

        return

    @property
    def credentials(self) -> dict:
        self.landscape_initialized.wait()
        return self._credentials

    @property
    def environment(self) -> dict:
        """
            Returns the environment section of the landscape configuration.
        """
        self.landscape_initialized.wait()
        return self._environment_info

    @property
    def environment_label(self) -> str:
        """
            Returns the environment.label section of the landscape configuration.
        """
        self.landscape_initialized.wait()
        return self._environment_label

    @property
    def environment_muse(self) -> dict:
        """
            Returns the environment.muse section of the landscape configuration or None.
        """
        self.landscape_initialized.wait()
        return self._environment_muse

    @property
    def name(self) -> str:
        """
            Returns the name associated with the landscape.
        """
        self.landscape_initialized.wait()
        lname = None
        if "name" in self.landscape_info:
            lname = self.landscape_info["name"]
        return lname

    @property
    def has_muse_devices(self) -> bool:
        """
            Returns a boolean indicating if the landscape contains muse devices.
        """
        self.landscape_initialized.wait()
        return self._has_muse_devices

    @property
    def has_ssh_devices(self) -> bool:
        """
            Returns a boolean indicating if the landscape contains ssh devices.
        """
        self.landscape_initialized.wait()
        return self._has_ssh_devices

    @property
    def has_upnp_devices(self) -> bool:
        """
            Returns a boolean indicating if the landscape contains upnp devices.
        """
        self.landscape_initialized.wait()
        return self._has_upnp_devices

    @property
    def landscape_info(self):
        """
            Returns the root landscape configuration dictionary.
        """
        self.landscape_initialized.wait()
        return self._landscape_info

    @property
    def muse_coord(self):
        """
            Returns a the :class:`MuseCoordinator` that is used to manage muse devices.
        """
        self.landscape_initialized.wait()
        return self._muse_coord

    @property
    def ssh_coord(self):
        """
            Returns a the :class:`SshPoolCoordinator` that is used to manage ssh devices.
        """
        self.landscape_initialized.wait()
        return self._ssh_coord

    @property
    def upnp_coord(self):
        """
            Returns a the :class:`UpnpCoordinator` that is used to manage upnp devices.
        """
        self.landscape_initialized.wait()
        return self._upnp_coord

    @property
    def databases(self) -> dict:
        """
            Returns the database configuration information from the landscape file.
        """
        self.landscape_initialized.wait()
        db_info = self.landscape_info["databases"]
        return db_info

    def checkin_device(self, device: LandscapeDevice):
        """
            Returns a landscape device to the the available device pool.
        """
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
        device = None

        device_list = self.checkout_devices_by_match("modelNumber", modelNumber, count=1)
        if len(device_list) > 0:
            device = device_list[0]

        return device

    def checkout_devices_by_match(self, match_type: str, *match_params, count=None) -> List[LandscapeDevice]:
        """
            Checks out the devices that are found to correspond with the match criteria provided.  If the
            'count' parameter is passed, then the number of devices that are checked out is limited to
            count matching devices.
        """
        self.landscape_initialized.wait()

        device_list = None

        self.landscape_lock.acquire()
        try:
            device_list = self.list_available_devices_by_match(match_type, *match_params, count=count)

            for device in device_list:
                self._locked_checkout_device(device)
        finally:
            self.landscape_lock.release()

        return device_list

    def checkout_devices_by_modelName(self, modelName:str , count=None) -> List[LandscapeDevice]:
        """
            Checks out the devices that are found to correspond with the modelName match criteria provided.
            If the 'count' parameter is passed, the the number of devices that are checked out is limited to
            count matching devices.
        """

        device_list = self.checkout_devices_by_match("modelName", modelName, count=count)

        return device_list


    def checkout_devices_by_modelNumber(self, modelNumber: str, count=None) -> List[LandscapeDevice]:
        """
            Checks out the devices that are found to correspond with the modelNumber match criteria provided.
            If the 'count' parameter is passed, the the number of devices that are checked out is limited to
            count matching devices.
        """

        device_list = self.checkout_devices_by_match("modelNumber", modelNumber, count=count)

        return device_list

    def diagnostic(self, diaglabel: str, diags: dict): # pytest: disable=unused-argument
        """
            Can be called in order to perform a diagnostic capture across the test landscape.

            :param diaglabel: The label to use for the diagnostic.
            :param diags: A dictionary of diagnostics to run.
        """
        self.landscape_initialized.wait()
        return

    def first_contact(self) -> List[str]:
        """
            This method should be called as early as possible in order to ensure the entities in the
            automation landscape exist and the authentication credentials provided for these entities
            are valid and usable to interact with these entities.

            :returns list: list of failing entities
        """
        self.landscape_initialized.wait()

        error_lists = []

        if self._has_upnp_devices and self._upnp_coord is None:
            raise AKitConfigurationError("UpnpCoordinator initialization failure.")

        if self._has_ssh_devices and self._ssh_coord is None:
            raise AKitConfigurationError("SshPoolCoordinator initialization failure.")

        available_upnp_devices = self.get_upnp_device_configs(ssh_only=True)
        available_ssh_devices = self.get_ssh_device_configs(exclude_upnp=True)

        self._logger.info("===================== Initiating SSH First Contact with Landscape Devices =====================")
        self._logger.info("")

        if len(available_upnp_devices) == 0 and len(available_ssh_devices) == 0:
            self._logger.info("No SSH Devices Found...")

        if len(available_upnp_devices) > 0:
            self._logger.info("UPNP DEVICES:")
            for devinfo in available_upnp_devices:
                usn = devinfo["upnp"]["USN"]
                ldev = self._ssh_coord.lookup_device_by_usn(usn)
                if ldev is not None:
                    agent = ldev.ssh
                    self._logger.info("    Verifying USN={} HOST={} IP={}".format(usn, agent.host, agent.ipaddr))
                    if not agent.verify_connectivity():
                        error_lists.append(devinfo)
            self._logger.info("")

        if len(available_ssh_devices) > 0:
            self._logger.info("SSH DEVICES:")
            for devinfo in available_ssh_devices:
                sshinfo = devinfo["ssh"]
                host = sshinfo["host"]
                agent = self._ssh_coord.lookup_device_by_host(host)
                self._logger.info("    Verifying HOST={} IP={}".format(agent.host, agent.ipaddr))
                if not agent.verify_connectivity():
                    error_lists.append(devinfo)
            self._logger.info("")

        return error_lists

    def get_available_devices(self) -> List[LandscapeDevice]:
        """
            Returns the list of devices from the landscape device pool.  This will
            skip any device that has a "skip": true member.
        """
        self.landscape_initialized.wait()

        device_list = None

        self.landscape_lock.acquire()
        try:
            device_list = [dev for dev in self._device_pool.values()]
        finally:
            self.landscape_lock.release()

        return device_list

    def get_devices(self) -> List[LandscapeDevice]:
        """
            Returns the list of devices from the landscape.  This will
            skip any device that has a "skip": true member.
        """
        self.landscape_initialized.wait()

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
        self.landscape_initialized.wait()

        device_config_list = self._internal_get_device_configs()

        return device_config_list

    def get_muse_device_configs(self, exclude_upnp=False) -> List[dict]:
        """
            Returns a list of devices that support Sonos muse protocol.
        """
        self.landscape_initialized.wait()

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
        self.landscape_initialized.wait()

        ssh_device_config_list = []

        for devinfo in self._internal_get_device_configs():
            dev_type = devinfo["deviceType"]

            if exclude_upnp and dev_type == "network/upnp":
                continue

            if "ssh" in devinfo:
                ssh_device_config_list.append(devinfo)

        return ssh_device_config_list

    def get_upnp_device_configs(self, ssh_only=False) -> List[dict]:
        """
            Returns a list of UPNP device information dictionaries.
        """
        self.landscape_initialized.wait()

        upnp_device_config_list = self._internal_get_upnp_device_configs(ssh_only=ssh_only)

        return upnp_device_config_list

    def get_upnp_device_config_lookup_table(self) -> dict:
        """
            Returns a USN lookup table for upnp devices.
        """
        self.landscape_initialized.wait()

        upnp_device_table = self._internal_get_upnp_device_config_lookup_table()

        return upnp_device_table

    def list_available_devices_by_match(self, match_type, *match_params, count=None) -> List[LandscapeDevice]:
        """
            Creates and returns a list of devices from the available devices pool that are found
            to correspond to the match criteria provided.  If a 'count' parameter is passed
            then the number of devices returned is limited to count devices.

            .. note:: This API does not perform a checkout of the devices returns so the
                      caller should not consider themselves to the the owner of the devices.
        """
        matching_devices = []
        device_list = self.get_available_devices()

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

    def lookup_device_by_modelName(self, modelName) -> Optional[LandscapeDevice]:
        """
            Looks up a single device that is found to correspond to the modelName match criteria
            provided.
        """
        device = None

        matching_devices = self.list_devices_by_match("modelName", modelName, count=1)
        if len(matching_devices) > 0:
            device = matching_devices[0]

        return device

    def lookup_device_by_modelNumber(self, modelNumber) -> Optional[LandscapeDevice]:
        """
            Looks up a single device that is found to correspond to the modelNumber match criteria
            provided.
        """
        device = None

        matching_devices = self.list_devices_by_match("modelNumber", modelNumber, count=1)
        if len(matching_devices) > 0:
            device = matching_devices[0]

        return device

    def lookup_power_agent(self, power_mapping: str) -> Union[dict, None]:
        """
            Looks up a power agent by name.
        """
        power_agent = self._power_coordinator.lookup_agent(power_mapping)
        return power_agent

    def lookup_serial_agent(self, serial_mapping: str) -> Union[dict, None]:
        """
            Looks up a serial agent name.
        """
        serial_agent = self._serial_coordinator.lookup_agent(serial_mapping)
        return serial_agent

    def lookup_serial_config(self, serial_service_name: str):
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

    def register_integration_point(self, role: str, mixin: type):
        """
            This method should be called from the attach_to_environment methods from individual mixins
            in order to register the base level integrations.  Integrations can be hierarchical so it
            is only necessary to register the root level integration mixins, the descendant mixins can
            be called from the root level mixins.

            :param role: The name of a role to assign for a mixin.
            :param mixin: The mixin to register for the associated role.
        """
        self.landscape_initialized.wait()

        if role not in self._integrations:
            self._ordered_roles.append(role)
            self._integrations[role] = mixin
        else:
            raise AKitSemanticError("A mixin with the role %r was already registered." % role)

        return

    def _initialize(self):
        """
            Called by '__init__' once at the beginning of the lifetime of a Landscape derived
            type.  This allows the derived types to participate in a customized intialization
            process.
        """

        self._ordered_roles = []
        self._integrations = {}

        context = Context()
        log_landscape_declaration = context.lookup("/environment/behaviors/log-landscape-declaration")

        self._landscape_file = get_expanded_path(context.lookup("/environment/configuration/paths/landscape"))
        landscape_file_basename = os.path.basename(self._landscape_file)
        landscape_file_basename, landscape_file_ext = os.path.splitext(landscape_file_basename)

        try:
            lscape_desc = self.landscape_description()
            self._landscape_info = lscape_desc.load(self._landscape_file)

            if log_landscape_declaration:
                results_dir = get_path_for_output()

                landscape_info_copy = copy.deepcopy(self._landscape_info)
                mask_passwords(landscape_info_copy)

                landscape_file_copy = os.path.join(results_dir, "{}-declared{}".format(landscape_file_basename, landscape_file_ext))
                with open(landscape_file_copy, 'w') as lsf:
                    yaml.dump(landscape_info_copy, lsf, indent=4)

                landscape_file_copy = os.path.join(results_dir, "{}-declared{}".format(landscape_file_basename, ".json"))
                with open(landscape_file_copy, 'w') as lsf:
                    json.dump(landscape_info_copy, lsf, indent=4)

        except Exception as xcpt:
            err_msg = "Error loading the landscape file from (%s)%s%s" % (
                self._landscape_file, os.linesep, traceback.format_exc())
            raise AKitConfigurationError(err_msg) from xcpt

        if "environment" not in self._landscape_info:
            err_msg = "The landscape file must have an 'environment' decription. (%s)" % self._landscape_file
            raise AKitConfigurationError(err_msg)

        self._environment_info = self._landscape_info["environment"]
        if "label" not in self._environment_info:
            err_msg = "The landscape 'environment' decription must have a 'label' member (development, production, test). (%s)" % self._landscape_file
            raise AKitConfigurationError(err_msg)
        if "credentials" not in self._environment_info:
            err_msg = "There must be a 'environment/credentials' section."

        self._environment_label = self._environment_info["label"]

        if "muse" in self._environment_info:
            self._environment_muse = self._environment_info["muse"]
            if ("authhost" not in self._environment_muse) or ("ctlhost" not in self._environment_muse) or ("version" not in self._environment_muse):
                err_msg = "The landscape 'environment/muse' decription must have both a 'envhost' and 'version' members. (%s)" % self._landscape_file
                raise AKitConfigurationError(err_msg)

        # We must initialize the credential store before we start initialized any devices or connectivity
        self._initialize_credentials()

        self._initialize_device_coordinators()

        # Set the landscape_initialized even to allow other threads to use the APIs of the Landscape object
        self.landscape_initialized.set()

        # We need to wait till we have initialized the landscape before we start registering integration points
        self.landscape_description.register_integration_points(self)

        return

    def _initialize_credentials(self):
        """
        """

        credentials_list = self._environment_info["credentials"]
        for credential in credentials_list:
            if "identifier" not in credential:
                raise AKitConfigurationError("Credential items in 'environment/credentials' must have an 'identifier' member.")
            ident = credential["identifier"]

            if "category" not in credential:
                raise AKitConfigurationError("Credential items in 'environment/credentials' must have an 'category' member.")
            category = credential["category"]

            if category == "basic":
                BasicCredential.validate(credential)
                credobj = BasicCredential(**credential)
                self._credentials[ident] = credobj
            elif category == "muse":
                MuseCredential.validate(credential)
                credobj = MuseCredential(**credential)
                self._credentials[ident] = credobj
            elif category == "ssh":
                SshCredential.validate(credential)
                credobj = SshCredential(**credential)
                self._credentials[ident] = credobj
            else:
                errmsg = "Unknown category '{}' found in credential '{}'".format(category, ident)
                raise AKitConfigurationError(errmsg)

        return

    def _initialize_device_coordinators(self):
        """
            Initializes the device coordinators according the the information specified in the
            'devices' portion of the configuration file.
        """

        pod_info = self._landscape_info["pod"]

        # We need to initialize the power and serial coordinators before attempting to
        # initialize any devices, so the devices will be able to lookup power and
        # serial connections as they are initialized
        if "power" in pod_info:
            power_config = pod_info["power"]
            self._power_coordinator = PowerCoordinator(self, power_config)

        if "serial" in pod_info:
            serial_config = pod_info["serial"]
            # TODO: Add creation of SerialCoordinator
            self._serial_coordinator = None

        upnp_device_list = []
        ssh_device_list = []
        muse_device_list = []

        for dev_config_info in self._internal_get_device_configs():
            dev_type = dev_config_info["deviceType"]
            if dev_type == "network/upnp":
                upnp_device_list.append(dev_config_info)
                if "muse" in dev_config_info:
                    muse_device_list.append(dev_config_info)
                if "credentials" in dev_config_info:
                    ssh_cred_list = filter_credentials(dev_config_info, self._credentials, "ssh")
                    if len(ssh_cred_list) > 0:
                        ssh_device_list.append((dev_config_info, ssh_cred_list))
            elif dev_type == "network/muse":
                muse_device_list.append(dev_config_info)
            elif dev_type == "network/ssh":
                if "credentials" in dev_config_info:
                    ssh_cred_list = filter_credentials(dev_config_info, self._credentials, "ssh")
                    if len(ssh_cred_list) > 0:
                        ssh_device_list.append((dev_config_info, ssh_cred_list))
            else:
                errmsg_lines = [
                    "Unknown device type %r in configuration file." % dev_type,
                    "DEVICE INFO:"
                ]
                errmsg_lines.extend(split_and_indent_lines(pprint.pformat(dev_config_info, indent=4), 1))

                errmsg = os.linesep.join(errmsg_lines)
                self._logger.error(errmsg)

        # Setup to pass the landscape to attach_to_devices calls
        lscape = self

        context = Context()
        log_landscape_scan = context.lookup("/environment/behaviors/log-landscape-scan")

        found_device_results = []
        matching_device_results = []
        missing_device_results = []

        ssh_scan_results = {}
        upnp_scan_results = {}

        if len(upnp_device_list) > 0:
            from akit.integration.coordinators.upnpcoordinator import UpnpCoordinator # pylint: disable=import-outside-toplevel

            self._has_upnp_devices = True
            upnp_hint_list = self._internal_get_upnp_device_config_lookup_table()
            self._upnp_coord = UpnpCoordinator(lscape)
            found_device_results, matching_device_results, missing_device_results = self._upnp_coord.startup_scan(
                upnp_hint_list, watchlist=upnp_hint_list, exclude_interfaces=["lo"])

            if log_landscape_scan:
                upnp_scan_results = {
                    "found_devices": found_device_results,
                    "matching_devices": matching_device_results,
                    "missing_devices": missing_device_results
                }

        if len(ssh_device_list) > 0:
            from akit.integration.coordinators.sshpoolcoordinator import SshPoolCoordinator # pylint: disable=import-outside-toplevel

            self._has_ssh_devices = True
            self._ssh_coord = SshPoolCoordinator(lscape)
            ssh_config_errors, matching_device_results, missing_device_results = self._ssh_coord.attach_to_devices(
                ssh_device_list, upnp_coord=self._upnp_coord)

            ssh_scan_results = {
                "matching_devices": matching_device_results,
                "missing_devices": missing_device_results
            }

        if len(muse_device_list) > 0 and self._environment_muse is not None:
            envlabel = self._environment_label
            muse_authhost = self._environment_muse["authhost"]
            muse_ctlhost = self._environment_muse["ctlhost"]
            muse_version = self._environment_muse["version"]

            from akit.integration.coordinators.musecoordinator import MuseCoordinator # pylint: disable=import-outside-toplevel

            self._has_muse_devices = True
            self._muse_coord = MuseCoordinator(lscape)
            self._muse_coord.attach_to_devices(envlabel, muse_authhost, muse_ctlhost, muse_version, muse_device_list, upnp_coord=self._upnp_coord)

        if log_landscape_scan:
            scan_results = {
                "ssh": ssh_scan_results,
                "upnp": upnp_scan_results
            }

            landscape_scan_result_file = os.path.join(get_path_for_output(), "landscape-startup-scan.json")
            with open(landscape_scan_result_file, 'w') as srf:
                json.dump(scan_results, srf, indent=4)

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

        if self._landscape_info is None:
            raise AKitSemanticError("The _internal_get_device_configs method should not be called until _landscape_info has been set.")

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

    def _internal_get_upnp_device_configs(self, ssh_only=False) -> List[dict]:
        """
            Returns a list of UPNP device information dictionaries.

            .. note:: The _internal_ methods do not guard against calls prior to
            landscape initialization so they should only be called with care.  This
            should not be called until after the _landscape_info variable has been
            loaded and contains the configuration data from the landscape.yaml file.
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

            .. note:: The _internal_ methods do not guard against calls prior to
            landscape initialization so they should only be called with care.  This
            should not be called until after the _landscape_info variable has been
            loaded and contains the configuration data from the landscape.yaml file.
        """

        self.landscape_lock.acquire()
        try:
            device = None
            if keyid in self._all_devices:
                device = self._all_devices[keyid]
        finally:
            self.landscape_lock.release()

        return device

    def _internal_register_device(self, keyid, device):
        """
            Registeres a device and stores it by keyid.

            .. note:: The _internal_ methods do not guard against calls prior to
            landscape initialization so they should only be called with care.  This
            should not be called until after the _landscape_info variable has been
            loaded and contains the configuration data from the landscape.yaml file.
        """

        self.landscape_lock.acquire()
        try:
            # Add the device to all devices, all devices does not change
            # based on check-out or check-in activity
            self._all_devices[keyid] = device

            # Add the device to the device pool, the device pool is used
            # for tracking device availability for check-out
            self._device_pool[keyid] = device
        finally:
            self.landscape_lock.release()

        return

    def _locked_checkout_device(self, device) -> Optional[LandscapeDevice]:

        rtn_device = None

        keyid = device.keyid
        if keyid not in self._device_pool:
            raise AKitSemanticError("A device is being checked out, that is not in the device pool.")

        rtn_device = self._device_pool[keyid]
        del self._device_pool[keyid]

        return rtn_device

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

if VARIABLES.AKIT_LANDSCAPE_MODULE is not None:
    lscape_module_override = import_by_name(VARIABLES.AKIT_LANDSCAPE_MODULE)
    load_and_set_landscape_type(lscape_module_override )
    check_landscape = Landscape()
