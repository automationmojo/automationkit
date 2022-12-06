
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

from akit.cli.cmdtree.databases.automation import group_akit_databases_automation

@click.group("databases", help="Grouping of database utility commands.")
def group_akit_databases():
    return

group_akit_databases.add_command(group_akit_databases_automation)
