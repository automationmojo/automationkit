"""
.. module:: interfaces
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains helper functions for working with internet interfaces

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

from typing import Dict, List, Tuple, Union

from enum import IntEnum

import os
import re
import socket
import subprocess

import netifaces

class InterfaceClass(IntEnum):
    UNKNOWN = 0
    LOOPBACK = 1
    BRIDGE = 2
    WIRED = 3
    WIRELESS = 4
    TUNNEL = 5

def encode_address(address: str) -> bytes:
    """
        Encodes the address string to bytes.

        :param address: The IP address to encode.

        :returns: A packed string suitable for use with low-level network functions.
    """
    is_ipv6 = ':' in address
    address_family = socket.AF_INET6 if is_ipv6 else socket.AF_INET
    return socket.inet_pton(address_family, address)

def get_ipv4_address(ifname: str) -> Union[str, None]:
    """
        Get the first IPv4 address associated with the specified interface name.

        :param ifname: The interface name to lookup the IP address for.

        :returns: The IPv4 address associated with the specified interface name or None
    """
    addr = None

    address_info = netifaces.ifaddresses(ifname)
    if address_info is not None and netifaces.AF_INET in address_info:
        addr_info = address_info[netifaces.AF_INET][0]
        addr = addr_info["addr"]

    return addr

def get_ipv6_address(ifname: str) -> Union[str, None]:
    """
        Get the first IPv6 address associated with the specified interface name.

        :param ifname: The interface name to lookup the IP address for.

        :returns: The IPv6 address associated with the specified interface name or None
    """
    addr = None

    address_info = netifaces.ifaddresses(ifname)
    if address_info is not None and netifaces.AF_INET6 in address_info:
        addr_info = address_info[netifaces.AF_INET][0]
        addr = addr_info["addr"]

    return addr

def get_correspondance_interface(ref_ip: str, ref_port: int, addr_family=socket.AF_INET) -> Tuple[str, str]:
    """
        Utilizes the TCP stack to make a connection to a remote computer and utilizes
        gets the network interface that was used to connect to the remote computer.
        This network interface is the network interface that is likely to be visible
        to the remote computer and thus could be used to establish services that will
        be visible to the remote computer.

        :param ref_ip: An IP address of a computer that is on the subnet that you wish
                       to find the correspondance ip address for and that is hosting a
                       service that will accept a TCP connection from a client.
        :param ref_port: The port number of a service on a computer that will accept a
                         TCP connection so we can determine a path to the computer.
        :param addr_family: The socket address family to utilize when making a remote
                            connection to a host socket.AF_INET or socket.AF_INET6.
                            The address family used will determine the type of IP address
                            returned from this function.

        :returns: The correspondance interface and IPAddress that can be used to setup a
                  service that is visible to the reference IP address.
    """

    corr_iface = None

    corr_ip = get_correspondance_ip_address(ref_ip, ref_port, addr_family=addr_family)

    corr_iface = get_interface_for_ip(corr_ip)

    return corr_iface, corr_ip

def get_correspondance_ip_address(ref_ip: str, ref_port: int, addr_family=socket.AF_INET) -> str:
    """
        Utilizes the TCP stack to make a connection to a remote computer and utilizes
        gets the socket address of the socket that connected to the remote computer.
        This socket address is the address of the socket that is likely to be visible
        to the remote computer and thus could be used to establish services that will
        be visible to the remote computer.

        :param ref_ip: An IP address of a computer that is on the subnet that you wish
                       to find the correspondance ip address for and that is hosting a
                       service that will accept a TCP connection from a client.
        :param ref_port: The port number of a service on a computer that will accept a
                         TCP connection so we can determine a path to the computer.
        :param addr_family: The socket address family to utilize when making a remote
                            connection to a host socket.AF_INET or socket.AF_INET6.
                            The address family used will determine the type of IP address
                            returned from this function.

        :returns: The correspondance IP address that can be used to setup a service that
                  is visible to the reference IP address.
    """
    corr_ip = None

    sock = socket.socket(addr_family, socket.SOCK_STREAM)
    try:
        sock.settimeout(10)
        sock.connect((ref_ip, ref_port))
        corr_ip, _ = sock.getsockname()
    except Exception: # pylint: disable=broad-except
        # If an exception occurs, just return None
        pass
    finally:
        sock.close()

    return corr_ip

def get_interface_for_ip(if_addr: str) -> str:
    """
        Finds the interface name on the local machine for the internet address provided.

        :param if_addr: The internet address on the local machine to find the interface name for.

        :returns: The ifname that corresponds to the address provided.
    """
    addr_info = socket.getaddrinfo(if_addr, 80)
    addr_family=addr_info[0][0]

    if_name = None

    iface_name_list = [ iface for iface in netifaces.interfaces() ]
    for iface in iface_name_list:
        if_address_table = netifaces.ifaddresses(iface)
        if addr_family in if_address_table:
            faddr_list = if_address_table[addr_family]
            for faddr in faddr_list:
                if 'addr' in faddr:
                    ipaddr = faddr['addr']
                    if ipaddr == if_addr:
                        if_name = iface
                        break
        if if_name is not None:
            break

    return if_name

def get_interface_class_table() -> Dict[str, InterfaceClass]:
    """
        Creates a dictionary lookup table of interface names to :class:`InterfaceClass` enumerations.

        :returns: The table of interface names to interface class values.
    """

    results = {}

    iface_name_list = [ iface for iface in netifaces.interfaces() ]
    for ifname in iface_name_list:
        ifcls = get_interface_class(ifname)
        results[ifname] = ifcls

    return results

def get_interface_class(ifname: str) -> InterfaceClass:
    """
        Returns an :class:`InterfaceClass` value for the interface name specified.

        :param ifname: The name of the interface to determine the interface class for.

        :returns: An :class:`InterfaceClass` that corresponds to the specified interface.
    """

    if_syscls_path = "/sys/class/net/{}".format(ifname)

    if not os.path.exists(if_syscls_path):
        raise FileNotFoundError("No sys class path found for interface={} exp={}".format(ifname, if_syscls_path))
    
    if_files_list = os.listdir(if_syscls_path)
    
    if_class = InterfaceClass.UNKNOWN
    if "wireless" in if_files_list:
        if_class = InterfaceClass.WIRELESS
    elif "bridge" in if_files_list:
        if_class = InterfaceClass.BRIDGE
    else:
        ifinfo = subprocess.check_output("ifconfig {} | grep flags".format(ifname), shell=True).decode('utf8')
        mobj: re.Match = re.match(r"[^<]*.([^>]*)", ifinfo)
        if mobj is not None:
            ifflags = mobj.groups()[0].strip().split(",")
            if "LOOPBACK" in ifflags:
                if_class = InterfaceClass.LOOPBACK
            elif "POINTTOPOINT" in ifflags:
                if_class = InterfaceClass.TUNNEL
            else:
                if_class = InterfaceClass.WIRED
    
    return if_class

def get_interface_names_of_class(ifcls_filter: InterfaceClass) -> List[str]:
    """
        Gets a list of interface names of a give :class:`InterfaceClass`.

        :returns: List of filtered interface names.
    """
    
    iface_list = []

    for ifname, ifcls in get_interface_class_table().items():
        if ifcls == ifcls_filter:
            iface_list.append(ifname)

    return iface_list

def is_ipv6_address(candidate: str) -> bool:
    """
        Checks to see if 'candidate' is an ipv6 address.

        :param candidate: A string that is to be checked to see if it is a valid IPv6 address.

        :returns: A boolean indicating if an IP address is an IPv6 address
    """
    is_ipv6 = False
    if len(candidate) == 16:
        is_ipv6 = True

    return is_ipv6
