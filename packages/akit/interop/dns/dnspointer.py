"""
.. module:: dnspointer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsPointer which represents a DNS record pointer.

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

from akit.interop.dns.dnsrecord import DnsRecord

if TYPE_CHECKING:
    from akit.interop.dns.dnspacketwriter import DnsPacketWriter

class DnsPointer(DnsRecord):
    """
        A DNS pointer record
    """

    def __init__(self, name: str, rtype: int, rclass: int, ttl: int, alias: str) -> None:
        DnsRecord.__init__(self, name, rtype, rclass, ttl)
        self._alias = alias
        return

    @property
    def alias(self):
        return self._alias

    def write(self, out: 'DnsPacketWriter') -> None:
        """
            Used in constructing an outgoing packet
        """
        out.write_name(self._alias)
        return

    def __eq__(self, other: DnsRecord) -> bool:
        """
            Tests equality on alias
        """
        # Call DnsRecord equality operator first because it can eliminate alot of equality checks early
        iseq = False
        if DnsRecord.__eq__(self, other):
            iseq = self._alias == other._alias
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
        other = self._alias
        strval = self.as_dns_string(other=other)
        return strval