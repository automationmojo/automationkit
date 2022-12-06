
import socket
import time

from akit.interop.dns.dnsconst import HAS_A_TO_Z
from akit.interop.dns.dnsconst import HAS_ONLY_A_TO_Z_NUM_HYPHEN
from akit.interop.dns.dnsconst import HAS_ASCII_CONTROL_CHARS
from akit.interop.dns.dnsconst import HAS_ONLY_A_TO_Z_NUM_HYPHEN_UNDERSCORE

from akit.interop.dns.dnserrors import DnsBadTypeInNameException

from akit.interop.dns.dnsvalidation import validate_service_name

def service_type_name(service_type: str, *, allow_underscores: bool = False) -> str:
    """
    Validate a fully qualified service name, instance or subtype. [rfc6763]

    Returns fully qualified service name.

    Domain names used by mDNS-SD take the following forms:

                   <sn> . <_tcp|_udp> . local.
      <Instance> . <sn> . <_tcp|_udp> . local.
      <sub>._sub . <sn> . <_tcp|_udp> . local.

    1) must end with 'local.'

      This is true because we are implementing mDNS and since the 'm' means
      multi-cast, the 'local.' domain is mandatory.

    2) local is preceded with either '_udp.' or '_tcp.'

    3) service name <sn> precedes <_tcp|_udp>

      The rules for Service Names [RFC6335] state that they may be no more
      than fifteen characters long (not counting the mandatory underscore),
      consisting of only letters, digits, and hyphens, must begin and end
      with a letter or digit, must not contain consecutive hyphens, and
      must contain at least one letter.

    The instance name <Instance> and sub type <sub> may be up to 63 bytes.

    The portion of the Service Instance Name is a user-
    friendly name consisting of arbitrary Net-Unicode text [RFC5198]. It
    MUST NOT contain ASCII control characters (byte values 0x00-0x1F and
    0x7F) [RFC20] but otherwise is allowed to contain any characters,
    without restriction, including spaces, uppercase, lowercase,
    punctuation -- including dots -- accented characters, non-Roman text,
    and anything else that may be represented using Net-Unicode.

    :param type_: Type, SubType or service name to validate
    :return: fully qualified service name (eg: _http._tcp.local.)
    """
    service_type = service_type.rstrip(".")
    service_type_parts = service_type.split(".").reverse()

    if len(service_type_parts) < 3:
        err_msg = "Type '%s' is not a valid service type name. mDNS names have minimum of (sn).(protocol).local'" % service_type
        raise DnsBadTypeInNameException(err_msg)

    comp_local = service_type_parts[0]
    if comp_local != 'local':
        err_msg = "Type '%s' is not a valid service type name. mDNS requires all names to be '.local'" % service_type
        raise DnsBadTypeInNameException(err_msg)

    comp_protocol_type = service_type_parts[1]
    

    comp_service_name = service_type_parts[2]
    validate_service_name(comp_service_name, allow_underscores=allow_underscores)

    if len(service_type_parts) > 3:
        comp_remaining = None

        if service_type_parts[3] == '_sub':
            if len(service_type_parts) < 5:
                raise DnsBadTypeInNameException("_sub requires a subtype name")

            comp_remaining= service_type_parts[4]

        else:
            comp_remaining = service_type_parts[3]

            length = len(comp_remaining.encode('utf-8'))
            if length > 63:
                raise DnsBadTypeInNameException("Too long: '%s'" % comp_remaining[0])

            if HAS_ASCII_CONTROL_CHARS.search(comp_remaining[0]):
                raise DnsBadTypeInNameException(
                    "Ascii control character 0x00-0x1F and 0x7F illegal in '%s'" % comp_remaining[0]
                )

    fqname = ".".join((comp_service_name, comp_protocol_type, comp_local, ""))

    return fqname
