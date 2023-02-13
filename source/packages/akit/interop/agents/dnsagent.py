
from typing import Tuple, Union

import enum
import errno
import socket
import struct
import threading

from akit.exceptions import AKitRuntimeError
from akit.networking.constants import MDNS_GROUP_ADDR, MDNS_PORT
from akit.networking.multicast import create_multicast_socket_for_iface

class DnsAgent:

    def __init__(self, ifname):
        self._ifname = ifname
        self._thread = None
        self._running = False
        return

    def start(self):
        sgate = threading.Event()
        self._thread = threading.Thread(name="DnsAgent - Monitor", target=self._thread_entry_monitor, daemon=True, args=(sgate,))
        return

    def _thread_entry_monitor(self, sgate):

        sock = None
        try:
            sock = create_multicast_socket_for_iface(MDNS_GROUP_ADDR, self._ifname, MDNS_PORT, socket.AF_INET, ttl=1)

            while self._running:
                request, addr = sock.recvfrom(1024)

                response, addr = sock.recvfrom(1024)
                print("PACKET: %s" % addr[0])
                response_lines = response.decode("utf-8").splitlines()
                for rline in response_lines:
                    print("    %s" % rline)
                print()

        finally:
            if sock is not None:
                sock.close()

        return