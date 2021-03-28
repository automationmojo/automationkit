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

from akit.environment.variables import LOG_LEVEL_NAMES

import click

import yaml

HELP_WORK = "The file containing the workpacket detail for performing a tasking orchestration."
HELP_OUTPUT = "The output directory where results and artifacts are collected."
HELP_START = r"A time stamp to associate with the start of the run. Example: 2020-10-17T15:30:11.989120  Bash: date +%Y-%m-%dT%H:%M:%S.%N"
HELP_CONSOLE_LOG_LEVEL = "The logging level for console output."
HELP_FILE_LOG_LEVEL = "The logging level for logfile output."

@click.group("tasking")
def group_tasking():
    return

@click.command("run")
@click.option("--work", "-w", required=True, help=HELP_WORK)
@click.option("--output", "-o", required=False, help=HELP_OUTPUT)
@click.option("--start", default=None, required=False, help=HELP_START)
@click.option("--console-level", default=None, required=False, type=click.Choice(LOG_LEVEL_NAMES, case_sensitive=False), help=HELP_CONSOLE_LOG_LEVEL)
@click.option("--logfile-level", default=None, required=False, type=click.Choice(LOG_LEVEL_NAMES, case_sensitive=False), help=HELP_FILE_LOG_LEVEL)
def command_tasking_run(work, includes, excludes, output, start, branch, build, flavor, console_level, logfile_level):

    # pylint: disable=unused-import,import-outside-toplevel

    # We do the imports of the automation framework code inside the action functions because
    # we don't want to startup loggin and the processing of inputs and environment variables
    # until we have entered an action method.  Thats way we know how to setup the environment.

    # IMPORTANT: We need to load the context first because it will trigger the loading
    # of the default user configuration
    from akit.environment.context import Context
    from akit.environment.variables import extend_path

    ctx = Context()
    env = ctx.lookup("/environment")

    workpacket_file = os.path.abspath(os.path.expanduser(os.path.expandvars(work)))
    if not os.path.exists(workpacket_file):
        error_msg = "The specified work packet file does not exist. file=%s" % workpacket_file
        raise click.BadParameter(error_msg)

    workpacket_info = None
    with open(workpacket_file, 'r') as wpf:
        wpfcontent = wpf.read()
        workpacket_info = yaml.safe_load(wpfcontent)

    if workpacket_info is not None:

        from akit.tasking.entrypoints import run_workpacket_entrypoint

        # Run the work packet
        run_workpacket_entrypoint(workpacket_info)

    else:
        error_msg = "Failure loading the work packet info from. file=%s" % workpacket_file
        raise click.BadParameter(error_msg)

    return