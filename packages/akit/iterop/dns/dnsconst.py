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

from akit.xenum import DocIntEnum

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

class DnsFlags(enum.IntEnum):
    """
        Enumeration for the DNS record flags.
    """
    FLAGS_AA = 0x0400  # Authoritative answer
    FLAGS_TC = 0x0200  # Truncated
    FLAGS_RD = 0x0100  # Recursion desired
    FLAGS_RA = 0x8000  # Recursion available

    FLAGS_Z =  0x0040   # Zero
    FLAGS_AD = 0x0020  # Authentic data
    FLAGS_CD = 0x0010  # Checking disabled

class DnsResponseFlags(enum.IntEnum):
    """
        Enumeration for the DNS response flags.
    """
    FLAGS_QR_MASK = 0x8000  # query response mask
    FLAGS_QR_QUERY = 0x0000  # query
    FLAGS_QR_RESPONSE = 0x8000  # response

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