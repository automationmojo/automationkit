"""
.. module:: dnstext
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsText objec which reprsents a DNS text record type.

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

class DnsText(DnsRecord):
    """
        A DNS text record
    """

    def __init__(self, name: str, rtype: int, rclass: int, ttl: int, text: bytes) -> None:
        assert isinstance(text, (bytes, type(None)))
        DnsRecord.__init__(self, name, rtype, rclass, ttl)
        self._text = text

    @property
    def text(self):
        return self._text

    def write(self, out: 'DnsPacketWriter') -> None:
        """
            Used in constructing an outgoing packet
        """
        out.write_string(self._text)

    def __eq__(self, other: DnsRecord) -> bool:
        """
            Tests equality on text
        """
        # Call DnsRecord equality operator first because it can eliminate alot of equality checks early
        iseq = False
        if DnsRecord.__eq__(self, other):
            iseq = self._text == other._text
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
        strval = None
        if len(self._text) > 10:
            strval = self.as_dns_string(self._text[:7]) + "..."
        else:
            strval = self.as_dns_string(self._text)
        return strval
