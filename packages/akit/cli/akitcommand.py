
import click

from akit.cli.commandtree.databases import group_databases
from akit.cli.commandtree.generators import group_generators
from akit.cli.commandtree.jobs import group_jobs
from akit.cli.commandtree.network import group_network
from akit.cli.commandtree.workflow import group_workflow
from akit.cli.commandtree.testing import group_testing
from akit.cli.commandtree.utilities import group_utilities

@click.group("akit")
def akit_root_command():
    return

akit_root_command.add_command(group_databases)
akit_root_command.add_command(group_generators)
akit_root_command.add_command(group_jobs)
akit_root_command.add_command(group_network)
akit_root_command.add_command(group_workflow)
akit_root_command.add_command(group_testing)
akit_root_command.add_command(group_utilities)

if __name__ == '__main__':
    akit_root_command()