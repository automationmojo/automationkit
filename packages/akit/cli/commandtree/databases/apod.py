
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import argparse
import os
import sys

import click

from akit.environment.variables import LOG_LEVEL_NAMES

@click.group("apod")
def group_databases_apod():
    return

HELP_PROFILE = "The name of the configuration profile to use for database connection information."

@click.command("create")
@click.option("--profile", required=True, type=str, help=HELP_PROFILE)
def command_databases_apod_create(profile):

    import akit.environment.console

    from akit.datum.dbio import create_apod_database

    create_apod_database(profile)

    return

@click.command("reset")
@click.option("--profile", required=True, type=str, help=HELP_PROFILE)
def command_databases_apod_reset(profile):
    return

group_databases_apod.add_command(command_databases_apod_create)
group_databases_apod.add_command(command_databases_apod_reset)
