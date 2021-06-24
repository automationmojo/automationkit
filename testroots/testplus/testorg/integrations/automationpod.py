
from typing import Generator

from akit.mixins.upnpcoordinatorintegration import UpnpCoordinatorIntegration
import akit.testing.testplus as testplus

class AutomationPod(UpnpCoordinatorIntegration):
    """
    """

@testplus.integration(constraints={})
def automation_pod() -> Generator[AutomationPod, None, None]:
    yield AutomationPod()