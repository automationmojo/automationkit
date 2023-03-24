
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

@click.group("mdns", help="Group of mDNS utility commands.")
def group_akit_network_scan():
    return

@click.command("scan", help="Performs a mDNS scan on a network for a specific amount of time.")
def command_akit_network_mdns_scan():
    
    import akit.activation.console

    from akit.interop.dns.mdnsservicecatalog import MdnsServiceCatalog

    return


group_akit_network_scan.add_command(command_akit_network_mdns_scan)
