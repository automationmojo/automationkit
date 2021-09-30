
from typing import Dict, Generator

import akit.testing.testplus as testplus

from akit.integration.landscaping.landscape import Landscape
from akit.testing.testplus.scopecoupling import ScopeCoupling


class AutomationPod(ScopeCoupling):
    """
    """

    landscape = Landscape()

    def __init__(self, upnp_integ):
        self._upnp_integ = upnp_integ
        return

    @property
    def upnp_integ(self):
        return self._upnp_integ


@testplus.scope()
def automation_pod(upnp_integ) -> Generator[AutomationPod, None, None]:
    yield AutomationPod(upnp_integ)
