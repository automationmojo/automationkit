
from typing import Optional

import socket
import struct

from akit.exceptions import AKitRuntimeError
from akit.networking.constants import IPPROTO_IPV6, SO_RECV_ANYIF

def create_unicast_socket(target_addr: str, port: int, family: socket.AddressFamily = socket.AF_INET,
    ttl: Optional[int] = None, timeout: Optional[float] = None, apple_p2p: bool = False) -> socket.socket:
    """
        Create a socket for listening for sending unicast packets to the specified target ip address.

        :param target_addr: The unicast network address the socket will be used to communicate with.
        :param port: The port to bind the socket with.
        :param family: The internet address family for the socket, either (socket.AF_INET or socket.AF_INET6)
        :param ttl: The time to live that will be attached to the packets sent by this socket.
                    0 = same host
                    1 = same subnet
                    32 = same site
                    64 = same region
                    128 = same continent
                    255 = unrestricted scope
        :param timeout: The socket timeout to assign to the socket
        :param apple_p2p: A boolean value indicating if the socket option for Apple Peer-2-Peer should be set.

    """

    bind_addr = None
    sock = None

    if family == socket.AF_INET:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    elif family == socket.AF_INET6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    else:
        raise AKitRuntimeError("Socket family not supported. family=%r" % family) from None

    if ttl is not None:
        if family == socket.AF_INET:
            ttl = struct.pack(b'b', ttl)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        else:
            sock.setsockopt(IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)

    if apple_p2p:
        sock.setsockopt(socket.SOL_SOCKET, SO_RECV_ANYIF, 1)

    if timeout is not None:
        sock.settimeout(timeout)

    return sock
