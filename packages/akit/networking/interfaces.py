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

from typing import Tuple, Union

import socket

import netifaces

def encode_address(address: str) -> bytes:
    """
        Encodes the address string to bytes

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

    iface_name_list = [ iface for iface in netifaces.interfaces() ]
    for iface in iface_name_list:
        if_address_table = netifaces.ifaddresses(iface)
        if addr_family in if_address_table:
            faddr_list = if_address_table[addr_family]
            for faddr in faddr_list:
                if 'addr' in faddr:
                    ipaddr = faddr['addr']
                    if ipaddr == corr_ip:
                        corr_iface = iface
                        break
        if corr_iface is not None:
            break

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
