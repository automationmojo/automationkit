
from typing import Generator

from akit.testing import testplus

from akit.coupling.upnpcoordinatorintegration import UpnpCoordinatorIntegration

@testplus.integration()
def upnp_coordinator_integration() -> Generator[UpnpCoordinatorIntegration, None, None]:
    yield UpnpCoordinatorIntegration()
