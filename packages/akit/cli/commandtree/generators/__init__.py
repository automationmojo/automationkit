
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

from akit.cli.commandtree.generators.upnp import group_generators_upnp

@click.group("generators")
def group_generators():
    return

group_generators.add_command(group_generators_upnp)