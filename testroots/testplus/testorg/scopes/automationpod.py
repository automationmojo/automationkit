
from typing import Dict, Generator

import akit.testing.testplus as testplus

from akit.iterop.landscaping.landscape import Landscape
from akit.testing.testplus.scopecoupling import ScopeCoupling


class AutomationPod(ScopeCoupling):
    """
    """

    landscape = Landscape()

    def __init__(self, upnp_integ, http_csrv):
        self._upnp_integ = upnp_integ
        self._http_csrv = http_csrv
        return

    @property
    def http_csrv(self):
        return self._http_csrv

    @property
    def upnp_integ(self):
        return self._upnp_integ


@testplus.scope()
def automation_pod(upnp_integ, http_csrv) -> Generator[AutomationPod, None, None]:
    yield AutomationPod(upnp_integ, http_csrv)
