
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

from akit.environment.variables import AKIT_VARIABLES

@click.group("upnp", help="Group of UPNP utility commands.")
def group_akit_network_upnp():
    return

@click.command("query", help="Performs a UPNP msearch query directly against a device.")
@click.argument("ipaddress")
def command_akit_network_upnp_query(ipaddress):

    from akit.interop.upnp.upnpprotocol import msearch_query_host

    show_progress = False
    if AKIT_VARIABLES.AKIT_INTERACTIVE_CONSOLE:
        show_progress = True

    print("")

    found_device_info = msearch_query_host(ipaddress)
    
    print(found_device_info)

    return

@click.command("scan", help="Performs a UPNP msearch scan of the network.")
def command_akit_network_upnp_scan():

    from akit.interop.upnp.upnpprotocol import msearch_scan

    device_hints = []
    found_devices = {}
    matching_devices = {}

    show_progress = False
    if AKIT_VARIABLES.AKIT_INTERACTIVE_CONSOLE:
        show_progress = True

    print("")

    iter_found_devices, iter_matching_devices = msearch_scan(device_hints, show_progress=show_progress)
    found_devices.update(iter_found_devices)
    matching_devices.update(iter_matching_devices)

    print("")

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

group_akit_network_upnp.add_command(command_akit_network_upnp_query)
group_akit_network_upnp.add_command(command_akit_network_upnp_scan)
