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

import threading

from akit.interop.dns.dnsrecord import DnsRecord

if TYPE_CHECKING:
    from akit.interop.dns.dnspacketwriter import DnsPacketWriter

class DnsService(DnsRecord):
    """
        A DNS service record
    """

    def __init__(self, name: str, rtype: int, rclass: int, ttl: Union[float, int], priority: int,
                 weight: int, port: int, server: str ) -> None:
        DnsRecord.__init__(self, name, rtype, rclass, ttl)
        self._priority = priority
        self._weight = weight
        self._port = port
        self._server = server

        self._thread_response = None
        self._running = False
        self._shutdown_gate = threading.Event()
        self._shutdown_gate.set()
        return

    @property
    def port(self):
        return self._port

    @property
    def priority(self):
        return self._priority

    @property
    def server(self):
        return self._server

    @property
    def weight(self):
        return self._weight
    
    def write(self, out: 'DnsPacketWriter') -> None:
        """
            Used in constructing an outgoing packet
        """
        out.write_short(self._priority)
        out.write_short(self._weight)
        out.write_short(self._port)
        out.write_name(self._server)
        return

    def __eq__(self, other: DnsRecord) -> bool:
        """
            Tests equality on priority, weight, port and server
        """
        # Call DnsRecord equality operator first because it can eliminate alot of equality checks early
        iseq = False
        if DnsRecord.__eq__(self, other):
            iseq = self._priority == other._priority and self._weight == other._weight and self._port == other._port and self._server == other._server
        return iseq

    def __ne__(self, other: DnsRecord) -> bool:
        """
            Non-equality test
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
            String representation
        """
        other = self._server + " " + self._port+ " " + self._priority + " " + self._weight
        strval = self.as_dns_string(other=other)
        return strval