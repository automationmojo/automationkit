"""
.. module:: configuration
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the default runtime configration dictionary and the functions that
               are used to load the automation configuration file and overlay the settings on top of the
               default runtime configuration.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import collections
import os
import yaml

from akit.environment.variables import AKIT_VARIABLES

# The override configuration dictionary is added to the ChainMap first so it takes
# precidence over all other dictionaries in the chain.
OVERRIDE_CONFIGURATION = {}

CONFIGURATION_MAP = collections.ChainMap(OVERRIDE_CONFIGURATION)

def load_user_configuration():

    # We create the default configuration here because there are a couple of environment
    # variables that might modify our default configuration values, we want to delay
    # locking the values from the variables into a default configuration declaration until
    # this function is called.
    default_user_configuration = { 
        "version": "1.0.0",
        "logging": {
            "levels": {
                "console": "INFO",
                "logfile": "DEBUG"
            },
            "logname": "%(jobtype)s.log",
            "branched": [
                {
                    "name": "paramiko.transport",
                    "logname": "paramiko.transport.log",
                    "loglevel": "DEBUG"
                }
            ]
        },
        "debugging": {
            "timemachine": {
                "active-portals": {
                }
            }
        }
    }

    user_configuration = {}

    user_configuration_file = os.path.expanduser(os.path.expandvars(os.path.abspath(AKIT_VARIABLES.AKIT_CONFIG_USER)))
    if os.path.exists(user_configuration_file):

        with open(user_configuration_file, 'r') as ucf:
            ucf_content = ucf.read()
            user_configuration = yaml.safe_load(ucf_content)
    else:

        with open(user_configuration_file, 'w+') as ucf:
            user_configuration = default_user_configuration
            ucf_content = yaml.dump(user_configuration, default_flow_style=False)
            ucf.write(ucf_content)

    return user_configuration

def load_runtime_configuration():

    runtime_configuration = {}

    runtime_configuration_file = os.path.expanduser(os.path.expandvars(os.path.abspath(AKIT_VARIABLES.AKIT_CONFIG_RUNTIME)))
    if os.path.exists(runtime_configuration_file):

        with open(runtime_configuration_file, 'r') as rcf:
            rcf_content = rcf.read()
            runtime_configuration = yaml.safe_load(rcf_content)

    return runtime_configuration

