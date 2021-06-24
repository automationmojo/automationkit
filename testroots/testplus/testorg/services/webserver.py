from typing import Generator

import akit.testing.testplus as testplus

from akit.testing.testplus.resourcelifespan import ResourceLifespan

class WebServer:
    """
    """

@testplus.resource(constraints={})
def http_content_server() -> Generator[WebServer, None, None]:
    yield None
