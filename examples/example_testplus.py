

from akit.integration.landscaping.landscape import Landscape
from akit.testing.testplus.resources import integration, scope

from akit.mixins.automationpodmixin import AutomationPodMixIn
from akit.mixins.scope import ScopeMixIn, ScopeAperture

class ScopeA(ScopeMixIn):

    @classmethod
    def scope_enter(self):
        return

    @classmethod
    def scope_exit(self):
        return


@integration
def pod() -> AutomationPodMixIn:
    return


def scopeA() -> ScopeMixIn:
    with ScopeAperture(ScopeA) as sa:
        sobj = ScopeA()
        yield sobj
