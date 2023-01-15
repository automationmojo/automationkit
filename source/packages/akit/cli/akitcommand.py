#!/usr/bin/env python3

import click

from akit.cli.cmdtree.databases import group_akit_databases
from akit.cli.cmdtree.generators import group_akit_generators
from akit.cli.cmdtree.landscape import group_akit_landscape
from akit.cli.cmdtree.network import group_akit_network
from akit.cli.cmdtree.workflow import group_akit_workflow
from akit.cli.cmdtree.servers import group_akit_servers
from akit.cli.cmdtree.testing import group_akit_testing
from akit.cli.cmdtree.utilities import group_akit_utilities

@click.group("akit")
@click.option('-v', '--verbose', count=True)
def akit_root_command(verbose):

    from akit.environment.variables import AKIT_VARIABLES

    if verbose == 0:
        AKIT_VARIABLES.AKIT_INTERACTIVE_CONSOLE = True
    else:
        AKIT_VARIABLES.AKIT_INTERACTIVE_CONSOLE = False

        if verbose == 1:
            AKIT_VARIABLES.AKIT_LOG_LEVEL_CONSOLE = "INFO"
        elif verbose == 2:
            AKIT_VARIABLES.AKIT_LOG_LEVEL_CONSOLE = "DEBUG"
        elif verbose > 2:
            AKIT_VARIABLES.AKIT_LOG_LEVEL_CONSOLE = "NOTSET"

    return

akit_root_command.add_command(group_akit_databases)
akit_root_command.add_command(group_akit_generators)
akit_root_command.add_command(group_akit_landscape)
akit_root_command.add_command(group_akit_network)
akit_root_command.add_command(group_akit_workflow)
akit_root_command.add_command(group_akit_servers)
akit_root_command.add_command(group_akit_testing)
akit_root_command.add_command(group_akit_utilities)

if __name__ == '__main__':
    akit_root_command()