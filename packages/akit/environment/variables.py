"""
.. module:: variables
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`AKIT_VARIABLES` object which is used store the environment variables.

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

import logging
import os
import sys
import uuid

environ = os.environ

LOG_LEVEL_NAMES = [
    "NOTSET",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "QUIET"
]

LOG_LEVEL_VALUES = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "QUIET": 100
}

def normalize_variable_whitespace(lval):
    lval = lval.strip().replace("/t", " ")
    while lval.find("  ") > -1:
        lval = lval.replace("  ", " ")
    return lval

class JOB_TYPES:
    UNKNOWN = "unknown"
    TESTRUN = "testrun"
    ORCHESTRATION = "orchestration"
    SERVICE = "service"


class AKIT_VARIABLES:
    """
        Container for all the configuration variables that can be passed via environmental variables.
    """

    AKIT_BRANCH = "unknown"
    if "AKIT_BRANCH" in environ:
        AKIT_BRANCH = environ["AKIT_BRANCH"]

    AKIT_BUILD = "unknown"
    if "AKIT_BUILD" in environ:
        AKIT_BUILD = environ["AKIT_BUILD"]

    AKIT_CONSOLE_LOG_LEVEL = None
    if "AKIT_CONSOLE_LOG_LEVEL" in environ:
        AKIT_CONSOLE_LOG_LEVEL = environ["AKIT_CONSOLE_LOG_LEVEL"].upper()

    AKIT_BREAKPOINT = None
    if "AKIT_BREAKPOINT" in environ:
        AKIT_BREAKPOINT = environ["AKIT_BREAKPOINT"].lower()

    AKIT_DEBUGGER = None
    if "AKIT_DEBUGGER" in environ:
        AKIT_DEBUGGER = environ["AKIT_DEBUGGER"].lower()

    AKIT_FILE_LOG_LEVEL = None
    if "AKIT_FILE_LOG_LEVEL" in environ:
        AKIT_FILE_LOG_LEVEL = environ["AKIT_FILE_LOG_LEVEL"].upper()

    AKIT_FLAVOR = "unknown"
    if "AKIT_FLAVOR" in environ:
        AKIT_FLAVOR = environ["AKIT_FLAVOR"]

    AKIT_JOBTYPE = "unknown"
    if "AKIT_JOBTYPE" in environ:
        AKIT_JOBTYPE = environ["AKIT_JOBTYPE"]

    AKIT_LANDSCAPE_MODULE = None
    if "AKIT_LANDSCAPE_MODULE" in environ:
        AKIT_LANDSCAPE_MODULE = environ["AKIT_LANDSCAPE_MODULE"]

    AKIT_RUNID = None
    if "AKIT_RUNID" in environ:
        AKIT_RUNID = environ["AKIT_RUNID"]
    else:
        AKIT_RUNID = str(uuid.uuid4())

    # AKIT_SERVICE_NAME is always set by environment variable
    # as a service starts up.
    AKIT_SERVICE_NAME = None

    AKIT_STARTTIME = None
    if "AKIT_STARTTIME" in environ:
        AKIT_STARTTIME = environ["AKIT_STARTTIME"]

    AKIT_DIRECTORY = os.path.expanduser("~/akit")
    if "AKIT_DIRECTORY" in environ:
        AKIT_DIRECTORY = environ["AKIT_DIRECTORY"]

    AKIT_CONFIG_DIRECTORY = os.path.join(AKIT_DIRECTORY, "config")
    if "AKIT_CONFIG_DIRECTORY" in environ:
        AKIT_CONFIG_DIRECTORY = environ["AKIT_CONFIG_DIRECTORY"]

    AKIT_CREDENTIALS = os.path.join(AKIT_CONFIG_DIRECTORY, "credentials.yaml")
    if "AKIT_CREDENTIALS" in environ:
        AKIT_CREDENTIALS = environ["AKIT_CREDENTIALS"].upper()

    AKIT_RUNTIME_CONFIGURATION = os.path.join(AKIT_CONFIG_DIRECTORY, "runtime.yaml")
    if "AKIT_RUNTIME_CONFIGURATION" in environ:
        AKIT_RUNTIME_CONFIGURATION = environ["AKIT_RUNTIME_CONFIGURATION"]

    AKIT_LANDSCAPE = os.path.join(AKIT_CONFIG_DIRECTORY, "landscape.yaml")
    if "AKIT_LANDSCAPE" in environ:
        AKIT_LANDSCAPE = environ["AKIT_LANDSCAPE"]

    AKIT_OUTPUT_DIRECTORY = None
    if "AKIT_OUTPUT_DIRECTORY" in environ:
        AKIT_OUTPUT_DIRECTORY = environ["AKIT_OUTPUT_DIRECTORY"]

    AKIT_SKIP_DEVICES = None
    if "AKIT_SKIP_DEVICES" in environ:
        AKIT_SKIP_DEVICES = environ["AKIT_SKIP_DEVICES"]

    AKIT_TESTROOT = None
    if "AKIT_TESTROOT" in environ:
        AKIT_TESTROOT = environ["AKIT_TESTROOT"]

    AKIT_TOPOLOGY = os.path.join(AKIT_CONFIG_DIRECTORY, "topology.yaml")
    if "AKIT_TOPOLOGY" in environ:
        AKIT_TOPOLOGY = environ["AKIT_TOPOLOGY"]

    AKIT_UPNP_SCAN_INTEGRATION_BASE = None
    if "AKIT_UPNP_SCAN_INTEGRATION_BASE" in environ:
        AKIT_UPNP_SCAN_INTEGRATION_BASE = environ["AKIT_UPNP_SCAN_INTEGRATION_BASE"]

    AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE = None
    if "AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE" in environ:
        AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE = environ["AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE"]

    AKIT_UPNP_DYN_EXTENSIONS_MODULE = None
    if "AKIT_UPNP_DYN_EXTENSIONS_MODULE" in environ:
        AKIT_UPNP_DYN_EXTENSIONS_MODULE = environ["AKIT_UPNP_DYN_EXTENSIONS_MODULE"]

def extend_path(dir_to_add):
    """
        Extends the PYTHONPATH in the current python process and also modifies
        'PYTHONPATH' so the child processes will also see inherit the extension
        of 'PYTHONPATH'.
    """
    found = False

    for nxt_item in sys.path:
        nxt_item = nxt_item.rstrip(os.sep)
        dir_to_add = dir_to_add.rstrip(os.sep)
        if nxt_item == dir_to_add:
            found = True
            break

    if not found:
        sys.path.insert(0, dir_to_add)
        if "PYTHONPATH" in os.environ:
            os.environ["PYTHONPATH"] = dir_to_add + os.pathsep + os.environ["PYTHONPATH"]
        else:
            os.environ["PYTHONPATH"] = dir_to_add

    return
