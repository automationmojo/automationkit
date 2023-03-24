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

from akit.interop.dns.dnsconst import DnsFlags, DnsQr, DnsRecordType
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

class DnsInboundMessage:
    """
        The :class:`DnsInboundMessage` object is used to read incoming DNS packets.
    """

    def __init__(self, data: bytes) -> None:
        """
            Constructor from string holding bytes of packet
        """
        self._offset: int = 0

        self._data: bytes = data
        self._questions: List[DnsQuestion] = []
        self._answers: List[DnsRecord] = []
        self._id: int = 0
        self._flags: DnsFlags = None  # type: int
        self._num_questions: int = 0
        self._num_answers: int = 0
        self._num_authorities: int = 0
        self._num_additionals: int = 0
        self._valid: bool = False

        try:
            self._ingest_header()
            self._ingest_questions()
            self._ingest_others()

            self._valid = True

        except (IndexError, struct.error, DnsDecodeError):
            logger.exception('Choked at offset %d while unpacking %r', self._offset, data)

        return

    @property
    def answers(self) -> List[DnsRecord]:
        return self._answers

    @property
    def data(self) -> bytes:
        return self._data

    @property
    def flags(self) -> DnsFlags:
        return self._flags

    @property
    def id(self) -> int:
        return self._id

    @property
    def questions(self) -> List[DnsQuestion]:
        return self._questions

    def is_query(self) -> bool:
        """
            Returns true if this is a query
        """
        result = self.flags._qr == DnsQr.Query
        return result

    def is_response(self) -> bool:
        """
            Returns true if this is a response
        """
        result = self.flags._qr == DnsQr.Response
        return result

    def _ingest_header(self) -> None:
        """
            Processes the header portion of the message
        """

        self._id = struct.unpack(b'!H', self._data)[0]
        self._offset += 2

        flags_int = struct.unpack(b'!H', self._data)[0]
        self._offset += 2
        self._flags = DnsFlags.parse(flags_int)
        
        self._num_questions = struct.unpack(b'!H', self._data)[0]
        self._offset += 2

        self._num_answers = struct.unpack(b'!H', self._data)[0]
        self._offset += 2

        self._num_authorities = struct.unpack(b'!H', self._data)[0]
        self._offset += 2

        self._num_additionals = struct.unpack(b'!H', self._data)[0]
        self._offset += 2

        return

    def _ingest_questions(self) -> None:
        """
            Processes the questions section of the message
        """
        for i in range(self._num_questions):
            name = self._read_name()
            rtype, rclass = self._unpack(b'!HH')

            question = DnsQuestion(name, rtype, rclass)
            self._questions.append(question)
        return
    
    def _ingest_others(self) -> None:
        """
            Processes the answers, authorities and additionals section of the message
        """
        n = self._num_answers + self._num_authorities + self._num_additionals
        for i in range(n):
            domain = self._read_name()
            rtype, rclass, ttl, length = self._unpack(b'!HHiH')

            rec = None  # type: Optional[DnsRecord]
            if rtype == DnsRecordType.A:
                rec = DnsAddress(domain, rtype, rclass, ttl, self._read_string_characters(4))
            elif rtype == DnsRecordType.CNAME or rtype == DnsRecordType.PTR:
                rec = DnsPointer(domain, rtype, rclass, ttl, self._read_name())
            elif rtype == DnsRecordType.TXT:
                rec = DnsText(domain, rtype, rclass, ttl, self._read_string(length))
            elif rtype == DnsRecordType.SRV:
                rec = DnsService(
                    domain,
                    rtype,
                    rclass,
                    ttl,
                    self._read_unsigned_short(),
                    self._read_unsigned_short(),
                    self._read_unsigned_short(),
                    self._read_name(),
                )
            elif rtype == DnsRecordType.HINFO:
                rec = DnsHostInfo(
                    domain,
                    rtype,
                    rclass,
                    ttl,
                    self._read_string().decode('utf-8'),
                    self._read_string().decode('utf-8'),
                )
            elif rtype == DnsRecordType.AAAA:
                rec = DnsAddress(domain, rtype, rclass, ttl, self._read_string_characters(16))
            else:
                # Try to ignore types we don't know about
                # Skip the payload for the resource record so the next
                # records can be parsed correctly
                self._offset += length

            if rec is not None:
                self.answers.append(rec)
        return

    def _read_name(self) -> str:
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
                result = ''.join((result, self._read_utf(off, length) + '.'))
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

    def _read_string(self) -> bytes:
        """
            Reads a character string from the packet
        """
        length = int(self._data[self._offset])
        self._offset += 1

        strval = self._read_string_characters(length)

        return strval

    def _read_string_characters(self, length: int) -> bytes:
        """
            Reads a string of a given length from the packet
        """
        strval = self._data[self._offset : self._offset + length]
        self._offset += length
        return strval

    def _read_unsigned_int(self):
        """
            Reads an integer from the packet
        """
        # Unpack 4 bytes as unsigned int using network byte order !I
        val = int(self._unpack(b'!I')[0])
        self._offset += 4
        return val

    def _read_unsigned_short(self) -> int:
        """
            Reads an unsigned short from the packet
        """
        # Unpack 2 bytes as unsigned short using network byte order !H
        val = int(self._unpack(b'!H')[0])
        self._offset += 2
        return val

    def _read_utf(self, offset: int, length: int) -> str:
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
        strval = '<DnsInboundMessage:{%s}>' % ', '.join(
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
