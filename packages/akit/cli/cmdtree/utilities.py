__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


import os

from datetime import datetime

import click

from akit.xtime import FORMAT_DATETIME

HELP_RUNTIME = "The full path of the runtime file to use for the creation of the output folder path."

@click.group("utilities")
def group_akit_utilities():
    return

@click.command("outputfolder")
@click.option("--runtime", "runtime_file", default=None, required=False, help=HELP_RUNTIME)
@click.argument("starttime")
def command_akit_utilities_outputfolder(runtime, starttime):
    
    # IMPORTANT: We need to load the context first because it will trigger the loading
    # of the default user configuration
    from akit.environment.context import Context

    from akit.environment.variables import JOB_TYPES
    from akit.environment.optionoverrides import override_starttime, override_config_runtime

    ctx = Context()
    env = ctx.lookup("/environment")

    # We need to set the job type before we trigger activation.
    env["jobtype"] = JOB_TYPES.COMMAND

    import akit.activation.console

    if runtime is not None:
        override_config_runtime(runtime)

    if starttime is not None:
        override_starttime(starttime)

    from akit.paths import get_path_for_output

    ts_string = get_path_for_output()

    print(ts_string)

    return

@click.command("timestamp")
def command_akit_utilities_timestamp():

    timestamp = datetime.now()
    ts_string = datetime.strftime(timestamp, FORMAT_DATETIME)

    print(ts_string)

    return

group_akit_utilities.add_command(command_akit_utilities_outputfolder)
group_akit_utilities.add_command(command_akit_utilities_timestamp)