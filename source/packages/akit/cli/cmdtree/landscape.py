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

HELP_CREDENTIALS = "The full path of the credentials file to use for the testrun."
HELP_LANDSCAPE = "The full path of the landscape file to verify."
HELP_RUNTIME = "The full path of the runtime file to use for the testrun."

@click.group("landscape", help="Contains commands that are used to perform operations on the test landscape.")
def group_akit_landscape():
    return

@click.command("verify")
@click.option("--credentials", "credentials_file", default=None, required=False, help=HELP_CREDENTIALS)
@click.option("--landscape", "landscape_file", default=None, required=False, help=HELP_LANDSCAPE)
@click.option("--runtime", "runtime_file", default=None, required=False, help=HELP_RUNTIME)
def command_akit_landscape_verify(credentials_file, landscape_file, runtime_file):
    
    # pylint: disable=unused-import,import-outside-toplevel

    # We do the imports of the automation framework code inside the action functions because
    # we don't want to startup loggin and the processing of inputs and environment variables
    # until we have entered an action method.  Thats way we know how to setup the environment.

    # IMPORTANT: We need to load the context first because it will trigger the loading
    # of the default user configuration
    from akit.environment.context import Context
    from akit.environment.contextpaths import ContextPaths

    from akit.environment.variables import JOB_TYPES, AKIT_VARIABLES
    
    from akit.environment.optionoverrides import (
        override_config_credentials,
        override_config_landscape,
        override_config_runtime
    )

    ctx = Context()
    env = ctx.lookup("/environment")

    # We need to set the job type before we trigger activation.
    env["jobtype"] = JOB_TYPES.COMMAND

    # Activate the AutomationKit environment with characteristics of a console application
    import akit.activation.console

    from akit.xlogging.foundations import logging_initialize, getAutomatonKitLogger

    # Initialize logging
    logging_initialize()
    logger = getAutomatonKitLogger()

    if credentials_file is not None:
        override_config_credentials(credentials_file)

    if landscape_file is not None:
        override_config_landscape(landscape_file)

    if runtime_file is not None:
        override_config_runtime(runtime_file)

    from akit.interop.landscaping.landscape import Landscape, startup_landscape
    from akit.interop.landscaping.landscapedevice import LandscapeDevice

    lscape: Landscape = startup_landscape(include_ssh=True, include_upnp=True)

    upnp_device_configs = lscape.get_upnp_device_configs()
    if len(upnp_device_configs):
        print("======================= UPNP DEVICES =======================")

        for dev in upnp_device_configs:
            skip_dev = True if "skip" in dev and dev["skip"] else False

            upnp_info = dev["upnp"]
            usn = upnp_info["USN"]
            modelName = upnp_info["modelName"]
            modelNumber = upnp_info["modelNumber"]

            status = "Down"
            lscape_dev: LandscapeDevice = lscape.lookup_device_by_identity(usn)
            if lscape_dev is not None:
                status = lscape_dev.verify_status()

            dev_info_lines = [
                "    Model: {} - {}".format(modelName, modelNumber),
                "      USN: {}".format(usn),
                "     Skip: {}".format(skip_dev),
                "   Status: {}".format(status)
            ]
            dev_info = os.linesep.join(dev_info_lines)

            print(dev_info)
            print("")

    ssh_devices_configs = lscape.get_ssh_device_configs(exclude_upnp=True)
    if len(ssh_devices_configs):
        print("======================= SSH DEVICES =======================")

        for dev in ssh_devices_configs:
            skip_dev = True if "skip" in dev and dev["skip"] else False

            host = dev["host"]

            status = "Down"
            lscape_dev: LandscapeDevice = lscape.lookup_device_by_identity(host)
            if lscape_dev is not None:
                status = lscape_dev.verify_status()

            dev_info_lines = [
                "    HOST: {}".format(host),
                "   Status: {}".format(status)
            ]
            dev_info = os.linesep.join(dev_info_lines)

            print(dev_info)
            print("")

    return

group_akit_landscape.add_command(command_akit_landscape_verify)
