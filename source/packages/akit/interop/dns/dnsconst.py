"""
.. module:: dnsconst
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the constants that are used in association with multicast DNS.

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

import enum
import re

DNS_SIZE_SIGNED_CHAR = 1
DNS_SIZE_SIGNED_SHORT = 2
DNS_SIZE_SIGNED_INTEGER = 4

DNS_SIZE_UNSIGNED_CHAR = 1
DNS_SIZE_UNSIGNED_SHORT = 2
DNS_SIZE_UNSIGNED_INTEGER = 4

DNS_PACK_FORMAT_SHORT = "!H"
DNS_PACK_FORMAT_INTEGER = "!I"


@enum.unique
class DnsLiftimePercent(enum.IntEnum):
    """
        Enumeration for the DNS lifetime percentage states.
    """
    Expired = 100
    Stale = 50
    Refresh = 75


@enum.unique
class DnsQuestionType(enum.IntEnum):
    """
        The MDNS question type.

        "QU" - questions requesting unicast responses.
        "QM" - questions requesting multicast responses.
    """
    QU=1
    QM=2


@enum.unique
class DnsRecordClass(enum.IntEnum):
    """
        Enumeration for the DNS record class.
    """
    IN = 1 # The internet
    CS = 2 # The CSNET class
    CH = 3 # The CHAOS class
    HS = 4 # Hesiod

    NONE = 254
    ANY = 255
    MASK = 0x7FFF
    UNIQUE = 0x8000


@enum.unique
class DnsRecordType(enum.IntEnum):
    """
        Enumeration for the DNS record types.
    """
    A = 1 #,              "RFC 1035 - Address Record"
    NS = 2 #,             "RFC 1035 - Name server record"
    MD = 3 #,             "RFC 833 - Mail Destination"
    MF = 4 #,             "RFC 833 - Mail Forwarder"
    CNAME = 5 #,          "RFC 1035 - Conanical record name"
    SOA = 6 #,            "RFC 1035,2308 - Start of [a zone of] authority record"
    MB = 7 #,             "RFC 833 - Mailbox Binding"
    MG = 8 #,             "RFC 833 - Mail Group"
    MR = 9 #,             "RFC 833 - Mail Rename"
    NULL = 10 #,          "RFC 1035 - Null record or placeholder"
    WKS = 11 #,           "RFC 1035 - Well Known Service"
    PTR = 12 #,           "RFC 1035 - PTR Resource Record"
    HINFO = 13 #,         "RFC 8482 - Host Information"
    MINFO = 14 #,         "RFC 1035 - Mail Information Record"
    MX = 15 #,            "RFC 1035,7505 - Mail exchange record"
    TXT = 16 #,           "RFC 1035 - Text record"
    RP = 17 #,            "RFC 1183 - Responsible Person"
    AFSDB = 18 #,         "RFC 1183 - AFS database record"
    SIG = 24 #,           "RFC 2535 - Signature"
    KEY = 25 #,           "RFC 2535,2930 - Key record"
    AAAA = 28 #,          "RFC 3596 - IPv6 Address Record"
    LOC = 29 #,           "RFC 1876 - Location record"
    SRV = 33 #,           "RFC 2782 - Service locator"
    NAPTR = 35 #,         "RFC 3403 - Naming Authority Pointer"
    KX = 36 #,            "RFC 2230 - Key Exchanger record"
    CERT = 37 #,          "RFC 4398 - Certificate record"
    DNAME = 39 #,         "RFC 6672 - Delegation name record"
    APL = 42 #,           "RFC 3123 - Address Prefix List"
    DS = 43 #,            "RFC 4034 - Delegation signer"
    SSHFP = 44 #,         "RFC 4255 - SSH Public Key Fingerprint"
    IPSECKEY = 45 #,      "RFC 4025 - IPsec Key"
    RRSIG = 46 #,         "RFC 4034 - DNSSEC signature"
    NSEC = 47 #,          "RFC 4034 - Next Secure record"
    DNSKEY = 48 #,        "RFC 4034 - DNS Key record"
    DHCID = 49 #,         "RFC 4701 - DHCP identifier"
    NSEC3 = 50 #,         "RFC 5155 - Next Secure record version 3"
    NSEC3PARAM = 51 #,    "RFC 5155 - NSEC3 parameters"
    TLSA = 52 #,          "RFC 6698 - TLSA certificate association"
    SMIMEA = 53 #,        "RFC 8162 - S/MIME cert association"
    HIP = 55 #,           "RFC 8005 - Host Identity Protocol"
    CDS = 59 #,           "RFC 7344 - Child copy of DS record, for transfer to parent"
    CDNSKEY = 60 #,       "RFC 7344 - Child copy of DNSKEY record, for transfer to parent"
    OPENPGPKEY = 61 #,    "RFC 7929 - OpenPGP public key record"
    CSYNC = 62 #,         "RFC 7477 - Child-to-Parent Synchronization"
    ZONEMD = 63 # 
    SVCB = 64 #,          "RFC ???? - Service Binding"
    HTTPS = 65 #,         "RFC ???? - HTTPS Binding"
    EUI48 = 108 #,        "RFC 7043 - MAC address (EUI-48)"
    EUI64 = 109 #,        "RFC 7043 - MAC address (EUI-64)"
    TKEY = 249 #,         "RFC 2930 - Transaction Key record"
    TSIG = 250 #,         "RFC 2845 - Transaction Signature"
    AXFR = 252 #,         "RFC 1035 - Zone transfer request"
    MAILB = 253 #,        "RFC 1035 - Request for mailbox related methods"
    MAILA = 254 #,        "RFC 1035 - Request for mail agent related records"
    ANY = 255 #,          "RFC 1035 - Any class query class"
    URI = 256 #,          "RFC 7553 - Uniform Resource Identifier"
    CAA = 257 #,          "RFC 6844 - Certification Authority Authorization"
    TA = 32768 #,         "RFC ???? - DNSSEC Trust Authorities"
    DLV = 32769 #,        "RFC 4431 - DNSSEC Lookaside Validation record"


@enum.unique
class DnsQr(enum.IntEnum):
    Query = 0
    Response = 1


@enum.unique
class DnsOpCode(enum.IntEnum):
    Query = 0    # RFC1035
    IQuery = 1   # RFC3425
    Status = 2   # RFC1035
                 # 3 is available
    Notify = 4   # RFC1996
    Update = 5   # RFC2136


@enum.unique
class DnsRespCode(enum.IntEnum):
    NoError = 0
    FormatError = 1
    ServerError = 2
    NameError = 3
    Refused = 5


class DnsFlags:
    """
        Note: The bits are in order specified below

           1  1  1  1  1  1
           5  4  3  2  1  0  9  8  7  6  5  4  3  2  1  0
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
          |   RCODE   |   Z    |RA|RD|TC|AA|   Opcode  |QR|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 
    """

    def __init__(self, *, qr: DnsQr, opcode: DnsOpCode, aa: bool, tc: bool, rd: bool, ra: bool, rcode: DnsRespCode, z: int=0):
        """
            Sets the flags for the DNS header.

            :param qr: Indicates if the message is a query or a response
            :param opcode: Specifies the opcode for the message
            :param aa: Specifies that the message is an authoritative answer
            :param tc: Specifies that the message is truncated
            :param rd: Specifies that recursion is desired (set in queries only)
            :param ra: Specifies that recursion is available (set in responses only)
            :param rcode: The response code associated with the message
            :param z: Not used, should be zero

        """
        self._qr = qr
        self._opcode = opcode
        self._aa = aa
        self._tc = tc
        self._rd = rd
        self._ra = ra
        self._rcode = rcode
        self._z = z
        self._flags = 
        return

    @property
    def flags(self) -> int:
        """
            Converts a :class:`DnsFlags` object to a flags integer.
        """
        
        flags: int = (self._rcode << 12) & 0xF000
        flags |= (self._z << 9) & 0x0E00
        flags |= (int(self._ra) << 8) & 0x0100
        flags |= (int(self._rd) << 7) & 0x0080
        flags |= (int(self._tc) << 6) & 0x0040
        flags |= (int(self._aa) << 5) & 0x0020
        flags |= (self._opcode << 1) & 0x001E
        flags |= self._qr & 0x0001

        return flags

    def _compile_flags(self):
        return

    @classmethod
    def parse(flags: int) -> "DnsFlags":
        """
            Parses a flags integer and converts it to a :class:`DnsFlags` object.
        """
        rcode = DnsRespCode((flags & 0xF000) >> 12)
        z = int((flags & 0x0E00) >> 9)
        ra = True if (flags & 0x0100) >> 8 else False
        rd = True if (flags & 0x0080) >> 7 else False 
        tc = True if (flags & 0x0040) >> 6 else False 
        aa = True if (flags & 0x0020) >> 5 else False 
        opcode = DnsOpCode((flags & 0x001E) >> 1)  
        qr = DnsQr(flags & 0x0001)

        fobj = DnsFlags(qr=qr, opcode=opcode, aa=aa, tc=tc, rd=rd, ra=ra, rcode=rcode, z=z)

        return fobj

MDNS_IPV4_QUERY_1 = "\x01\x00\x5e\x00\x00\xfb\xf4\x28\x53\x0f\x43\x6d\x08\x00\x45\x00" \
    "\x00\x77\x9d\xdf\x40\x00\xff\x11\x4f\x41\xac\x10\x01\x49\xe0\x00" \
    "\x00\xfb\x14\xe9\x14\xe9\x00\x63\x02\xbb\x00\x00\x00\x00\x00\x01" \
    "\x00\x01\x00\x00\x00\x00\x08\x5f\x73\x63\x61\x6e\x6e\x65\x72\x04" \
    "\x5f\x74\x63\x70\x05\x6c\x6f\x63\x61\x6c\x00\x00\x0c\x00\x01\xc0" \
    "\x0c\x00\x0c\x00\x01\x00\x00\x11\x94\x00\x2a\x27\x48\x50\x20\x43" \
    "\x6f\x6c\x6f\x72\x20\x4c\x61\x73\x65\x72\x4a\x65\x74\x20\x50\x72" \
    "\x6f\x20\x4d\x34\x37\x38\x66\x2d\x39\x66\x20\x5b\x38\x33\x34\x42" \
    "\x41\x42\x5d\xc0\x0c"

MDNS_IPV4_QUERY_2 = "\x01\x00\x5e\x00\x00\xfb\x48\xa6\xb8\xb0\x06\x24\x08\x00\x45\x00" \
    "\x02\x70\x68\xea\x40\x00\xff\x11\x82\x54\xac\x10\x01\x32\xe0\x00" \
    "\x00\xfb\x14\xe9\x14\xe9\x02\x5c\x62\x26\x00\x00\x84\x00\x00\x00" \
    "\x00\x01\x00\x00\x00\x06\x06\x5f\x73\x6f\x6e\x6f\x73\x04\x5f\x74" \
    "\x63\x70\x05\x6c\x6f\x63\x61\x6c\x00\x00\x0c\x00\x01\x00\x00\x11" \
    "\x94\x00\x27\x24\x53\x6f\x6e\x6f\x73\x2d\x34\x38\x41\x36\x42\x38" \
    "\x42\x30\x30\x36\x32\x34\x40\x44\x69\x6e\x69\x6e\x67\x20\x52\x6f" \
    "\x6f\x6d\x20\x28\x41\x72\x63\x29\xc0\x0c\xc0\x29\x00\x10\x80\x01" \
    "\x00\x00\x11\x94\x01\x7c\x32\x69\x6e\x66\x6f\x3d\x2f\x61\x70\x69" \
    "\x2f\x76\x31\x2f\x70\x6c\x61\x79\x65\x72\x73\x2f\x52\x49\x4e\x43" \
    "\x4f\x4e\x5f\x34\x38\x41\x36\x42\x38\x42\x30\x30\x36\x32\x34\x30" \
    "\x31\x34\x30\x30\x2f\x69\x6e\x66\x6f\x06\x76\x65\x72\x73\x3d\x35" \
    "\x3b\x70\x72\x6f\x74\x6f\x76\x65\x72\x73\x3d\x31\x2e\x33\x34\x2e" \
    "\x30\x2d\x61\x6c\x70\x68\x61\x2e\x37\x2d\x31\x31\x2d\x67\x35\x36" \
    "\x33\x34\x64\x35\x63\x64\x2b\x62\x38\x34\x30\x62\x39\x64\x64\x35" \
    "\x65\x2e\x37\x33\x2e\x30\x2d\x33\x39\x30\x32\x30\x13\x6d\x69\x6e" \
    "\x41\x70\x69\x56\x65\x72\x73\x69\x6f\x6e\x3d\x31\x2e\x31\x2e\x30" \
    "\x0b\x62\x6f\x6f\x74\x73\x65\x71\x3d\x39\x34\x38\x25\x68\x68\x69" \
    "\x64\x3d\x53\x6f\x6e\x6f\x73\x5f\x6f\x58\x64\x77\x4c\x58\x6f\x4a" \
    "\x41\x77\x79\x6d\x4a\x58\x67\x7a\x6e\x4c\x33\x58\x73\x66\x45\x70" \
    "\x37\x76\x3b\x6d\x68\x68\x69\x64\x3d\x53\x6f\x6e\x6f\x73\x5f\x6f" \
    "\x58\x64\x77\x4c\x58\x6f\x4a\x41\x77\x79\x6d\x4a\x58\x67\x7a\x6e" \
    "\x4c\x33\x58\x73\x66\x45\x70\x37\x76\x2e\x59\x63\x4e\x49\x53\x46" \
    "\x74\x77\x77\x5a\x74\x78\x6b\x38\x79\x4e\x67\x53\x43\x47\x3b\x6c" \
    "\x6f\x63\x61\x74\x69\x6f\x6e\x3d\x68\x74\x74\x70\x3a\x2f\x2f\x31" \
    "\x37\x32\x2e\x31\x36\x2e\x31\x2e\x35\x30\x3a\x31\x34\x30\x30\x2f" \
    "\x78\x6d\x6c\x2f\x64\x65\x76\x69\x63\x65\x5f\x64\x65\x73\x63\x72" \
    "\x69\x70\x74\x69\x6f\x6e\x2e\x78\x6d\x6c\x0c\x73\x73\x6c\x70\x6f" \
    "\x72\x74\x3d\x31\x34\x34\x33\x0e\x68\x68\x73\x73\x6c\x70\x6f\x72" \
    "\x74\x3d\x31\x38\x34\x33\x09\x76\x61\x72\x69\x61\x6e\x74\x3d\x32" \
    "\x0e\x6d\x64\x6e\x73\x73\x65\x71\x75\x65\x6e\x63\x65\x3d\x30\x12" \
    "\x77\x73\x73\x3d\x2f\x77\x65\x62\x73\x6f\x63\x6b\x65\x74\x2f\x61" \
    "\x70\x69\x12\x53\x6f\x6e\x6f\x73\x2d\x34\x38\x41\x36\x42\x38\x42" \
    "\x30\x30\x36\x32\x34\xc0\x18\x00\x01\x80\x01\x00\x00\x00\x78\x00" \
    "\x04\xac\x10\x01\x32\xc1\xd8\x00\x1c\x80\x01\x00\x00\x00\x78\x00" \
    "\x10\xfe\x80\x00\x00\x00\x00\x00\x00\x4a\xa6\xb8\xff\xfe\xb0\x06" \
    "\x24\xc0\x29\x00\x21\x80\x01\x00\x00\x00\x78\x00\x08\x00\x00\x00" \
    "\x00\x05\xa3\xc1\xd8\xc0\x29\x00\x2f\x80\x01\x00\x00\x11\x94\x00" \
    "\x09\xc0\x29\x00\x05\x00\x00\x80\x00\x40\xc1\xd8\x00\x2f\x80\x01" \
    "\x00\x00\x00\x78\x00\x08\xc1\xd8\x00\x04\x40\x00\x00\x08"



EXPIRE_FULL_TIME_PERCENT = 100
EXPIRE_STALE_TIME_PERCENT = 50
EXPIRE_REFRESH_TIME_PERCENT = 75

HAS_A_TO_Z = re.compile(r'[A-Za-z]')
HAS_ONLY_A_TO_Z_NUM_HYPHEN = re.compile(r'^[A-Za-z0-9\-]+$')
HAS_ONLY_A_TO_Z_NUM_HYPHEN_UNDERSCORE = re.compile(r'^[A-Za-z0-9\-\_]+$')
HAS_ASCII_CONTROL_CHARS = re.compile(r'[\x00-\x1f\x7f]')

MAX_MSG_TYPICAL = 1460  # unused
MAX_MSG_ABSOLUTE = 8966

class DnsKnownServiceTypes:
    AIRTUNES = "AirTunes Remote Audio"
    AIRPLAY = "_airplay._tcp"
    MICROSOFT_WINDOWS_NETWORK = "Microsoft Windows Network"
    SFTP = "SFTP File Transfer"
    SONOS = "_sonos._tcp"
    SPOTIFY_CONNECT = "_spotify-connect._tcp"
    SSH = "SSH Remote Terminal"
    VNC = "VNC Remote Access"
