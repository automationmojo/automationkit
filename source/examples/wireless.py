
from akit.networking.interfaces import get_interface_names_of_class, InterfaceClass

import nmcli

wireless_iface = get_interface_names_of_class(InterfaceClass.WIRELESS)[0]

networks = nmcli.device.wifi(wireless_iface)

sonos_ap = None
for devwifi in networks:
    if devwifi.ssid.find("SONOS-") == 0:
        sonos_ap = devwifi 

