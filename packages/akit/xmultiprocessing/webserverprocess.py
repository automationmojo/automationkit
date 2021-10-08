
from typing import Any, Optional, Tuple

import contextlib
import multiprocessing
import multiprocessing.managers
import os
import socket

from http.server import SimpleHTTPRequestHandler

from threading import Thread

from functools import partial

from akit.networking.httpserverthreadpool import HttpServerThreadPool

class SimpleWebContentHandler(SimpleHTTPRequestHandler):
    def __init__(self, request: socket.socket, client_address: Tuple[str, int], server: HttpServerThreadPool, directory: Optional[str]=None, **_kwargs) -> None:
        """
            ..note: Overide the constructor for BaseHTTPRequestHandler so we can absorb any extra kwargs.
        """
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server, directory=directory)
        self._kwargs = _kwargs
        return

class SimpleWebServer(HttpServerThreadPool):

    def __init__(self, address: Tuple[str, int], directory: str, protocol: str, **kwargs):
        directory = os.path.abspath(os.path.expanduser(os.path.expandvars(directory)))
        
        SimpleWebContentHandler.protocol_version = protocol
        kwargs["directory"] = directory

        HttpServerThreadPool.__init__(self, address, SimpleWebContentHandler, **kwargs)
        return

    def get_server_address(self):
        """
            Get the address of the server.

            ..note: Overloaded to ensure this method will proxy well to remote processes.
        """
        return self.server_address

    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

    def server_close(self):
        super().server_close()
        return

    def server_start(self):
        """
            Start the server and thread pool.

            ..note: Overloaded to ensure this method will proxy well to remote processes.
        """
        HttpServerThreadPool.server_start(self)
        return
    
    def server_stop(self):
        """
            Stop the server and thread pool.

            ..note: Overloaded to ensure this method will proxy well to remote processes.
        """
        HttpServerThreadPool.server_stop(self)
        return

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
