"""
.. module:: dnsrecord
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsRecord object which serves as the base object type for other DNS record types.

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

from typing import Optional, Union, cast, TYPE_CHECKING

import socket
import time

from akit.exceptions import AKitAbstractMethodError

from akit.networking.interfaces import is_ipv6_address
from akit.interop.dns.dnsconst import DnsLiftimePercent

from akit.xtime import current_time_millis

from akit.interop.dns.dnsconst import DnsRecordClass
from akit.interop.dns.dnsconst import DnsRecordType

if TYPE_CHECKING:
    from akit.interop.dns.dnsincoming import DnsIncoming
    from akit.interop.dns.dnspacketwriter import DnsPacketWriter

class DnsRecord:
    """
        A DNS record is a DNS entry that has a Time To Live or TTL attached.

                                         1  1  1  1  1  1
           0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                                               |
        /                                               /
        /                      NAME                     /
        |                                               |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                      TYPE                     |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                     CLASS                     |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                      TTL                      |
        |                                               |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                   RDLENGTH                    |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
        /                     RDATA                     /
        /                                               /
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

    """
    def __init__(self, name: str, rtype: DnsRecordType, rclass: DnsRecordClass, ttl: Union[float, int]) -> None:
        self._key = name.lower()
        self._name = name
        self._rtype = rtype
        self._rclass = (rclass & DnsRecordClass.MASK)
        self._ttl = ttl

        self._unique = (rclass & DnsRecordClass.UNIQUE) != 0
        self._updated = current_time_millis()

        self._when_expires = self._compute_time_marker(DnsLiftimePercent.Expired)
        self._when_refresh = self._compute_time_marker(DnsLiftimePercent.Refresh)
        self._when_stale = self._compute_time_marker(DnsLiftimePercent.Stale)
        return

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @property
    def rclass(self):
        return self._rclass

    @property
    def rtype(self):
        return self._rtype

    @property
    def ttl(self):
        return self._ttl

    @property
    def unique(self):
        return self._unique

    @property
    def updated(self):
        return self._updated

    def as_dns_string(self, other: Optional[str] = None) -> str:
        """
            Creates a DNS string representation of the DNS record.
        """
        remaining_ttl = int(self.get_remaining_ttl(current_time_millis()))
        other = "%s/%s,%s" % (self.ttl, remaining_ttl, other)
        
        dnsstr = "%s[%s,%s" % ('record', self._rtype.name, self._rclass.name)

        if self._unique:
            dnsstr += "-unique,"
        else:
            dnsstr += ","

        dnsstr += self._name

        if other is not None:
            dnsstr += "]=%s" % other
        else:
            dnsstr += "]"

        return dnsstr

    def get_remaining_ttl(self, now: float) -> float:
        """
            Gets the remaining time to live (TTL) in seconds.
        """
        rval = max(0, (self._when_expires - now) / 1000)
        return rval

    def is_expired(self, now: Optional[float]) -> bool:
        """
            Returns true if this record is expired.
        """
        if now is None:
            now = time.time()

        bval = self._when_expires <= now
        return bval

    def is_stale(self, now: Optional[float]) -> bool:
        """
            Returns true if this record is stale.
        """
        if now is None:
            now = time.time()

        bval = self._when_stale <= now
        return bval

    def suppressed_by(self, msg: 'DnsIncoming') -> bool:
        """
            Returns true if any answer in a message can suffice for the information held in this
            record.
        """
        rtn_val = False
        for record in msg.answers:
            if self.suppressed_by_answer(record):
                rtn_val = True
                break
        return rtn_val

    def suppressed_by_answer(self, other: 'DnsRecord') -> bool:
        """
            Returns true if another record has same name, type and class, and if its TTL is at least
            half of this record's.
        """
        rtnval = self == other and other.ttl > (self.ttl / 2)
        return rtnval

    def update_ttl(self, other: 'DnsRecord') -> None:
        """
            Updates the time to live TTL from the specified record.
        """
        self._updated = other._updated
        self._ttl = other._ttl
        self._when_expires = self._compute_time_marker(DnsLiftimePercent.Expired)
        self._when_refresh = self._compute_time_marker(DnsLiftimePercent.Refresh)
        self._when_stale = self._compute_time_marker(DnsLiftimePercent.Stale)
        return

    def write(self, out: 'DnsPacketWriter') -> None:
        """
            Abstract method
        """
        raise AKitAbstractMethodError from None

    def _compute_time_marker(self, percent: int) -> float:
        marker = self._updated + (percent * self._ttl * 10)
        return marker

    def __eq__(self, other: 'DnsRecord') -> bool:
        """
            Equality test on name, record type, and record class
        """
        iseq = False
        if isinstance(other, type(self)):
            if self._rtype == other._rtype and self._rclass and other._rclass:
                iseq = self._name == other._name
        return iseq

    def __ne__(self, other: 'DnsRecord') -> bool:
        """
            Non-equality test
        """
        isne = not self.__eq__(other)
        return isne

    def __str__(self) -> str:
        """
            String representation
        """
        dnsstr = self.as_dns_string()
        return dnsstr
