"""
.. module:: dnsvalidation
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing method used to validate DNS record information in accordance
               with RFC6763.

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

from akit.interop.dns.dnsconst import HAS_A_TO_Z
from akit.interop.dns.dnsconst import HAS_ONLY_A_TO_Z_NUM_HYPHEN
from akit.interop.dns.dnsconst import HAS_ASCII_CONTROL_CHARS
from akit.interop.dns.dnsconst import HAS_ONLY_A_TO_Z_NUM_HYPHEN_UNDERSCORE

from akit.interop.dns.dnserrors import DnsBadTypeInNameException

def validate_service_name(service_name: str, allow_underscores: bool = False):
    """
        Validates a service name for a DNS service.  The service name must meet the following
        requirements as per RFC6335

        1. Must begin with an underscore character '_'
        2. MUST be at least 1 character and no more than 15 characters long (not counting the mandatory underscore)
        3. MUST contain only US-ASCII [ANSI.X3.4-1986] letters 'A' - 'Z' and
           'a' - 'z', digits '0' - '9', and hyphens ('-', ASCII 0x2D or
           decimal 45)
        4. MAY not use consecutive hyphen characters '-'.
        5. MAY not use the hyphen character '-' as the first character after the underscore.
    """

    if service_name[0] != '_':
        raise DnsBadTypeInNameException("Service name (%s) must start with '_'" % service_name)

    # remove leading underscore
    service_name = service_name[1:]

    if len(service_name) > 15:
        raise DnsBadTypeInNameException("Service name (%s) must be <= 15 bytes" % service_name)

    if '--' in service_name:
        raise DnsBadTypeInNameException("Service name (%s) must not contain '--'" % service_name)

    if '-' in (service_name[0], service_name[-1]):
        raise DnsBadTypeInNameException("Service name (%s) may not start or end with '-'" % service_name)

    if not HAS_A_TO_Z.search(service_name):
        raise DnsBadTypeInNameException("Service name (%s) must contain at least one letter (eg: 'A-Z')" % service_name)

    allowed_characters_re = (
        HAS_ONLY_A_TO_Z_NUM_HYPHEN_UNDERSCORE if allow_underscores else HAS_ONLY_A_TO_Z_NUM_HYPHEN
    )

    if not allowed_characters_re.search(service_name):
        raise DnsBadTypeInNameException(
            "Service name (%s) must contain only these characters: "
            "A-Z, a-z, 0-9, hyphen ('-')%s" % (service_name, ", underscore ('_')" if allow_underscores else "")
        )

    return
