

from typing import Generator

import akit.testing.testplus as testplus

from akit.testing.testplus.resourcelifespan import ResourceLifespan

from akit.mixins.upnpcoordinatorintegration import UpnpCoordinatorIntegration
from akit.mixins.scope import ScopeMixIn


class AutomationPod(UpnpCoordinatorIntegration):
    """
    """

class HTRoom(ScopeMixIn):
    """
    """

class WebServer:
    """
    """

@testplus.integration(constraints={})
def automation_pod() -> Generator[AutomationPod, None, None]:
    yield None

# Scopes can have varying lifespans. Scopes are a mechanism to include integrations
# and to establish conditions.
@testplus.scope(life_span=ResourceLifespan.Session)
def hometheater_room() -> Generator[HTRoom, None, None]:
    yield None

# 
@testplus.resource(constraints={})
def http_content_server() -> Generator[WebServer, None, None]:
    yield None


@testplus.param(automation_pod, identifier="apod")
@testplus.param(hometheater_room, identifier="room", constraints={"devices":["HT", ["S18", "S19"], ["S18", "S19"]]})
@testplus.param(http_content_server, identifier="websrv")
def test_dolby50(apod, room, websrv):
    return
