"""
.. module:: dnshostinfo
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsHostInfo object which provides a record type for host information.

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

class DnsHostInfo(DnsRecord):
    """
        A DNS host information record
    """

    def __init__(self, name: str, rtype: int, rclass: int, ttl: int, cpu: str, os: str) -> None:
        DnsRecord.__init__(self, name, rtype, rclass, ttl)
        self._cpu = cpu
        self._os = os
        return

    @property
    def cpu(self):
        return self._cpu

    @property
    def os(self):
        return self._os

    def write(self, out: 'DnsPacketWriter') -> None:
        """
            Used in constructing an outgoing packet
        """
        out.write_character_string(self._cpu.encode('utf-8'))
        out.write_character_string(self._os.encode('utf-8'))
        return

    def __eq__(self, other: DnsRecord) -> bool:
        """
            Tests equality on cpu and os
        """
        # Call DnsRecord equality operator first because it can eliminate alot of equality checks early
        iseq = False
        if DnsRecord.__eq__(self, other):
            iseq = self._cpu == other._cpu and self._os == other._os
        return iseq

    def __ne__(self, other: DnsRecord) -> bool:
        """
            Non-equality test
        """
        isne = not self.__eq__(other)
        return isne

    def __str__(self) -> str:
        """
            String representation
        """
        other = self._cpu + " " + self._os
        strval = self.as_dns_string(other=other)
        return strval
