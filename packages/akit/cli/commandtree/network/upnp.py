
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import os

import click

from akit.environment.variables import LOG_LEVEL_NAMES

@click.group("upnp")
def group_network_upnp():
    return

@click.command("scan")
def command_network_upnp_scan():

    from akit.integration.upnp.upnpprotocol import msearch_scan

    device_hints = []
    found_devices = {}
    matching_devices = {}

    iter_found_devices, iter_matching_devices = msearch_scan(device_hints)
    found_devices.update(iter_found_devices)
    matching_devices.update(iter_matching_devices)

    for fdusn, fdinfo in found_devices.items():
        dev_lines = [
            "DEVICE - {}".format(fdusn)
        ]
        for fdi_key, fdi_val in fdinfo.items():
            dev_lines.append("    {}: {}".format(fdi_key, fdi_val))
        dev_lines.append("")
        dev_info_out = os.linesep.join(dev_lines)
        print(dev_info_out)

    return

group_network_upnp.add_command(command_network_upnp_scan)
