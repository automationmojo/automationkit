
from typing import Dict, Generator

from akit.mixins.upnpcoordinatorintegration import UpnpCoordinatorIntegration
import akit.testing.testplus as testplus

class AutomationPod(UpnpCoordinatorIntegration):
    """
    """

    @classmethod
    def attach_to_environment(cls, constraints: Dict={}):
        """
            This API is called so that the IntegrationMixIn can process configuration information.  The :class:`IntegrationMixIn`
            will verify that it has a valid environment and configuration to run in.

            :raises :class:`akit.exceptions.AKitMissingConfigError`, :class:`akit.exceptions.AKitInvalidConfigError`:
        """
        super(AutomationPod, cls).attach_to_environment(constraints=constraints)
        return

    @classmethod
    def attach_to_framework(cls, landscape: "Landscape"):
        """
            This API is called so that the IntegrationMixIn can attach to the test framework and participate with
            registration processes.  This allows the framework to ignore the bringing-up of mixins that are not being
            included by a test.
        """
        super(AutomationPod, cls).attach_to_framework(landscape)
        return


@testplus.integration(constraints={})
def automation_pod() -> Generator[AutomationPod, None, None]:
    yield AutomationPod()
