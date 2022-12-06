"""
.. module:: dnsincoming
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsIncoming object which is used to represent an incoming DNS packet and to provide
               methods for processing the packet.

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


from typing import cast, List, Optional

import struct

from akit.interop.dns.dnsconst import DnsRecordType, DnsResponseFlags
from akit.interop.dns.dnserrors import DnsDecodeError

from akit.interop.dns.dnsaddress import DnsAddress
from akit.interop.dns.dnshostinfo import DnsHostInfo
from akit.interop.dns.dnspointer import DnsPointer
from akit.interop.dns.dnsquestion import DnsQuestion
from akit.interop.dns.dnsrecord import DnsRecord
from akit.interop.dns.dnsservice import DnsService
from akit.interop.dns.dnstext import DnsText

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

class DnsPacketReader:
    """
        The :class:`DnsPacketReader` object is used to read incoming DNS packets.
    """

    def __init__(self, data: bytes) -> None:
        """
            Constructor from string holding bytes of packet
        """
        self._offset = 0

        self._data = data
        self._questions = []  # type: List[DnsQuestion]
        self._answers = []  # type: List[DnsRecord]
        self._id = 0
        self._flags = 0  # type: int
        self._num_questions = 0
        self._num_answers = 0
        self._num_authorities = 0
        self._num_additionals = 0
        self._valid = False

        try:
            self.read_header()
            self.read_questions()
            self.read_others()

            self._valid = True

        except (IndexError, struct.error, DnsDecodeError):
            logger.exception('Choked at offset %d while unpacking %r', self._offset, data)

        return

    @property
    def answers(self):
        return self._answers

    @property
    def data(self):
        return self._data

    @property
    def flags(self):
        return self._flags

    @property
    def id(self):
        return self._id

    @property
    def questions(self):
        return self._questions

    def is_query(self) -> bool:
        """
            Returns true if this is a query
        """
        result = (self.flags & DnsResponseFlags.FLAGS_QR_MASK) == DnsResponseFlags.FLAGS_QR_QUERY
        return result

    def is_response(self) -> bool:
        """
            Returns true if this is a response
        """
        result = (self.flags & DnsResponseFlags.FLAGS_QR_MASK) == DnsResponseFlags.FLAGS_QR_RESPONSE
        return result

    def read_header(self) -> None:
        """
            Reads header portion of packet
        """
        self._id, self._flags, self._num_questions, self._num_answers, self._num_authorities, self._num_additionals = self._unpack(b'!6H')
        return

    def read_name(self) -> str:
        """
            Reads a domain name from the packet
        """
        result = ''
        off = self._offset
        next_ = -1
        first = off

        while True:
            length = self._data[off]
            off += 1
            if length == 0:
                break
            t = length & 0xC0
            if t == 0x00:
                result = ''.join((result, self.read_utf(off, length) + '.'))
                off += length
            elif t == 0xC0:
                if next_ < 0:
                    next_ = off + 1
                off = ((length & 0x3F) << 8) | self._data[off]
                if off >= first:
                    raise DnsDecodeError("Bad domain name (circular) at %s" % (off,))
                first = off
            else:
                raise DnsDecodeError("Bad domain name at %s" % (off,))

        if next_ >= 0:
            self._offset = next_
        else:
            self._offset = off

        return result

    def read_others(self) -> None:
        """
            Reads the answers, authorities and additionals section of the packet
        """
        n = self._num_answers + self._num_authorities + self._num_additionals
        for i in range(n):
            domain = self.read_name()
            rtype, rclass, ttl, length = self._unpack(b'!HHiH')

            rec = None  # type: Optional[DnsRecord]
            if rtype == DnsRecordType.A:
                rec = DnsAddress(domain, rtype, rclass, ttl, self.read_string(4))
            elif rtype == DnsRecordType.CNAME or rtype == DnsRecordType.PTR:
                rec = DnsPointer(domain, rtype, rclass, ttl, self.read_name())
            elif rtype == DnsRecordType.TXT:
                rec = DnsText(domain, rtype, rclass, ttl, self.read_string(length))
            elif rtype == DnsRecordType.SRV:
                rec = DnsService(
                    domain,
                    rtype,
                    rclass,
                    ttl,
                    self.read_unsigned_short(),
                    self.read_unsigned_short(),
                    self.read_unsigned_short(),
                    self.read_name(),
                )
            elif rtype == DnsRecordType.HINFO:
                rec = DnsHostInfo(
                    domain,
                    rtype,
                    rclass,
                    ttl,
                    self.read_character_string().decode('utf-8'),
                    self.read_character_string().decode('utf-8'),
                )
            elif rtype == DnsRecordType.AAAA:
                rec = DnsAddress(domain, rtype, rclass, ttl, self.read_string(16))
            else:
                # Try to ignore types we don't know about
                # Skip the payload for the resource record so the next
                # records can be parsed correctly
                self._offset += length

            if rec is not None:
                self.answers.append(rec)
        return

    def read_questions(self) -> None:
        """
            Reads questions section of packet
        """
        for i in range(self._num_questions):
            name = self.read_name()
            rtype, rclass = self._unpack(b'!HH')

            question = DnsQuestion(name, rtype, rclass)
            self._questions.append(question)
        return

    def read_string(self) -> bytes:
        """
            Reads a character string from the packet
        """
        length = int(self._data[self._offset])
        self._offset += 1

        strval = self.read_string_characters(length)

        return strval

    def read_string_characters(self, length: int) -> bytes:
        """
            Reads a string of a given length from the packet
        """
        strval = self._data[self._offset : self._offset + length]
        self._offset += length
        return strval

    def read_unsigned_int(self):
        """
            Reads an integer from the packet
        """
        # Unpack 4 bytes as unsigned int using network byte order !I
        val = int(self._unpack(b'!I')[0])
        self._offset += 4
        return val

    def read_unsigned_short(self) -> int:
        """
            Reads an unsigned short from the packet
        """
        # Unpack 2 bytes as unsigned short using network byte order !H
        val = int(self._unpack(b'!H')[0])
        self._offset += 2
        return val

    def read_utf(self, offset: int, length: int) -> str:
        """
            Reads a UTF-8 string of a given length from the packet
        """
        utfval = str(self._data[offset : offset + length], 'utf-8', 'replace')
        return utfval

    def _unpack(self, format_: bytes) -> tuple:
        length = struct.calcsize(format_)
        info = struct.unpack(format_, self._data[self._offset : self._offset + length])
        self._offset += length
        return info

    def __str__(self) -> str:
        strval = '<DnsIncoming:{%s}>' % ', '.join(
            [
                'id=%s' % self._id,
                'flags=%s' % self._flags,
                'n_q=%s' % self._num_questions,
                'n_ans=%s' % self._num_answers,
                'n_auth=%s' % self._num_authorities,
                'n_add=%s' % self._num_additionals,
                'questions=%s' % self._questions,
                'answers=%s' % self._answers,
            ]
        )
        return strval
