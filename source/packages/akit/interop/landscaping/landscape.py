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

from akit.exceptions import AKitConfigurationError

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
