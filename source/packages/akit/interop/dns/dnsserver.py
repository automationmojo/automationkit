"""
.. module:: dnspointer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsService object which represents a DNS service record.

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

from typing import Union, TYPE_CHECKING

import socket
import threading

from akit.interop.dns.dnsquestion import DnsQuestion
from akit.interop.dns.dnspacketreader import DnsPacketReader
from akit.networking.constants import MDNS_GROUP_ADDR, MDNS_GROUP_ADDR6, MDNS_PORT

if TYPE_CHECKING:
    from akit.interop.dns.dnspacketwriter import DnsPacketWriter

class DnsServer:
    """
        A DNS server
    """

    def __init__(self, endpoint=(MDNS_GROUP_ADDR, MDNS_PORT) ) -> None:
        self._svc_addr, self._svc_port = endpoint
        
        self._thread_response = None
        self._running = False
        self._shutdown_gate = threading.Event()
        self._shutdown_gate.set()
        return

    @property
    def svc_addr(self):
        return self._svc_addr

    @property
    def svc_port(self):
        return self._svc_port

    def start(self):
        sgate = threading.Event()
        sgate.clear()

        self._thread_response = threading.Thread(name="dns-responder", target=self._entry_thread_response, args=[sgate])
        self._thread_response.setDaemon(True)
        self._thread_response.start()

        sgate.wait()

        return
    
    def query_all_services(self):

        qpacket = DnsQuestion()

        return

    def wait(self, timeout=None):
        
        if self._running:
            self._shutdown_gate.wait(timeout)

    def _entry_thread_response(self, sgate: threading.Event):
        """
            The entry point for monitor thread.  The monitor thread sets up monitoring on all interfaces.

            :param sgate: The startup gate that is used to indicate to the thread spinning up the coordinator
                          that the monitor thread has started.
        """
        multicast_address = MDNS_GROUP_ADDR
        multicast_port = MDNS_PORT

        try:
            self._running = True
            self._shutdown_gate.clear()

            # Set the start gate to allow the thread spinning us up to continue
            sgate.set()

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

            try:
                # Make sure other Automation processes can also bind to the UPNP address and port
                # so they can also get responses.
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

                # Set us up to be a member of the group, this allows us to receive all the packets
                # that are sent to the group
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_address) + socket.inet_aton('0.0.0.0'))

                sock.bind((multicast_address, multicast_port))

                while self._running:
                    msg_data, addr = sock.recvfrom(1024)

                    reader = DnsPacketReader(msg_data)

                    print(reader)

            finally:
                sock.close()

        finally:
            self._shutdown_gate.set()

        return
