
from typing import List, Optional, Tuple

import contextlib
import datetime
import email
import os
import urllib
import socket

from http.server import SimpleHTTPRequestHandler
from http import HTTPStatus

from akit.networking.httpserverthreadpool import HttpServerThreadPool

class SimpleWebContentHandler(SimpleHTTPRequestHandler):

    index_pages = ["index.html", "index.htm"]

    def __init__(self, request: socket.socket, client_address: Tuple[str, int], server: HttpServerThreadPool, 
                 directory: Optional[str]=None, index_pages: Optional[List[str]]=None, **_kwargs) -> None:
        """
            ..note: Overide the constructor for BaseHTTPRequestHandler so we can absorb any extra kwargs.
        """
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server, directory=directory)
        
        if index_pages is not None:
            self.index_pages = index_pages

        self._kwargs = _kwargs
        return
    
    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.end_headers()
                return None
            for index in self.index_pages:
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        # check for trailing "/" which should return 404. See Issue17324
        # The test for this was added in test_httpserver.py
        # However, some OS platforms accept a trailingSlash as a filename
        # See discussion on python-dev and Issue34711 regarding
        # parseing and rejection of filenames with a trailing slash
        if path.endswith("/"):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        try:
            fs = os.fstat(f.fileno())
            # Use browser cache if possible
            if ("If-Modified-Since" in self.headers
                    and "If-None-Match" not in self.headers):
                # compare If-Modified-Since and time of last file modification
                try:
                    ims = email.utils.parsedate_to_datetime(
                        self.headers["If-Modified-Since"])
                except (TypeError, IndexError, OverflowError, ValueError):
                    # ignore ill-formed values
                    pass
                else:
                    if ims.tzinfo is None:
                        # obsolete format with no timezone, cf.
                        # https://tools.ietf.org/html/rfc7231#section-7.1.1.1
                        ims = ims.replace(tzinfo=datetime.timezone.utc)
                    if ims.tzinfo is datetime.timezone.utc:
                        # compare to UTC datetime of last modification
                        last_modif = datetime.datetime.fromtimestamp(
                            fs.st_mtime, datetime.timezone.utc)
                        # remove microseconds, like in If-Modified-Since
                        last_modif = last_modif.replace(microsecond=0)

                        if last_modif <= ims:
                            self.send_response(HTTPStatus.NOT_MODIFIED)
                            self.end_headers()
                            f.close()
                            return None

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

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