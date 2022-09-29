"""
.. module:: automationpodcoupling
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains a UpnpCoordinatorIntegration object to use for working with the nodes of a cluster

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

from typing import Dict, List, Tuple, TYPE_CHECKING

from akit.environment.contextpaths import ContextPaths
from akit.exceptions import AKitConfigurationError, AKitSemanticError
from akit.coupling.coordinatorcoupling import CoordinatorCoupling
from akit.interop.coordinators.upnpcoordinator import UpnpCoordinator

# Types imported only for type checking purposes
if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

class UpnpCoordinatorIntegration(CoordinatorCoupling):
    """
        The UpnpCoordinatorIntegration handle the requirement registration for the UPNP coordinator.
    """

    pathbase = "/upnp"

    def __init__(self, *args, **kwargs):
        """
            The default contructor for an :class:`UpnpCoordinatorIntegration`.
        """
        super(UpnpCoordinatorIntegration, self).__init__(*args, **kwargs)
        return

    @classmethod
    def attach_to_environment(cls, constraints: Dict={}):
        """
            This API is called so that the IntegrationCoupling can process configuration information.  The :class:`IntegrationCoupling`
            will verify that it has a valid environment and configuration to run in.

            :raises :class:`akit.exceptions.AKitMissingConfigError`, :class:`akit.exceptions.AKitInvalidConfigError`:
        """
        resources_acquired = False

        upnp_device_hints = cls.landscape.get_upnp_device_config_lookup_table()
        if len(upnp_device_hints) > 0:
            resources_acquired = True

        if resources_acquired:
            cls.landscape.activate_integration_point("coordinator/upnp", cls.create_coordinator)
        else:
            errmsg = "The required UPNP resources were not configured."
            raise AKitConfigurationError(errmsg) from None

        return

    @classmethod
    def attach_to_framework(cls, landscape: "Landscape"):
        """
            This API is called so that the IntegrationCoupling can attach to the test framework and participate with
            registration processes.  This allows the framework to ignore the bringing-up of couplings that are not being
            included by a test.
        """
        super(UpnpCoordinatorIntegration, cls).attach_to_framework(landscape)
        cls.landscape.register_integration_point("coordinator/upnp", cls)
        return

    @classmethod
    def collect_resources(cls):
        """
            This API is called so the `IntegrationCoupling` can connect with a resource management
            system and gain access to the resources required for the automation run.

            :raises :class:`akit.exceptions.AKitResourceError`:
        """
        return

    @classmethod
    def create_coordinator(cls, landscape: "Landscape") -> object:
        """
            This API is called so that the landscape can create a coordinator for a given integration role.
        """
        cls.coordinator = UpnpCoordinator(landscape)
        return cls.coordinator

    @classmethod
    def declare_precedence(cls) -> int:
        """
            This API is called so that the IntegrationCoupling can declare an ordinal precedence that should be
            utilized for bringing up its integration state.
        """
        # We need to call the base class, it sets the 'logger' member
        super(UpnpCoordinatorIntegration, cls).declare_precedence()
        return

    @classmethod
    def diagnostic(cls, label: str, level: int, diag_folder: str):
        """
            The API is called by the :class:`akit.sequencer.Sequencer` object when the automation sequencer is
            building out a diagnostic package at a diagnostic point in the automation sequence.  Example diagnostic
            points are:

            * pre-run
            * post-run

            Each diagnostic package has its own storage location so derived :class:`akit.scope.ScopeCoupling` objects
            can simply write to their specified output folder.

            :param label: The label associated with this diagnostic.
            :param level: The maximum diagnostic level to run dianostics for.
            :param diag_folder: The output folder path where the diagnostic information should be written.
        """

        return

    @classmethod
    def establish_connectivity(cls, allow_missing_devices: bool=False, upnp_recording: bool = False, allow_unknown_devices: bool = False) -> Tuple[List[str], dict]:
        """
            This API is called so the `IntegrationCoupling` can establish connectivity with any compute or storage
            resources.

            :returns: A tuple with a list of error messages for failed connections and dict of connectivity
                      reports for devices devices based on the coordinator.
        """
        lscape = cls.landscape

        exclude_interfaces = ["lo"]

        runtime_exclude_interfaces = cls.context.lookup(ContextPaths.UPNP_EXCLUDE_INTERFACES)
        if runtime_exclude_interfaces is not None:
            exclude_interfaces = runtime_exclude_interfaces

        upnp_hint_table = lscape.get_upnp_device_config_lookup_table()
        
        if len(upnp_hint_table) == 0:
            raise AKitSemanticError("we should not have been called if the upnp device config had 0 devices.") from None

        required_devices = None
        if not allow_missing_devices:
            required_devices = [usn for usn in upnp_hint_table.keys()]

        found_device_results, matching_device_results, missing_device_results = cls.coordinator.startup_scan(
            upnp_hint_table, watchlist=upnp_hint_table, required_devices=required_devices, exclude_interfaces=exclude_interfaces,
            upnp_recording=upnp_recording, allow_unknown_devices=allow_unknown_devices)

        conn_results = {
            "upnp": {
                "found": found_device_results,
                "matching": matching_device_results,
                "missing": missing_device_results
            }
        }

        conn_errors = []

        return (conn_errors, conn_results)

    @classmethod
    def establish_presence(cls) -> Tuple[List[str], dict]:
        """
            This API is called so the `IntegrationCoupling` can establish presence with any compute or storage
            resources.

            :returns: A tuple with a list of error messages for failed connections and dict of connectivity
                      reports for devices devices based on the coordinator.
        """
        cls.coordinator.establish_presence()
        return

    def checkout_upnp_device(self, usn):
        """
            Checkout a device from the device pool by USN.
        """
        codev = None

        if usn in self.upnp_devices_pool:
            codev = self.upnp_devices_pool.pop(usn)
            self.upnp_devices_inuse[usn] = codev

        return codev

    def checkin_upnp_device(self, codev):
        """
            Checkin a device to the device pool.
        """
        usn = codev["USN"]

        if usn in self.upnp_devices_inuse:
            codev = self.upnp_devices_inuse.pop(usn)
            self.upnp_devices_pool[usn] = codev

        return

    
