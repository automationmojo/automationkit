
from typing import List

import csv
import netifaces
import os

ARPING_RANGE_CMD = """/bin/bash -c 'for i in {1..254} ;do ping %s.$i -c 1 -w 5  >/dev/null && echo "%s.$i" & done; wait < <(jobs -p); echo Done' """

def get_arp_table(normalize_hwaddr: bool=False):
    arp_table = {}

    with open('/proc/net/arp') as aif:
        #'IP address', 'HW type', 'Flags', 'HW address', 'Mask', 'Device'
        reader = csv.reader(aif, skipinitialspace=True, delimiter=' ')
        table_data_rows = [r for r in reader][1:]
        for ip, hwtype, flags, hwaddr, mask, ifname in table_data_rows:
            if normalize_hwaddr:
                hwaddr = hwaddr.replace(":", "").upper()
            iinfo = { hwaddr: {"hwaddr": hwaddr, "ip": ip, "ifname": ifname, "hwtype": hwtype, "flags": flags, "mask": mask }}
            arp_table.update(iinfo)

    return arp_table

def refresh_arp_table(exclude_interfaces: List=["lo"]):
    """
        ping -c 5 -b 10.x.x.255
    """
    interface_list = netifaces.interfaces()
    for ifname in interface_list:
        if ifname not in exclude_interfaces:
            address_info = netifaces.ifaddresses(ifname)
            if address_info is not None:

                # First look for IPv4 address information
                if netifaces.AF_INET in address_info:
                    addr_info = address_info[netifaces.AF_INET][0]
                    ifaddress = addr_info["addr"]
                    ifaddr_parts = ifaddress.split(".")
                    addr_prefix = ".".join(ifaddr_parts[:-1])
                    ping_cmd = PING_RANGE_CMD % (addr_prefix, addr_prefix)
                    os.system(ping_cmd)

    return

if __name__ == "__main__":
    refresh_arp_table()