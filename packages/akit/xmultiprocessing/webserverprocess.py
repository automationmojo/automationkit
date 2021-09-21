
from typing import Any, Tuple

import contextlib
import http.server
import multiprocessing
import multiprocessing.managers
import os
import socket

from threading import Thread

from functools import partial

from akit.xthreading.looper import Looper
from akit.xthreading.looperpool import LooperPool

class SimpleHTTPLooper(Looper):
    """
    """

    def loop(self, packet) -> bool:
        """
            Method that is overloaded by derived classes in order to implement a work loop.
        """
        server, request, client_address = packet
        self.process_request_packet(server, request, client_address)
        return True

    def process_request_packet(self, server, request, client_address):
        """
            Same as in BaseServer but in a looper thread.  We also perform some
            exception handling here to prevent threads from shutting down unexpectedly.

        """
        orig_name = self.thread_get_name()
        self.thread_set_name("{}-*".format(orig_name))
        try:
            server.finish_request(request, client_address)
        except Exception:
            server.handle_error(request, client_address)
        finally:
            server.shutdown_request(request)
        self.thread_set_name(orig_name)
        return


class ThreadPoolHTTPServer(LooperPool, http.server.HTTPServer):
    def __init__(self, address: Tuple[str, int], handler_class: http.server.SimpleHTTPRequestHandler,
                       group_name: str='webserver-worker', min_loopers: int=5, max_loopers: int=10, highwater: int=5,
                       daemon=True, **kwargs):
        LooperPool.__init__(self, SimpleHTTPLooper, group_name=group_name, min_loopers=min_loopers,
                         max_loopers=max_loopers, highwater=highwater, daemon=daemon,
                         **kwargs)
        http.server.HTTPServer.__init__(self, address, handler_class)
        return

    def process_request(self, request, client_address):
        """
            Start a new thread to process the request.
        """
        self.push_work((self, request, client_address))
        return

    def server_close(self):
        super().server_close()
        self._threads.join()
        return

class SimpleWebServer(ThreadPoolHTTPServer):

    def __init__(self, address: Tuple[str, int], rootdir: str, protocol: str):
        rootdir = os.path.abspath(os.path.expanduser(os.path.expandvars(rootdir)))
        http.server.SimpleHTTPRequestHandler.protocol_version = protocol
        handler_class = partial(http.server.SimpleHTTPRequestHandler, directory=rootdir)
        super().__init__(address, handler_class)
        return

    def get_server_address(self):
        return self.server_address

    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

    def start_serving(self):
        self.start_pool()

        start_thread = Thread(target=self.serve_forever, name='webserver-listener')
        start_thread.daemon = True
        start_thread.start()
        return

class SimpleWebServerManager(multiprocessing.managers.BaseManager):
    """
        This is a process manager used for creating a :class:`SimpleWebServer`
        in a remote process that can be communicated with via a proxy.
    """

SimpleWebServerManager.register("SimpleWebServer", SimpleWebServer)

def spawn_webserver_process(address: Tuple[str, int], rootdir: str, protocol: str="HTTP/1.0") -> Tuple[SimpleWebServerManager, SimpleWebServer]:
    websrvr_mgr = SimpleWebServerManager()
    websrvr_mgr.start()
    wsvr_proxy = websrvr_mgr.SimpleWebServer(address, rootdir, protocol)
    wsvr_proxy.start_serving()
    return websrvr_mgr, wsvr_proxy
