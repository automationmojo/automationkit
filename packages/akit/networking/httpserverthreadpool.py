
from typing import Optional, Tuple

import socket

from socketserver import BaseServer
from threading import Thread

from http.server import HTTPServer, BaseHTTPRequestHandler

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

class HttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request: socket.socket, client_address: Tuple[str, int], server: BaseServer, **_kwargs) -> None:
        """
            ..note: Overide the constructor for BaseHTTPRequestHandler so we can absorb any extra kwargs.
        """
        BaseHTTPRequestHandler.__init__(request, client_address, server)
        self._kwargs = _kwargs
        return

class HttpServerThreadPool(LooperPool, HTTPServer):
    def __init__(self, address: Tuple[str, int], handler_class: HttpRequestHandler, group_name: str='webserver-worker',
                 min_loopers: int=5, max_loopers: int=10, highwater: int=5, daemon=True, **handler_kwargs):
        LooperPool.__init__(self, SimpleHTTPLooper, group_name=group_name, min_loopers=min_loopers, max_loopers=max_loopers,
                            highwater=highwater, daemon=daemon)
        HTTPServer.__init__(self, address, handler_class)
        self._handler_kwargs = handler_kwargs
        return

    def finish_request(self, request: socket.socket, client_address: Tuple[str, int]) -> None:
        self.RequestHandlerClass(request, client_address, self, **self._handler_kwargs)
        return

    def get_request(self) -> socket.socket:
        asock = self.socket.accept()
        return asock

    def get_server_address(self) -> Tuple[str, int]:
        rtnval = self.server_address
        return rtnval

    def process_request(self, request, client_address):
        """
            Start a new thread to process the request.
        """
        self.push_work((self, request, client_address))
        return

    def server_stop(self):
        super().server_close()
        self.shutdown()
        return

    def server_start(self):
        self.start_pool()

        start_thread = Thread(target=self.serve_forever, name=self._group_name)
        start_thread.daemon = True
        start_thread.start()
        return
