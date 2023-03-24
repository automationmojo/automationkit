"""
.. module:: sshcoordinator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains a SshPoolCoordinatorIntegration object to use for working with the computer nodes via SSH

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

from typing import Dict, Generator, List, Tuple, TYPE_CHECKING

from akit.exceptions import AKitConfigurationError, AKitSemanticError
from akit.coupling.coordinatorcoupling import CoordinatorCoupling
from akit.interop.coordinators.sshpoolcoordinator import SshPoolCoordinator

from akit.testing import testplus

# Types imported only for type checking purposes
if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

class SshPoolCoordinatorIntegration(CoordinatorCoupling):
    """
        The SshPoolCoordinatorIntegration handle the requirement registration for the SSH coordinator.
    """

    pathbase = "/ssh"

    def __init__(self, *args, **kwargs):
        """
            The default contructor for an :class:`SshPoolCoordinatorIntegration`.
        """
        super(SshPoolCoordinatorIntegration, self).__init__(*args, **kwargs)
        if self.pathbase is None:
            raise ValueError("The 'pathbase' class member variable must be set to a unique name for each integration class type.")

        self.context.insert(self.pathbase, self)
        return

    @classmethod
    def attach_to_environment(cls, constraints: Dict={}):
        """
            This API is called so that the IntegrationCoupling can process configuration information.  The :class:`IntegrationCoupling`
            will verify that it has a valid environment and configuration to run in.

            :raises :class:`akit.exceptions.AKitMissingConfigError`, :class:`akit.exceptions.AKitInvalidConfigError`:
        """
        resources_acquired = False

        ssh_device_list = cls.landscape.get_ssh_device_list()

        if len(ssh_device_list) > 0:
            resources_acquired = True

        if resources_acquired:
            cls.landscape.activate_integration_point("coordinator/ssh", cls.create_coordinator)

        return

    @classmethod
    def attach_to_framework(cls, landscape: "Landscape"):
        """
            This API is called so that the IntegrationCoupling can attach to the test framework and participate with
            registration processes.  This allows the framework to ignore the bring-up of couplings that are not being
            included by a test.
        """
        super(SshPoolCoordinatorIntegration, cls).attach_to_framework(landscape)
        cls.landscape.register_integration_point("coordinator/ssh", cls)
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
        cls.coordinator = SshPoolCoordinator(landscape)
        return cls.coordinator

    @classmethod
    def declare_precedence(cls) -> int:
        """
            This API is called so that the IntegrationCoupling can declare an ordinal precedence that should be
            utilized for bringing up its integration state.
        """
        # We need to call the base class, it sets the 'logger' member
        super(SshPoolCoordinatorIntegration, cls).declare_precedence()
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
    def establish_connectivity(cls, allow_missing_devices: bool=False) -> Tuple[List[str], dict]:
        """
            This API is called so the `IntegrationCoupling` can establish connectivity with any compute or storage
            resources.

            :returns: A tuple with a list of error messages for failed connections and dict of connectivity
                      reports for devices devices based on the coordinator.
        """

        ssh_device_list = cls.landscape.get_ssh_device_list()

        if len(ssh_device_list) == 0:
            raise AKitSemanticError("We should have not been called if no SSH devices are available.")

        upnp_coord = cls.landscape._internal_get_upnp_coord()

        ssh_config_errors, matching_device_results, missing_device_results = cls.coordinator.attach_to_devices(
            ssh_device_list, upnp_coord=upnp_coord)

        ssh_scan_results = {
            "ssh": {
                "matching_devices": matching_device_results,
                "missing_devices": missing_device_results
            }
        }

        return (ssh_config_errors, ssh_scan_results)

    @classmethod
    def establish_presence(cls) -> Tuple[List[str], dict]:
        """
            This API is called so the `IntegrationCoupling` can establish presence with any compute or storage
            resources.

            :returns: A tuple with a list of error messages for failed connections and dict of connectivity
                      reports for devices devices based on the coordinator.
        """
        return

@testplus.integration()
def ssh_coordinator_integration() -> Generator[SshPoolCoordinatorIntegration, None, None]:
    yield SshPoolCoordinatorIntegration()
