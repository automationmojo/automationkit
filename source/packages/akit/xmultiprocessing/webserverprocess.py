__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Tuple

import multiprocessing
import multiprocessing.managers

from akit.networking.simplewebserver import SimpleWebServer

class SimpleWebServerManager(multiprocessing.managers.BaseManager):
    """
        This is a process manager used for creating a :class:`SimpleWebServer`
        in a remote process that can be communicated with via a proxy.
    """

SimpleWebServerManager.register("SimpleWebServer", SimpleWebServer)

def spawn_webserver_process(address: Tuple[str, int], rootdir: str, protocol: str="HTTP/1.0") -> Tuple[SimpleWebServerManager, SimpleWebServer]:
    srvr_mgr = SimpleWebServerManager()
    srvr_mgr.start()
    wsvr_proxy = srvr_mgr.SimpleWebServer(address, rootdir, protocol)
    return srvr_mgr, wsvr_proxy
