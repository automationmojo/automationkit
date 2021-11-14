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

RUNTIME_DEFAULTS = {
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
    "paths": {
        "landscape": AKIT_VARIABLES.AKIT_LANDSCAPE,
        "results": os.sep.join(("~", "akit", "results")),
        "runtime": os.sep.join(("~", "akit", "config", "runtime.yaml")),
        "consoleresults": os.sep.join(("~", "akit", "console", "%(starttime)s")),
        "runresults": os.sep.join(("~", "akit", "results", "runresults", "%(starttime)s")),
        "testresults": os.sep.join(("~", "akit", "results", "testresults", "%(starttime)s")),
        "topology": AKIT_VARIABLES.AKIT_TOPOLOGY
    }
}

RUNTIME_CONFIGURATION = collections.ChainMap(RUNTIME_DEFAULTS)

def load_runtime_configuration():

    runtime_configuration = {}

    runtime_configuration_file = os.path.expanduser(os.path.expandvars(os.path.abspath(AKIT_VARIABLES.AKIT_RUNTIME_CONFIGURATION)))
    if os.path.exists(runtime_configuration_file):

        with open(runtime_configuration_file, 'r') as rcf:
            rcf_content = rcf.read()
            runtime_configuration = yaml.safe_load(rcf_content)

    return runtime_configuration

