"""
.. module:: constants
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains constants associated with network activities from the test framework.

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

import platform
import socket

HTTP1_1_LINESEP = b"\r\n"
HTTP1_1_END_OF_HEADER = b"\r\n\r\n"
HTTP1_1_END_OF_MESSAGE = b"\r\n\r\n"

if hasattr(socket, "IPPROTO_IPV6"):
    IPPROTO_IPV6 = socket.IPPROTO_IPV6
else:
    # Sigh: https://bugs.python.org/issue29515
    IPPROTO_IPV6 = 41

MDNS_GROUP_ADDR = '224.0.0.251'
MDNS_GROUP_ADDR6 = 'ff02::fb'

MDNS_PORT = 5353


UPNP_GROUP_ADDR = '239.255.255.250'

UPNP_GROUP_LOCAL_ADDR6 = 'FF02::1'
UPNP_GROUP_SITE_ADDR6 = 'FF05::1'
UPNP_GROUP_ORG_ADDR6 = 'FF08::1'
UPNP_GROUP_GLOBAL_ADDR6 = 'FF0E::1'

UPNP_PORT = 1900

if hasattr(socket, "SO_RECV_ANYIF"):
    SO_RECV_ANYIF = socket.SO_RECV_ANYIF
else:
    # https://opensource.apple.com/source/xnu/xnu-4570.41.2/bsd/sys/socket.h
    SO_RECV_ANYIF = 0x1104

class AKitHttpHeaders:
    USER_AGENT = "AutomationKit/1.0 Automation Kit Test Framework"
    SERVER = "{},{},AutomationKit/1.0".format(platform.system(), platform.release())