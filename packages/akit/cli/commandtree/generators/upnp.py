
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


import click

from akit.environment.variables import LOG_LEVEL_NAMES

@click.group("upnp")
def group_generators_upnp():
    return

@click.command("generate")
def command_generators_upnp_generate():
    return

@click.command("scan")
def command_generators_upnp_scan():
    return

group_generators_upnp.add_command(command_generators_upnp_generate)
group_generators_upnp.add_command(command_generators_upnp_scan)
