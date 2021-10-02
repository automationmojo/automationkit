
from typing import Generator

import os

import akit.testing.testplus as testplus

from akit.testing.testplus.resourcelifespan import ResourceLifespan

class WebServer:
    """
    """
    def __init__(self, root_directory):
        self._root_directory = os.path.abspath(os.path.expanduser(os.path.expandvars(root_directory)))
        return

    def start(self):
        return

    def stop(self):
        return

@testplus.resource(constraints={"root_directory": "/var/www"})
def http_content_server(constraints) -> Generator[WebServer, None, None]:
    root_directory = constraints["root_directory"]

    web_srvr = WebServer(root_directory)
    web_srvr.start()

    yield web_srvr

    web_srvr.stop()
