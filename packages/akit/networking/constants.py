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

class RegisteredMulticastAddresses:
    """
        https://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml
    """

    BASE = "224.0.0.0"                           # RFC 1112
    ALL_SYSTEMS_ON_SUBNET = "224.0.0.1"          # RFC 1112
    ALL_ROUTERS_ON_SUBNET = "224.0.0.2"
    UNASSIGNED_A = "224.0.0.3"
    DVMRP_ROUTERS = "224.0.0.4"                  # RFC 1075
    OSPFIGP_ALL_ROUTERS = "224.0.0.5"            # RFC 2328
    OSPFIGP_DESIGNATED_ROUTERS = "224.0.0.6"     # RFC 2328
    ST_ROUTERS = "224.0.0.7"                     # RFC 1190
    ST_HOSTS = "224.0.0.8"                       # RFC 1190
    RIP2_ROUTERS = "224.0.0.9"                   # RFC 1723
    EIGRP_ROUTERS = "224.0.0.10"                 # RFC 7868
    MOBILE_AGENTS = "224.0.0.11"
    DHCP_SERVER_OR_AGENT = "224.0.0.12"
    ALL_PIM_ROUTERS = "224.0.0.13"
    RSVP_ENCAPSULATION = "224.0.0.14"
    ALL_CBT_ROUTERS = "224.0.0.15"
    DESIGNATED_SBM = "224.0.0.16"
    ALL_SBMS = "224.0.0.17"
    VRRP = "224.0.0.18"
    IPAll_L1_ISs = "224.0.0.19"
    IPAll_L2_ISs = "224.0.0.20"
    IPAll_INTERMEDIATE_SYSTEMS = "224.0.0.21"
    IGMP = "224.0.0.22"
    GLOBECAST_ID = "224.0.0.23"
    OSPFIGP_TE = "224.0.0.24"
    ROUTER_TO_SWITCH = "224.0.0.25"
    UNASSIGNED_B = "224.0.0.26"
    AL_MPP_HELLO = "224.0.0.27"
    ETC_CONTROL = "224.0.0.28"
    GE_FANUC = "224.0.0.29"
    INDIGO_VHDP = "224.0.0.30"
    SHIN_BROAD_BAND = "224.0.0.31"
    DIGISTAR = "224.0.0.32"
    FF_SYSTEM_MANAGEMENT = "224.0.0.33"
    PT2_DISCOVER = "224.0.0.34"
    DXCLUSTER = "224.0.0.35"
    DTCP_ANNOUNCEMENT = "224.0.0.36"
    ZERO_CONF_ADDR = [
        "224.0.0.36", "224.0.0.37", "224.0.0.38", "224.0.0.39", "224.0.0.40",
        "224.0.0.41", "224.0.0.42", "224.0.0.43", "224.0.0.44", "224.0.0.45",
        "224.0.0.46", "224.0.0.47", "224.0.0.48", "224.0.0.49", "224.0.0.50",
        "224.0.0.51", "224.0.0.52", "224.0.0.53", "224.0.0.54", "224.0.0.55",
        "224.0.0.56", "224.0.0.57", "224.0.0.58", "224.0.0.59", "224.0.0.60",
        "224.0.0.61", "224.0.0.62", "224.0.0.63", "224.0.0.64", "224.0.0.65",
        "224.0.0.66", "224.0.0.67", "224.0.0.68"
    ],
    UNASSIGNED_C = [
        "224.0.0.69", "224.0.0.70", "224.0.0.71", "224.0.0.72", "224.0.0.73",
        "224.0.0.74", "224.0.0.75", "224.0.0.76", "224.0.0.77", "224.0.0.78",
        "224.0.0.79", "224.0.0.80", "224.0.0.81", "224.0.0.82", "224.0.0.83",
        "224.0.0.84", "224.0.0.85", "224.0.0.86", "224.0.0.87", "224.0.0.88",
        "224.0.0.89", "224.0.0.90", "224.0.0.91", "224.0.0.92", "224.0.0.93",
        "224.0.0.94", "224.0.0.95", "224.0.0.96", "224.0.0.97", "224.0.0.98",
        "224.0.0.99", "224.0.0.100"
    ],
    CISCO_NHAP = "224.0.0.101",
    HSRP = "224.0.0.102",
    MDAP = "224.0.0.103",
    NOKIA_MC_CH = "224.0.0.104"
    FF_LR_ADDRESS = "224.0.0.105"
    ALL_SNOOPERS = "224.0.0.106"
    PTP_PDELAY = "224.0.0.107"
    SARATOGA = "224.0.0.108"
    LL_MANET_ROUTERS = "224.0.0.109"
    IGRS = "224.0.0.110"
    BABEL = "224.0.0.111"
    MMA_DEVICE_DISCOVERY = "224.0.0.112"
    ALL_JOYN = "224.0.0.113"
    INTER_RFID_READER_PROTOCOL = "224.0.0.114"
    JSDP = "224.0.0.115"
    DEVICE_DISCOVERY = "224.0.0.116"
    DLEP_DISCOVERY = "224.0.0.117"
    MAAS = "224.0.0.118"
    ALL_GRASP_NEIGHBORS = "224.0.0.119"
    UNASSIGNED_D = [
        "224.0.0.120", "224.0.0.121", "224.0.0.122", "224.0.0.123", "224.0.0.124",
        "224.0.0.125", "224.0.0.126", "224.0.0.127", "224.0.0.128", "224.0.0.129",
        "224.0.0.130", "224.0.0.131", "224.0.0.132", "224.0.0.133", "224.0.0.134",
        "224.0.0.135", "224.0.0.136", "224.0.0.137", "224.0.0.138", "224.0.0.139",
        "224.0.0.140", "224.0.0.141", "224.0.0.142", "224.0.0.143", "224.0.0.144",
        "224.0.0.145", "224.0.0.146", "224.0.0.147", "224.0.0.148", "224.0.0.149"
    ]
    RAMP_ALTITUDE_CDN = "224.0.0.150"
    UNASSIGNED_E = [
        "224.0.0.151", "224.0.0.152", "224.0.0.153", "224.0.0.154", "224.0.0.155",
        "224.0.0.156", "224.0.0.157", "224.0.0.158", "224.0.0.159", "224.0.0.160",
        "224.0.0.161", "224.0.0.162", "224.0.0.163", "224.0.0.164", "224.0.0.165",
        "224.0.0.166", "224.0.0.167", "224.0.0.168", "224.0.0.169", "224.0.0.170",
        "224.0.0.171", "224.0.0.172", "224.0.0.173", "224.0.0.174", "224.0.0.175",
        "224.0.0.176", "224.0.0.177", "224.0.0.178", "224.0.0.179", "224.0.0.180",
        "224.0.0.181", "224.0.0.182", "224.0.0.183", "224.0.0.184", "224.0.0.185",
        "224.0.0.186", "224.0.0.187", "224.0.0.188", "224.0.0.189", "224.0.0.190",
        "224.0.0.191", "224.0.0.192", "224.0.0.193", "224.0.0.194", "224.0.0.195",
        "224.0.0.196", "224.0.0.197", "224.0.0.198", "224.0.0.199", "224.0.0.200",
        "224.0.0.201", "224.0.0.202", "224.0.0.203", "224.0.0.204", "224.0.0.205",
        "224.0.0.206", "224.0.0.207", "224.0.0.208", "224.0.0.209", "224.0.0.210",
        "224.0.0.211", "224.0.0.212", "224.0.0.213", "224.0.0.214", "224.0.0.215",
        "224.0.0.216", "224.0.0.217", "224.0.0.218", "224.0.0.219", "224.0.0.220",
        "224.0.0.221", "224.0.0.222", "224.0.0.223", "224.0.0.224", "224.0.0.225",
        "224.0.0.226", "224.0.0.227", "224.0.0.228", "224.0.0.229", "224.0.0.230",
        "224.0.0.231", "224.0.0.232", "224.0.0.233", "224.0.0.234", "224.0.0.235",
        "224.0.0.236", "224.0.0.237", "224.0.0.238", "224.0.0.239", "224.0.0.240",
        "224.0.0.241", "224.0.0.242", "224.0.0.243", "224.0.0.244", "224.0.0.245",
        "224.0.0.246", "224.0.0.247", "224.0.0.248", "224.0.0.249", "224.0.0.250"
    ]
    MDNS = "224.0.0.251"
    LINK_LOCAL_NAME_RESOLUTION = "224.0.0.252"
    TEREDO = "224.0.0.253"
    RFC3692 = "224.0.0.254"
    UNASSIGNED_F = "224.0.0.255"
