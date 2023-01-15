
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

from akit.cli.cmdtree.generators.upnp import group_akit_generators_upnp

@click.group("generators", help="Contains code generators for creating various types of interop code.")
def group_akit_generators():
    return

group_akit_generators.add_command(group_akit_generators_upnp)
