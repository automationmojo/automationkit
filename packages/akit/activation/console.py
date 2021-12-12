"""
.. module:: console
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is utilized by interactive consoles to activate the environment
               with logging to the console minimized in order to provide a good interactive
               console work experience.

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

import os
import tempfile

from logging.handlers import RotatingFileHandler

from akit.exceptions import AKitSemanticError
from akit.environment.variables import ActivationProfile, AKIT_VARIABLES

# Guard against attemps to activate more than one, activation profile.
if AKIT_VARIABLES.AKIT_ACTIVATION_PROFILE is not None:
    errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
        AKIT_VARIABLES.AKIT_ACTIVATION_PROFILE
    )
    raise AKitSemanticError(errmsg)

AKIT_VARIABLES.AKIT_ACTIVATION_PROFILE = ActivationProfile.Console


temp_output_dir = tempfile.gettempdir()

AKIT_VARIABLES.AKIT_CONSOLE_LOG_LEVEL = "QUIET"
AKIT_VARIABLES.AKIT_JOBTYPE = "console"
AKIT_VARIABLES.AKIT_OUTPUT_DIRECTORY = temp_output_dir

# For console activation we don't want to log to the console and we want
# to point the logs to a different output folder
os.environ["AKIT_CONSOLE_LOG_LEVEL"] = AKIT_VARIABLES.AKIT_CONSOLE_LOG_LEVEL
os.environ["AKIT_JOBTYPE"] = AKIT_VARIABLES.AKIT_JOBTYPE
os.environ["AKIT_OUTPUT_DIRECTORY"] = AKIT_VARIABLES.AKIT_OUTPUT_DIRECTORY

import akit.activation.base # pylint: disable=unused-import,wrong-import-position

from akit.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
logging_initialize()

def showlog():

    print("OUTPUT FOLDER: {}".format(AKIT_VARIABLES.AKIT_OUTPUT_DIRECTORY))
    print("")

    return