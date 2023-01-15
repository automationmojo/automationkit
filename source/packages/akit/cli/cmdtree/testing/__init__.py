
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click

from akit.cli.cmdtree.testing.jobs import group_akit_testing_jobs

from akit.cli.cmdtree.testing.query import command_akit_testing_query
from akit.cli.cmdtree.testing.run import command_akit_testing_run

@click.group("testing", help="Contains command for working with tests and test results.")
def group_akit_testing():
    return

group_akit_testing.add_command(group_akit_testing_jobs)

group_akit_testing.add_command(command_akit_testing_query)
group_akit_testing.add_command(command_akit_testing_run)
