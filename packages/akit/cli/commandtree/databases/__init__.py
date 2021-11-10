
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

from akit.cli.commandtree.databases.aqueue import group_databases_aqueue

@click.group("databases")
def group_databases():
    return

group_databases.add_command(group_databases_aqueue)
