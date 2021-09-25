from typing import Generator

import akit.testing.testplus as testplus

from akit.testing.testplus.resourcelifespan import ResourceLifespan

from akit.testing.testplus.scopecoupling import ScopeCoupling

from testorg.integrations.automationpod import automation_pod

class HTRoom(ScopeCoupling):
    """
    """

# Scopes can have varying lifespans. Scopes are a mechanism to include integrations
# and to establish conditions.
@testplus.scope()
def hometheater_room(apod, constraints) -> Generator[HTRoom, None, None]:
    yield None
