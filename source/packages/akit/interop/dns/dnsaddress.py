"""
.. module:: dnsaddress
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsAddress record type.

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

from typing import TYPE_CHECKING

import socket

from akit.networking.interfaces import is_ipv6_address

from akit.interop.dns.dnsrecord import DnsRecord

if TYPE_CHECKING:
    from akit.interop.dns.dnspacketwriter import DnsPacketWriter

class DnsAddress(DnsRecord):
    """
        A DNS address record
    """

    def __init__(self, name: str, rtype: int, rclass: int, ttl: int, address: bytes) -> None:
        DnsRecord.__init__(self, name, rtype, rclass, ttl)
        self._address = address
        return

    @property
    def address(self):
        return self._address

    def write(self, out: 'DnsPacketWriter') -> None:
        """
            Used in constructing an outgoing packet
        """
        out.write_string(self._address)
        return

    def __eq__(self, other: DnsRecord) -> bool:
        """
            Tests equality on priority, weight, port and server
        """
        # Call DnsRecord equality operator first because it can eliminate alot of equality checks early
        iseq = False
        if DnsRecord.__eq__(self, other):
            iseq = self._address == other._address
        return iseq

    def __ne__(self, other: DnsRecord) -> bool:
        """
            Non-equality test
        """
        isneq = not self.__eq__(other)
        return isneq

    def __str__(self) -> str:
        """
            String representation
        """
        strval = None

        try:
            strval = self.as_dns_string(
                socket.inet_ntop(
                    socket.AF_INET6 if is_ipv6_address(self._address) else socket.AF_INET, self._address
                )
            )
        except Exception:  # TODO stop catching all Exceptions
            strval = self.as_dns_string(str(self._address))

        return strval