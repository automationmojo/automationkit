
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

@click.group("automation")
def group_akit_databases_automation():
    return

HELP_PROFILE = "The name of the configuration profile to use for database connection information."
HELP_SAMPLE_DATA = "Flag indicating if the database should be populated with sample data."

@click.command("create")
@click.option("--profile", show_default="automationdb-admin", default="automationdb-admin", type=str, help=HELP_PROFILE)
@click.option("--sample-data", is_flag=True, show_default=False, default=False, help=HELP_SAMPLE_DATA)
def command_akit_databases_automation_create(profile, sample_data):

    import akit.activation.console

    from akit.datum.dbio import create_automation_database

    create_automation_database(profile)

    return

@click.command("reset")
@click.option("--profile", show_default="automationdb-admin", default="automationdb-admin", type=str, help=HELP_PROFILE)
def command_akit_databases_automation_reset(profile):

    import akit.activation.console

    from akit.datum.dbio import reset_automation_database

    reset_automation_database(profile)

    return

group_akit_databases_automation.add_command(command_akit_databases_automation_create)
group_akit_databases_automation.add_command(command_akit_databases_automation_reset)
