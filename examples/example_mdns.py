
import socket

from akit.integration.dns.dnsconst import DnsRecordClass, DnsRecordType
from akit.integration.dns.dnsquestion import DnsQuestion

from akit.networking.multicast import MDNS_GROUP_ADDR, MDNS_PORT, create_multicast_socket_for_iface

ifname = "wlo1"

def main_mdns():

    sock = create_multicast_socket_for_iface(MDNS_GROUP_ADDR, ifname, MDNS_PORT, socket.AF_INET, ttl=1)

    question = DnsQuestion("*", DnsRecordType.SRV, DnsRecordType.ANY)
    msearch_msg = question.as_query_bytes()

    sock.sendto(msearch_msg, (MDNS_GROUP_ADDR, MDNS_PORT))

    while True:
        response, addr = sock.recvfrom(1024)
        print("PACKET: %s" % addr[0])
        response_lines = response.decode("utf-8").splitlines()
        for rline in response_lines:
            print("    %s" % rline)
        print()

if __name__ == "__main__":
     main_mdns()