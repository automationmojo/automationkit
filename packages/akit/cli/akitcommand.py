
import click

from akit.cli.commandtree.generators import group_generators
from akit.cli.commandtree.jobs import group_jobs
from akit.cli.commandtree.network import group_network
from akit.cli.commandtree.tasking import group_tasking
from akit.cli.commandtree.testing import group_testing

@click.group("akit")
def akit_root_command():
    return

akit_root_command.add_command(group_generators)
akit_root_command.add_command(group_jobs)
akit_root_command.add_command(group_network)
akit_root_command.add_command(group_tasking)
akit_root_command.add_command(group_testing)

if __name__ == '__main__':
    akit_root_command()