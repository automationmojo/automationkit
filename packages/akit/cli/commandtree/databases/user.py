
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

@click.group("user")
def group_database_user():
    return

HELP_PROFILE = "The name of the configuration profile to use for database connection information."

@click.command("create")
@click.option("--profile", required=True, type=str, help=HELP_PROFILE)
def command_database_user_create(profile):

    engine = engine.lower()

    if engine != "postgresql":
        click.UsageError("UnSupported database engine '{}'".format(engine))

    if port is None:
        if engine == 'postgresql':
            port = 5432

    from akit.datum.dbio import create_user_postgresql_database

    if engine == 'postgresql':
        create_user_postgresql_database(host=host, username=username, password=password)
    else:
        errmsg = "We should never reach this because we pre-check database engine."
        raise RuntimeError(errmsg)

    return

@click.command("reset")
@click.option("--profile", required=True, type=str, help=HELP_PROFILE)
def command_database_user_reset(profile):
    return

group_database_user.add_command(command_database_user_create)
group_database_user.add_command(command_database_user_reset)
