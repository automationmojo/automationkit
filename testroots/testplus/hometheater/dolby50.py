

from typing import Generator

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


@integration(constraints={})
def automation_pod() -> Generator[AutomationPod, None, None]:
    yield None

# Scopes can have varying lifespans. Scopes are a mechanism to include integrations
# and to establish conditions.
@scope(life_span=ResourceLifespan.Session)
def hometheater_room() -> Generator[HTRoom, None, None]:
    yield None

# 
@resource(constraints={})
def http_content_server() -> Generator[WebServer, None, None]:
    yield None


@param(automation_pod, identifier="apod")
@param(hometheater_room, identifier="room", constraints={"devices":["HT", ["S18", "S19"], ["S18", "S19"]]})
@param(http_content_server, identifier="websrv")
def test_dolby50(apod, room, websrv):
    return
