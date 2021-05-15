
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

@click.group("generators")
def group_generators():
    return

def command_generators_generate():
    return

def command_generators_scan():
    return

group_generators.add_command(command_generators_scan)
group_generators.add_command(command_generators_generate)
