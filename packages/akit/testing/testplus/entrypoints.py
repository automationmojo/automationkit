"""
.. module:: entrypoints
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A set of standaridized entry point functions that provide standardized test environment
               startup and test run commencement utilizing the :class:`akit.testing.unittest.testsequencer.TestSequencer`
               object.

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


import argparse
import inspect
import os
import sys

# Force the default configuration to load if it is not already loaded
import akit.environment.activate # pylint: disable=unused-import

from akit.environment.context import Context
from akit.environment.variables import LOG_LEVEL_NAMES

from akit.paths import get_path_for_output
from akit.testing.utilities import find_testmodule_root, find_testmodule_fullname
from akit.testing.testplus.testjob import DefaultTestJob
from akit.xlogging.foundations import logging_initialize, getAutomatonKitLogger

logger = getAutomatonKitLogger()

def generic_test_entrypoint():
    """
        This is the generic test entry point for test modules.  It provides a standardized set of
        commanline parameters that can be used to run test files as scripts.

    .. note::
       The `generic_test_entrypoint` is a useful tool to place at the bottom of test files to allow
       them to easily be run for debugging purposes.
    """
    # We must exit with a result code, initialize it to 0 here
    result_code = 0

    

    sys.exit(result_code)

    return
