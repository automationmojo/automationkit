"""
.. module:: dnsoutgoing
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the DnsOutgoing object which is used to write out DNS records of different types into
               a DNS packet.

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

from typing import Any, Dict, List, Optional, Tuple, Union

import struct

from enum import IntEnum

from akit.interop.dns.dnsconst import DnsRecordClass, DnsRecordType, MAX_MSG_ABSOLUTE, MAX_MSG_TYPICAL

from akit.interop.dns.dnserrors import DnsNamePartTooLongException
from akit.interop.dns.dnsquestion import DnsQuestion
from akit.interop.dns.dnsrecord import DnsRecord
from akit.interop.dns.dnspointer import DnsPointer

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

struct_int_to_byte = struct.Struct(">B")

class DnsPacketBuilderState(IntEnum):
    Initial = 0
    Finished = 1

class DnsPacketWriter:
    """
        The :class:`DnsPacketWriter` object is used to write outgoing DNS packets.
    """

    def __init__(self, flags: int, multicast: bool = True) -> None:
        """
        """
        self._finished = False
        self._id = 0
        self._multicast = multicast
        self._flags = flags
        self._packets_data: List[bytes] = [] 

        # these 3 are per-packet -- see also reset_for_next_packet()
        self._names: Dict[str, int] = {}  
        self._data: List[bytes] = []
        self._size = 12

        self._state = DnsPacketBuilderState.Initial

        self._questions: List[DnsQuestion] = []
        self._answers: List[Tuple[DnsRecord, float]] = [] 
        self._authorities: List[DnsPointer] = [] 
        self._additionals: List[DnsRecord] = []

    @property
    def additionals(self) -> List[DnsRecord]:
        return self._additionals

    @property
    def answers(self) -> List[Tuple[DnsRecord, float]]:
        return self._answers

    @property
    def authorities(self) -> List[DnsPointer] :
        return self._authorities

    @property
    def data(self) -> List[bytes]:
        return self._data

    @property
    def finished(self) -> bool:
        return self._finished

    @property
    def flags(self) -> int:
        return self._flags

    @property
    def id(self) -> int:
        return self._id

    @property
    def multicast(self) -> bool:
        return self._multicast

    @property
    def names(self) -> Dict[str, int]:
        return self._names

    @property
    def packets_data(self):
        return self._packets_data

    @property
    def questions(self) -> List[DnsQuestion]:
        return self._questions

    @property
    def size(self) -> int:
        return self._size

    @property
    def state(self) -> DnsPacketBuilderState:
        return self._state

    @staticmethod
    def is_type_unique(rtype: int) -> bool:
        rtnval = rtype == DnsRecordType.TXT or rtype == DnsRecordType.SRV or rtype == DnsRecordType.A or rtype == DnsRecordType.AAAA
        return rtnval

    def add_question(self, record: DnsQuestion) -> None:
        """
            Adds a question
        """
        self._questions.append(record)
        return

    def add_answer(self, inp: DnsIncoming, record: 'DnsRecord') -> None:
        """
            Adds an answer
        """
        if not record.suppressed_by(inp):
            self.add_answer_at_time(record, 0)
        return

    def add_additional_answer(self, record: 'DnsRecord') -> None:
        """
        Adds an additional answer

        From: RFC 6763, DNS-Based Service Discovery, February 2013

        12.  DNS Additional Record Generation

           DNS has an efficiency feature whereby a DNS server may place
           additional records in the additional section of the DNS message.
           These additional records are records that the client did not
           explicitly request, but the server has reasonable grounds to expect
           that the client might request them shortly, so including them can
           save the client from having to issue additional queries.

           This section recommends which additional records SHOULD be generated
           to improve network efficiency, for both Unicast and Multicast DNS-SD
           responses.

        12.1.  PTR Records

           When including a DNS-SD Service Instance Enumeration or Selective
           Instance Enumeration (subtype) PTR record in a response packet, the
           server/responder SHOULD include the following additional records:

           o  The SRV record(s) named in the PTR rdata.
           o  The TXT record(s) named in the PTR rdata.
           o  All address records (type "A" and "AAAA") named in the SRV rdata.

        12.2.  SRV Records

           When including an SRV record in a response packet, the
           server/responder SHOULD include the following additional records:

           o  All address records (type "A" and "AAAA") named in the SRV rdata.

        """
        self._additionals.append(record)
        return

    def add_answer_at_time(self, record: Optional['DnsRecord'], now: Union[float, int]) -> None:
        """
            Adds an answer if it does not expire by a certain time
        """
        if record is not None:
            if now == 0 or not record.is_expired(now):
                self._answers.append((record, now))
        return

    def add_authorative_answer(self, record: DnsPointer) -> None:
        """
            Adds an authoritative answer
        """
        self._authorities.append(record)
        return

    def packet(self) -> bytes:
        """
            Returns a bytestring containing the first packet's bytes.

            Generally, you want to use packets() in case the response does not fit in a single packet, but this
            exists for backward compatibility.
        """
        packets = self.packets()
        if len(packets) > 0:
            if len(packets[0]) > MAX_MSG_ABSOLUTE:
                # TODO: Filter this logging down to once per packet type or instance
                logger.warn(
                    "Created over-sized packet (%d bytes) %r", len(packets[0]), packets[0]
                )
            return packets[0]
        else:
            return b''

    def packets(self) -> List[bytes]:
        """
            Returns a list of bytestrings containing the packets' bytes

            No further parts should be added to the packet once this is done.  The packets are each restricted to
            _MAX_MSG_TYPICAL or less in length, except for the case of a single answer which will be written out to
            a single oversized packet no more than _MAX_MSG_ABSOLUTE in length (and hence will be subject to IP
            fragmentation potentially).
        """

        if self._state == self._state.finished:
            return self._packets_data

        answer_offset = 0
        authority_offset = 0
        additional_offset = 0

        # we have to at least write out the question
        first_time = True

        while (
            first_time
            or answer_offset < len(self._answers)
            or authority_offset < len(self._authorities)
            or additional_offset < len(self._additionals)
        ):
            first_time = False
            logger.debug("offsets = %d, %d, %d", answer_offset, authority_offset, additional_offset)
            logger.debug("lengths = %d, %d, %d", len(self._answers), len(self._authorities), len(self._additionals))

            additionals_written = 0
            authorities_written = 0
            answers_written = 0
            questions_written = 0

            for question in self._questions:
                self.write_question(question)
                questions_written += 1

            allow_long = True  # at most one answer is allowed to be a long packet
            for answer, time_ in self._answers[answer_offset:]:
                if self.write_record(answer, time_, allow_long):
                    answers_written += 1
                allow_long = False

            for authority in self._authorities[authority_offset:]:
                if self.write_record(authority, 0):
                    authorities_written += 1

            for additional in self._additionals[additional_offset:]:
                if self.write_record(additional, 0):
                    additionals_written += 1

            self._insert_short(0, additionals_written)
            self._insert_short(0, authorities_written)
            self._insert_short(0, answers_written)
            self._insert_short(0, questions_written)
            self._insert_short(0, self._flags)

            if self._multicast:
                self._insert_short(0, 0)
            else:
                self._insert_short(0, self._id)

            self._packets_data.append(b''.join(self._data))
            self._reset_for_next_packet()

            answer_offset += answers_written
            authority_offset += authorities_written
            additional_offset += additionals_written

            logger.debug("now offsets = %d, %d, %d", answer_offset, authority_offset, additional_offset)
            if (answers_written + authorities_written + additionals_written) == 0 and (
                len(self._answers) + len(self._authorities) + len(self._additionals)
            ) > 0:
                logger.warning("packets() made no progress adding records; returning")
                break

        self._state = self._state.finished

        return self._packets_data

    def write_byte(self, value: int) -> None:
        """
            Writes a single byte to the packet
        """
        # TODO: Optimize this
        self._pack(b'!c', struct_int_to_byte.pack(value))
        return

    def write_character_string(self, value: bytes) -> None:
        assert isinstance(value, bytes)
        length = len(value)
        if length > 256:
            raise DnsNamePartTooLongException
        self.write_byte(length)
        self.write_string(value)


    def write_int(self, value: Union[float, int]) -> None:
        """
            Writes an unsigned integer to the packet
        """
        self._pack(b'!I', int(value))
        return

    def write_name(self, name: str) -> None:
        """
            Write names to packet

            18.14. Name Compression

            When generating Multicast DNS messages, implementations SHOULD use
            name compression wherever possible to compress the names of resource
            records, by replacing some or all of the resource record name with a
            compact two-byte reference to an appearance of that data somewhere
            earlier in the message [RFC1035].
        """

        # split name into each label
        parts = name.split('.')
        if not parts[-1]:
            parts.pop()

        # construct each suffix
        name_suffices = ['.'.join(parts[i:]) for i in range(len(parts))]

        # look for an existing name or suffix
        for count, sub_name in enumerate(name_suffices):
            if sub_name in self._names:
                break
        else:
            count = len(name_suffices)

        # note the new names we are saving into the packet
        name_length = len(name.encode('utf-8'))
        for suffix in name_suffices[:count]:
            self._names[suffix] = self._size + name_length - len(suffix.encode('utf-8')) - 1

        # write the new names out.
        for part in parts[:count]:
            self.write_utf(part)

        # if we wrote part of the name, create a pointer to the rest
        if count != len(name_suffices):
            # Found substring in packet, create pointer
            index = self._names[name_suffices[count]]
            self.write_byte((index >> 8) | 0xC0)
            self.write_byte(index & 0xFF)
        else:
            # this is the end of a name
            self.write_byte(0)
        return

    def write_question(self, question: DnsQuestion) -> None:
        """
            Writes a question to the packet
        """
        self.write_name(question.name)
        self.write_short(question.type)
        self.write_short(question.rclass)
        return

    def write_record(self, record: 'DnsRecord', now: float, allow_long: bool = False) -> bool:
        """
            Writes a record (answer, authoritative answer, additional) to the packet.  Returns True on success, or False if
            we did not (either because the packet was already finished or because the record does not fit.)
        """
        if self._state == self._state.finished:
            return False

        start_data_length, start_size = len(self._data), self._size
        self.write_name(record.name)
        self.write_short(record.type)

        if record.unique and self._multicast:
            self.write_short(record.rclass | DnsRecordClass.UNIQUE)
        else:
            self.write_short(record.rclass)

        if now == 0:
            self.write_int(record.ttl)
        else:
            self.write_int(record.get_remaining_ttl(now))

        index = len(self._data)

        # Adjust size for the short we will write before this record
        self._size += 2
        record.write(self)
        self._size -= 2

        length = sum((len(d) for d in self._data[index:]))
        # Here is the short we adjusted for
        self._insert_short(index, length)

        len_limit = MAX_MSG_ABSOLUTE if allow_long else MAX_MSG_TYPICAL

        # if we go over, then rollback and quit
        if self._size > len_limit:
            while len(self._data) > start_data_length:
                self._data.pop()
            self._size = start_size
            return False

        return True

    def write_short(self, value: int) -> None:
        """
            Writes an unsigned short to the packet
        """
        self._pack(b'!H', value)
        return

    def write_bytes(self, buffer: bytes) -> None:
        """
            Writes a string to the packet
        """
        assert isinstance(buffer, bytes)
        self._data.append(buffer)
        self._size += len(buffer)
        return

    def write_utf(self, s: str) -> None:
        """
            Writes a UTF-8 string of a given length to the packet
        """
        bytes = s.encode('utf-8')
        length = len(utfstr)
        if length > 64:
            raise DnsNamePartTooLongException
        self.write_byte(length)
        self.write_string(bytes)
        return

    def _insert_short(self, index: int, value: int) -> None:
        """
            Inserts an unsigned short in a certain position in the packet
        """
        self._data.insert(index, struct.pack(b'!H', value))
        self._size += 2
        return

    def _pack(self, format_: Union[bytes, str], value: Any) -> None:
        self._data.append(struct.pack(format_, value))
        self._size += struct.calcsize(format_)
        return

    def _reset_for_next_packet(self) -> None:
        self._names = {}
        self._data = []
        self._size = 12
    
    def __str__(self) -> str:
        strval = '<DnsOutgoing:{%s}>' % ', '.join(
            [
                'multicast=%s' % self._multicast,
                'flags=%s' % self._flags,
                'questions=%s' % self._questions,
                'answers=%s' % self._answers,
                'authorities=%s' % self._authorities,
                'additionals=%s' % self._additionals,
            ]
        )
        return strval