"""
.. module:: dnsquestion
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsQuestion object which represents a DNS question to be posed to the DNS service.

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

import struct

from akit.interop.dns.dnsconst import DnsRecordClass, DnsRecordType
from akit.interop.dns.dnsrecord import DnsRecord

class DnsQuestion:
    """
        The :class:`DnsQuestion` object is utilized to formulate DNS querys and to check to
        see if a :class:`DnsRecord` answers the query provided.
    """
    def __init__(self, name: str, rtype: DnsRecordType, rclass: DnsRecordClass) -> None:
        self._name = name
        self._rtype = rtype
        self._rclass = DnsRecordClass(rclass & DnsRecordClass.MASK)
        self._unique = (rclass & DnsRecordClass.UNIQUE) != 0
        return

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
    def unique(self):
        return self._unique

    def answered_by(self, rec: DnsRecord) -> bool:
        """
            Returns true if the question is answered by the record.
        """
        bval = False
        if self._rclass == rec._rclass:
            if self._rtype == rec._rtype or self._rtype == DnsRecordType.ANY:
               bval = self._name == rec._name
        return bval

    def as_query_bytes(self) -> str:
        """
            Formats the DNS question as a byte stream for transmission.
        """

        brtype = self._rtype.name.encode("utf-8")
        brclass = self._rclass.name.encode("utf-8")

        name_len = len(self._name)

        dnsstr = b"%s/x00%s,%s" % ('question', brtype, brclass)

        if self._unique:
            dnsstr += "-unique,"
        else:
            dnsstr += ","

        dnsstr += self._name

        dnsbytes = dnsstr.encode("utf-8")

        return dnsbytes
