"""
.. module:: musecoordinator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the MuseCoordinator which is used for managing connectivity with muse managed
        devices visible in the automation landscape.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import socket
import weakref

from http.server import HTTPServer, BaseHTTPRequestHandler

from akit.paths import get_expanded_path
from akit.xlogging.foundations import getAutomatonKitLogger

from akit.integration.agents.museagent import MuseAgent
from akit.integration.landscaping.landscapedevice import LandscapeDevice

from akit.integration.coordinators.coordinatorbase import CoordinatorBase

class MuseCoordinator(CoordinatorBase):
    """
        The :class:`MuseCoordinator` creates a pool of agents that can be used to
        coordinate the interop activities of the automation process and remote MUSE
        nodes.
    """
    # pylint: disable=attribute-defined-outside-init

    def __init__(self, lscape, control_point=None, workers: int = 5):
        super(MuseCoordinator, self).__init__(lscape, control_point=control_point, workers=workers)
        return

    def _initialize(self, control_point=None, workers: int = 5):
        """
            Called by the CoordinatorBase constructor to perform the one time initialization of the coordinator Singleton
            of a given type.
        """
        self._cl_usn_to_ip_lookup = {}
        self._cl_ip_to_host_lookup = {}
        return

    def attach_to_devices(self, envlabel, authhost, ctlhost, version, musedevices, upnp_coord=None):

        lscape = self.landscape

        self._envlabel = envlabel
        self._authhost = authhost
        self._ctlhost = ctlhost
        self._version = version

        muse_config_errors = []

        for musedev_config in musedevices:
            devtype = musedev_config["deviceType"]
            museinfo = musedev_config["muse"]
            host = None
            usn = None

            if "host" in museinfo:
                host = museinfo["host"]
            elif devtype == "network/upnp":
                usn = musedev_config["upnp"]["USN"]
                if upnp_coord is not None:
                    dev = upnp_coord.lookup_device_by_usn(usn)
                    if dev is None:
                        dev = upnp_coord.lookup_device_by_usn(usn)
                    ipaddr = dev.IPAddress
                    host = ipaddr
                else:
                    muse_config_errors.append(museinfo)

            if host is not None:
                username = museinfo["username"]
                password = museinfo["password"]
                apikey = museinfo["apikey"]
                secret = museinfo["secret"]

                bearer = None
                if "bearer" in museinfo:
                    bearer = museinfo["bearer"]

                ip = socket.gethostbyname(host)
                agent = MuseAgent(envlabel, authhost, ctlhost, host, username, password, apikey, secret, bearer=bearer, version=self._version)

                self._coord_lock.acquire()
                try:
                    self._cl_ip_to_host_lookup[ip] = host
                    self._cl_children[host] = agent
                    if usn is not None:
                        self._cl_usn_to_ip_lookup[usn] = ipaddr
                finally:
                    self._coord_lock.release()

                coord_ref = weakref.ref(self)

                basedevice = None
                if usn is not None:
                    basedevice = lscape._internal_lookup_device_by_keyid(usn)
                    basedevice.attach_extension("muse", agent)
                else:
                    basedevice = LandscapeDevice(lscape, host, "network/muse", musedev_config)
                    basedevice.initialize_features()
                    basedevice.attach_extension("muse", agent)
                    lscape._internal_register_device(host, basedevice)

                basedevice_ref = weakref.ref(basedevice)
                agent.initialize(coord_ref, basedevice_ref, host, ip, musedev_config)
            else:
                muse_config_errors.append(museinfo)

        return muse_config_errors

    def lookup_device_by_host(self, host):
        """
            Looks up the agent for a device by its hostname.  If the
            agent is not found then the API returns None.
        """
        device = None

        self._coord_lock.acquire()
        try:
            if host in self._cl_children:
                device = self._cl_children[host]
        finally:
            self._coord_lock.release()

        return device

    def lookup_device_by_ip(self, ip):
        """
            Looks up the agent for a device by its ip address.  If the
            agent is not found then the API returns None.
        """
        device = None

        self._coord_lock.acquire()
        try:
            if ip in self._cl_ip_to_host_lookup:
                host = self._cl_ip_to_host_lookup[ip]
                device = self.lookup_agent_by_host(host)
        finally:
            self._coord_lock.release()

        return device

    def lookup_agent_by_usn(self, usn):
        """
            Looks up the agent for a UPNP device by its USN.  If the
            agent is not found then the API returns None.
        """
        agent = None

        self._coord_lock.acquire()
        try:
            if usn in self._cl_usn_to_ip_lookup:
                ip = self._cl_usn_to_ip_lookup[usn]
                agent = self.lookup_agent_by_ip(ip)
        finally:
            self._coord_lock.release()

        return agent

    def _callback_server_entry(self):

        class AuthenticationCallbackHandler(BaseHTTPRequestHandler):

            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Hello, world!')

        self._callback_server = HTTPServer(('localhost', 5000), AuthenticationCallbackHandler)

        self._callback_server.serve_forever()

        return
