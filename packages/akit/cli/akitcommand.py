#!/usr/bin/env python

import click

from akit.cli.cmdtree.databases import group_akit_databases
from akit.cli.cmdtree.generators import group_akit_generators
from akit.cli.cmdtree.jobs import group_akit_jobs
from akit.cli.cmdtree.landscape import group_akit_landscape
from akit.cli.cmdtree.network import group_akit_network
from akit.cli.cmdtree.workflow import group_akit_workflow
from akit.cli.cmdtree.testing import group_akit_testing
from akit.cli.cmdtree.utilities import group_akit_utilities

@click.group("akit")
def akit_root_command():
    return

akit_root_command.add_command(group_akit_databases)
akit_root_command.add_command(group_akit_generators)
akit_root_command.add_command(group_akit_jobs)
akit_root_command.add_command(group_akit_landscape)
akit_root_command.add_command(group_akit_network)
akit_root_command.add_command(group_akit_workflow)
akit_root_command.add_command(group_akit_testing)
akit_root_command.add_command(group_akit_utilities)

if __name__ == '__main__':
    akit_root_command()