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

@click.group("utilities")
def group_utilities():
    return

@click.command("outputfolder")
@click.argument("timestamp")
def command_utilities_outputfolder(timestamp):
    os.environ["AKIT_STARTTIME"] = timestamp

    import akit.environment.console

    from akit.paths import get_path_for_output

    ts_string = get_path_for_output()
    print(ts_string)

    return

@click.command("timestamp")
def command_utilities_timestamp():
    timestamp = datetime.now()
    ts_string = datetime.strftime(timestamp, FORMAT_DATETIME)

    print(ts_string)

    return

group_utilities.add_command(command_utilities_outputfolder)
group_utilities.add_command(command_utilities_timestamp)
