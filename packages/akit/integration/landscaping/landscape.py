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

from typing import List, Optional, Union

import inspect
import os
import threading

import pprint

from akit.compat import import_by_name

from akit.environment.context import Context
from akit.environment.variables import AKIT_VARIABLES

from akit.exceptions import AKitConfigurationError

from akit.integration.landscaping.landscapedevice import LandscapeDevice

from akit.integration.landscaping.layers.landscapeconfigurationlayer import LandscapeConfigurationLayer
from akit.integration.landscaping.layers.landscapeintegrationlayer import LandscapeIntegrationLayer
from akit.integration.landscaping.layers.landscapeoperationallayer import LandscapeOperationalLayer

import threading


from akit.xlogging.foundations import getAutomatonKitLogger

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


class Landscape(LandscapeConfigurationLayer, LandscapeIntegrationLayer, LandscapeOperationalLayer):
    """
        The base class for all derived :class:`Landscape` objects.  The :class:`Landscape`
        object is a singleton object that provides access to the resources and test
        environment level methods.
    """

    context = Context()

    logger = getAutomatonKitLogger()
    landscape_lock = threading.RLock()

    _landscape_type = None
    _instance = None
    _instance_initialized = False

    def __new__(cls):
        """
            Constructs new instances of the Landscape object from the :class:`Landscape`
            type or from a derived type that is found in the module specified in the
            :module:`akit.environment.variables` module or by setting the
            'AKIT_CONFIG_LANDSCAPE_MODULE' environment variable.
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
        lscapeType = type(self)

        # We are a singleton so we only want the intialization code to run once
        lscapeType.landscape_lock.acquire()
        if not lscapeType._instance_initialized:
            lscapeType._instance_initialized = True
            lscapeType.landscape_lock.release()

            self._interactive_mode = False

            super().__init__()
        else:
            lscapeType.landscape_lock.release()

        return

    @property
    def interactive_mode(self):
        """
            Returns a boolean indicating if interactive mode is on or off.
        """
        return self._interactive_mode

    @interactive_mode.setter
    def set_interactive_mode(self, interactive: bool) -> None:
        """
            Turn on or off interactive mode.
        """
        self._interactive_mode = interactive
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

if AKIT_VARIABLES.AKIT_CONFIG_LANDSCAPE_MODULE is not None:
    lscape_module_override = import_by_name(AKIT_VARIABLES.AKIT_CONFIG_LANDSCAPE_MODULE)
    load_and_set_landscape_type(lscape_module_override )

# We need to ensure that the first time this module is loaded that we trigger
# the initialization of the landscape and that we activate the configuration
first_landscape = Landscape()
first_landscape.activate_configuration()


def startup_landscape(include_ssh=True, include_upnp=True, interactive=False) -> Landscape:
    """
        Statup the landscape outside of a testrun.
    """

    # ==================== Landscape Initialization =====================
    # The first stage of standing up the test landscape is to create and
    # initialize the Landscape object.  If more than one thread calls the
    # constructor of the Landscape, object, the other thread will block
    # until the first called has initialized the Landscape and released
    # the gate blocking other callers.

    # When the landscape object is first created, it spins up in configuration
    # mode, which allows consumers consume and query the landscape configuration
    # information.
    lscape = Landscape()
    lscape.interactive_mode = interactive

    lscape.activate_configuration()

    if include_upnp:
        from akit.coupling.upnpcoordinatorintegration import UpnpCoordinatorIntegration

        # Give the UpnpCoordinatorIntegration an opportunity to register itself, we are
        # doing this in this way to simulate test framework startup.
        UpnpCoordinatorIntegration.attach_to_framework(lscape)

    if include_ssh:
        from akit.coupling.sshpoolcoordinatorintegration import SshPoolCoordinatorIntegration

        # Give the SshPoolCoordinatorIntegration an opportunity to register itself, we are
        # doing this in this way to simulate test framework startup.
        SshPoolCoordinatorIntegration.attach_to_framework(lscape)

    # After all the coordinators have had an opportunity to register with the
    # 'landscape' object, transition the landscape to the activated 'phase'
    lscape.activate_integration()

    if include_upnp:
        # After we transition the the landscape to the activated phase, we give
        # the different coordinators such as the UpnpCoordinatorIntegration an
        # opportunity to attach to its environment and determine if the resources
        # requested and the resource configuration match
        UpnpCoordinatorIntegration.attach_to_environment()

    if include_ssh:
        # After we transition the the landscape to the activated phase, we give
        # the different coordinators such as the SshPoolCoordinatorIntegration an
        # opportunity to attach to its environment and determine if the resources
        # requested and the resource configuration match
        SshPoolCoordinatorIntegration.attach_to_environment()

    # Finalize the activation process and transition the landscape
    # to fully active where all APIs are available.
    lscape.activate_operations()

    if include_ssh:
        lscape.ssh_coord.establish_presence()

    if include_upnp:
        lscape.upnp_coord.establish_presence()

    return lscape
