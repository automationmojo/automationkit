
import click

from akit.cli.level1.generators import group_generators
from akit.cli.level1.jobs import group_jobs
from akit.cli.level1.tasking import group_tasking
from akit.cli.level1.tests import group_tests

@click.group("akit")
def akit_root_command():
    return

akit_root_command.add_command(group_generators)
akit_root_command.add_command(group_jobs)
akit_root_command.add_command(group_tasking)
akit_root_command.add_command(group_tests)

if __name__ == '__main__':
    akit_root_command()