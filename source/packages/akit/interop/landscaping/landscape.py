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

from typing import Dict, List, Optional, Union

import inspect
import os
import pprint
import threading

import zeroconf
import zeroconf.const

from akit.compat import import_by_name

from akit.environment.context import Context
from akit.environment.variables import AKIT_VARIABLES

from akit.exceptions import AKitConfigurationError, AKitSemanticError
from akit.friendlyidentifier import FriendlyIdentifier
from akit.interop.landscaping.landscapedevice import LandscapeDevice

from akit.interop.landscaping.layers.landscapeconfigurationlayer import LandscapeConfigurationLayer
from akit.interop.landscaping.layers.landscapeintegrationlayer import LandscapeIntegrationLayer
from akit.interop.landscaping.layers.landscapeoperationallayer import LandscapeOperationalLayer

from akit.interop.dns.mdnsserviceinfo import MdnsServiceInfo
from akit.interop.dns.mdnsservicecatalog import MdnsServiceCatalog

from akit.wellknown.singletons import LandscapeSingleton


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
        environment level methods.  The functionality of the :class:`Landscape` object is setup
        so it can be transitioned through activation stages:
        
        * Configuration
        * Integration
        * Operational

        The different phases of operation of the landscape allow it to be used for a wider variety
        of purposes from commandline configuration and maintenance operations, peristent services
        and automation run functionality.

        The activation stages or levels of the :class:`Landscape` object are implemented using
        a python MixIn pattern in order to ensure that individual layers can be customized
        using object inheritance while at the same time keeping the object hierarchy simple.

        ..note: The :class:`Landscape` object constructor utilizes the `super` keyword for calling
        the mixin layer constructors using method resolution order or `mro`.  In order for `super`
        to work correctly all objects in the hierarchy should also provide a constructor and should
        also utilize `super`.  This is true also for objects that only inherit from :class:`object`.
        Should you need to create a custom layer override object, you must ensure the proper use
        of `super` in its constructor.
    """

    context = Context()

    logger = getAutomatonKitLogger()
    landscape_lock = threading.RLock()

    _landscape_type = None
    _instance = None
    _instance_initialized = False

    MDNS_BROWSE_TYPES = ["_http._tcp.local.", "_sonos._tcp.local."]

    def __new__(cls):
        """
            Constructs new instances of the Landscape object from the :class:`Landscape`
            type or from a derived type that is found in the module specified in the
            :module:`akit.environment.variables` module or by setting the
            'AKIT_CONFIG_EXTENSION_POINTS_MODULE' environment variable and overloading
            the 'get_landscape_type' method.
        """

        if Landscape._landscape_type is None:
            if Landscape._instance is None:
                Landscape._instance = super(Landscape, cls).__new__(cls)
        elif Landscape._instance is None:
            Landscape._instance = super(Landscape, cls._landscape_type).__new__(cls._landscape_type)

        return Landscape._instance

    def __init__(self):
        """
            Creates an instance or reference to the :class:`Landscape` singleton object.  On the first call to this
            constructor the :class:`Landscape` object is initialized and the landscape configuration is loaded.
        """
        
        # We are a singleton so we only want the intialization code to run once
        Landscape.landscape_lock.acquire()
        if not Landscape._instance_initialized:
            Landscape._instance_initialized = True
            Landscape.landscape_lock.release()

            self._interactive_mode = False

            super().__init__()

            self._zeroconf = zeroconf.Zeroconf()
            self._zeroconf_catalog = MdnsServiceCatalog(self.logger)
            self._zeroconf_browser = zeroconf.ServiceBrowser(self._zeroconf, self.MDNS_BROWSE_TYPES, self._zeroconf_catalog)

        else:
            Landscape.landscape_lock.release()

        return

    @property
    def interactive_mode(self):
        """
            Returns a boolean indicating if interactive mode is on or off.
        """
        return self._interactive_mode

    @interactive_mode.setter
    def interactive_mode(self, interactive: bool) -> None:
        """
            Turn on or off interactive mode.
        """
        self._interactive_mode = interactive
        return

    @property
    def zeroconf(self) -> zeroconf.Zeroconf:
        """
            Returns the ZeroConf object.
        """
        return self._zeroconf
    
    @property
    def zeroconf_catalog(self) -> MdnsServiceCatalog:
        """
            Returns the service catalog that is used to lookup specific information about
            services reported by mDNS
        """
        return self._zeroconf_catalog

    @property
    def zeroconf_browser(self) -> "zeroconf.ServiceBrowser":
        """
            Returns the service browser used for searching for mDNS services.
        """
        return self._zeroconf_browser

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

    def mdns_list_service_names_for_type(self, svc_type: str) -> List[str]:

        svc_name_list = self._zeroconf_catalog.list_service_names_for_type(svc_type)

        return svc_name_list

    def mdns_lookup_service_info(self, svc_type: str, svc_name: str) -> MdnsServiceInfo:
        
        service_info = self._zeroconf_catalog.lookup_service_info(svc_type, svc_name)

        return service_info

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

def startup_landscape(include_ssh: bool=True, include_upnp: bool=True,
                      allow_missing_devices: bool=False, allow_unknown_devices: bool=False,
                      validate_features: bool=True, validate_topology: bool=True,
                      interactive: Optional[bool]=None) -> Landscape:
    """
        Statup the landscape outside of a testrun.
    """

    interactive_mode = False
    if AKIT_VARIABLES.AKIT_INTERACTIVE_CONSOLE:
        interactive_mode = AKIT_VARIABLES.AKIT_INTERACTIVE_CONSOLE

    if interactive is not None:
        interactive_mode = interactive

    # ==================== Landscape Initialization =====================
    # The first stage of standing up the test landscape is to create and
    # initialize the Landscape object.  If more than one thread calls the
    # constructor of the Landscape, object, the other thread will block
    # until the first called has initialized the Landscape and released
    # the gate blocking other callers.

    # When the landscape object is first created, it spins up in configuration
    # mode, which allows consumers consume and query the landscape configuration
    # information.
    lscape = LandscapeSingleton()
    lscape.interactive_mode = interactive_mode

    lscape.activate_configuration()

    from akit.extensionpoints import AKitExtensionPoints
    extension_points = AKitExtensionPoints()

    UpnpCoordinatorIntegrationType = None
    SshPoolCoordinatorIntegrationType = None

    if include_upnp:
        UpnpCoordinatorIntegrationType = extension_points.get_coupling_upnp_coord_integration_type()
    
        # Give the UpnpCoordinatorIntegration an opportunity to register itself, we are
        # doing this in this way to simulate test framework startup.
        UpnpCoordinatorIntegrationType.attach_to_framework(lscape)

    if include_ssh:
        SshPoolCoordinatorIntegrationType = extension_points.get_coupling_ssh_coord_integration_type()

        # Give the SshPoolCoordinatorIntegration an opportunity to register itself, we are
        # doing this in this way to simulate test framework startup.
        SshPoolCoordinatorIntegrationType.attach_to_framework(lscape)

    # After all the coordinators have had an opportunity to register with the
    # 'landscape' object, transition the landscape to the activated 'phase'
    lscape.activate_integration()

    if UpnpCoordinatorIntegrationType is not None:
        # After we transition the the landscape to the activated phase, we give
        # the different coordinators such as the UpnpCoordinatorIntegration an
        # opportunity to attach to its environment and determine if the resources
        # requested and the resource configuration match
        UpnpCoordinatorIntegrationType.attach_to_environment()

    if SshPoolCoordinatorIntegrationType is not None:
        # After we transition the the landscape to the activated phase, we give
        # the different coordinators such as the SshPoolCoordinatorIntegration an
        # opportunity to attach to its environment and determine if the resources
        # requested and the resource configuration match
        SshPoolCoordinatorIntegrationType.attach_to_environment()

    # Finalize the activation process and transition the landscape
    # to fully active where all APIs are available.
    lscape.activate_operations(allow_missing_devices=allow_missing_devices,
                               allow_unknown_devices=allow_unknown_devices,
                               validate_features=validate_features,
                               validate_topology=validate_topology)

    if include_ssh:
        lscape.ssh_coord.establish_presence()

    if include_upnp:
        lscape.upnp_coord.establish_presence()

    return lscape
