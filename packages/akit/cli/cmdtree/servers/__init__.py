
__author__ = "Myron Walker"
__copyright__ = "Copyright 2022, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click

from akit.cli.cmdtree.servers.results_server import command_akit_servers_results_server

@click.group("servers", help="Contains command for working with tests and test results.")
def group_akit_servers():
    return

group_akit_servers.add_command(command_akit_servers_results_server)
