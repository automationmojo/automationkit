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

from datetime import datetime
from enum import Enum

from akit.conversions import string_to_bool
from akit.xtime import parse_datetime

environ = os.environ

THIS_DIR = os.path.dirname(__file__)

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
    COMMAND = "command"
    CONSOLE = "console"
    TESTRUN = "testrun"
    ORCHESTRATION = "orchestration"
    SERVICE = "service"


class ActivationProfile(str, Enum):
    Command = "command"
    Console = "console"
    Orchestration = "orchestration"
    Service = "service"
    TestRun = "testrun"


class AKIT_VARIABLES:
    """
        Container for all the configuration variables that can be passed via environmental variables.
    """

    AKIT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))

    AKIT_ACTIVATION_PROFILE = None

    AKIT_INTERACTIVE_CONSOLE = False
    if "AKIT_INTERACTIVE_CONSOLE" in environ:
        AKIT_INTERACTIVE_CONSOLE = string_to_bool(environ["AKIT_INTERACTIVE_CONSOLE"].lower())

    AKIT_APOD_NAME = "unknown"
    if "AKIT_APOD_NAME" in environ:
        AKIT_APOD_NAME = environ["AKIT_APOD_NAME"]

    AKIT_BUILD_BRANCH = "unknown"
    if "AKIT_BUILD_BRANCH" in environ:
        AKIT_BUILD_BRANCH = environ["AKIT_BUILD_BRANCH"]

    AKIT_BUILD_NAME = "unknown"
    if "AKIT_BUILD_NAME" in environ:
        AKIT_BUILD_NAME = environ["AKIT_BUILD_NAME"]

    AKIT_BUILD_OWNER = None
    if "AKIT_BUILD_OWNER" in environ:
        AKIT_BUILD_OWNER = environ["AKIT_BUILD_OWNER"]
        
    AKIT_BUILD_OWNER_ID = None
    AKIT_BUILD_OWNER_DISPLAY = None
    if AKIT_BUILD_OWNER is not None:
        if AKIT_BUILD_OWNER.find(";") > -1:
            AKIT_BUILD_OWNER_ID, AKIT_BUILD_OWNER_DISPLAY = AKIT_BUILD_OWNER.split(";")
        else:
            AKIT_BUILD_OWNER_ID = AKIT_BUILD_OWNER

    AKIT_LOG_LEVEL_CONSOLE = None
    if "AKIT_LOG_LEVEL_CONSOLE" in environ:
        AKIT_LOG_LEVEL_CONSOLE = environ["AKIT_LOG_LEVEL_CONSOLE"].upper()

    AKIT_BREAKPOINTS = None
    if "AKIT_BREAKPOINTS" in environ:
        breakpoints = []
        for bkpnt in environ["AKIT_BREAKPOINTS"].lower().split(","):
            breakpoints.append(bkpnt)
        AKIT_BREAKPOINTS = breakpoints

    AKIT_DEBUGGER = None
    if "AKIT_DEBUGGER" in environ:
        AKIT_DEBUGGER = environ["AKIT_DEBUGGER"].lower()

    AKIT_LOG_LEVEL_FILE = None
    if "AKIT_LOG_LEVEL_FILE" in environ:
        AKIT_LOG_LEVEL_FILE = environ["AKIT_LOG_LEVEL_FILE"].upper()

    AKIT_BUILD_FLAVOR = "unknown"
    if "AKIT_BUILD_FLAVOR" in environ:
        AKIT_BUILD_FLAVOR = environ["AKIT_BUILD_FLAVOR"]

    AKIT_JOBTYPE = "unknown"
    if "AKIT_JOBTYPE" in environ:
        AKIT_JOBTYPE = environ["AKIT_JOBTYPE"]

    AKIT_CONFIG_EXTENSION_POINTS_MODULE = "akit.extensionpoints"
    if "AKIT_CONFIG_EXTENSION_POINTS_MODULE" in environ:
        AKIT_CONFIG_EXTENSION_POINTS_MODULE = environ["AKIT_CONFIG_EXTENSION_POINTS_MODULE"]

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
        starttime = parse_datetime(environ["AKIT_STARTTIME"])
        AKIT_STARTTIME = starttime
    elif AKIT_STARTTIME is None:
        AKIT_STARTTIME = datetime.now()

    AKIT_HOME_DIRECTORY = os.path.expanduser("~/akit")
    if "AKIT_HOME_DIRECTORY" in environ:
        AKIT_HOME_DIRECTORY = environ["AKIT_HOME_DIRECTORY"]

    AKIT_CONFIG_DIRECTORY = os.path.join(AKIT_HOME_DIRECTORY, "config")
    if "AKIT_CONFIG_DIRECTORY" in environ:
        AKIT_CONFIG_DIRECTORY = environ["AKIT_CONFIG_DIRECTORY"]

    AKIT_CONFIG_CREDENTIALS = os.path.join(AKIT_CONFIG_DIRECTORY, "credentials.yaml")
    if "AKIT_CONFIG_CREDENTIALS" in environ:
        AKIT_CONFIG_CREDENTIALS = environ["AKIT_CONFIG_CREDENTIALS"].upper()

    AKIT_CONFIG_LANDSCAPE_NAME = "default-landscape"
    if "AKIT_CONFIG_LANDSCAPE_NAME" in environ:
        AKIT_CONFIG_LANDSCAPE_NAME = environ["AKIT_CONFIG_LANDSCAPE_NAME"]

    AKIT_CONFIG_LANDSCAPE = os.path.join(AKIT_CONFIG_DIRECTORY, "landscapes", AKIT_CONFIG_LANDSCAPE_NAME + ".yaml")
    if "AKIT_CONFIG_LANDSCAPE" in environ:
        AKIT_CONFIG_LANDSCAPE = environ["AKIT_CONFIG_LANDSCAPE"]

    AKIT_CONFIG_RUNTIME_NAME = "default-runtime"
    if "AKIT_CONFIG_RUNTIME_NAME" in environ:
        AKIT_CONFIG_RUNTIME_NAME = environ["AKIT_CONFIG_RUNTIME_NAME"]

    AKIT_CONFIG_RUNTIME_SEARCH_PATH = None
    if "AKIT_CONFIG_RUNTIME_SEARCH_PATH" in environ:
        AKIT_CONFIG_RUNTIME_SEARCH_PATH = environ["AKIT_CONFIG_RUNTIME_SEARCH_PATH"]
    else:
        AKIT_CONFIG_RUNTIME_SEARCH_PATH = os.path.join(AKIT_CONFIG_DIRECTORY, "runtimes")

    AKIT_CONFIG_RUNTIME = None
    if "AKIT_CONFIG_RUNTIME" in environ:
        AKIT_CONFIG_RUNTIME = environ["AKIT_CONFIG_RUNTIME"]
    else:
        runtime_search_path_list = AKIT_CONFIG_RUNTIME_SEARCH_PATH.split(":")
        for spath in runtime_search_path_list:
            check_path = os.path.join(spath, AKIT_CONFIG_RUNTIME_NAME + ".yaml")
            if os.path.exists(check_path):
                AKIT_CONFIG_RUNTIME = check_path
                break
    
    # If we still did not find a runtime file, set it to the default location
    # the configuration loading code can warn if the file does not exist.
    if AKIT_CONFIG_RUNTIME is None:
        AKIT_CONFIG_RUNTIME = os.path.join(AKIT_CONFIG_DIRECTORY, "runtimes", AKIT_CONFIG_RUNTIME_NAME + ".yaml")

    AKIT_CONFIG_TOPOLOGY_NAME = "default-topology"
    if "AKIT_CONFIG_TOPOLOGY_NAME" in environ:
        AKIT_CONFIG_TOPOLOGY_NAME = environ["AKIT_CONFIG_TOPOLOGY_NAME"]

    AKIT_CONFIG_TOPOLOGY = os.path.join(AKIT_CONFIG_DIRECTORY, "topologies", AKIT_CONFIG_TOPOLOGY_NAME + ".yaml")
    if "AKIT_CONFIG_TOPOLOGY" in environ:
        AKIT_CONFIG_TOPOLOGY = environ["AKIT_CONFIG_TOPOLOGY"]

    AKIT_CONFIG_USER = os.path.join(AKIT_CONFIG_DIRECTORY, "user.yaml")
    if "AKIT_CONFIG_USER" in environ:
        AKIT_CONFIG_USER = environ["AKIT_CONFIG_USER"]

    AKIT_OUTPUT_DIRECTORY = None
    if "AKIT_OUTPUT_DIRECTORY" in environ:
        AKIT_OUTPUT_DIRECTORY = environ["AKIT_OUTPUT_DIRECTORY"]

    AKIT_SKIP_DEVICES = None
    if "AKIT_SKIP_DEVICES" in environ:
        AKIT_SKIP_DEVICES = environ["AKIT_SKIP_DEVICES"]

    AKIT_RESULTS_STATIC_RESOURCE_DEST_DIR = os.path.join(AKIT_HOME_DIRECTORY, "results", "static")
    if "AKIT_RESULTS_STATIC_RESOURCE_DEST_DIR" in environ:
        AKIT_RESULTS_STATIC_RESOURCE_DEST_DIR = environ["AKIT_RESULTS_STATIC_RESOURCE_DEST_DIR"]
    
    AKIT_RESULTS_STATIC_RESOURCE_SRC_DIR = os.path.join(AKIT_DIR, "templates", "static")
    if "AKIT_RESULTS_STATIC_RESOURCE_SRC_DIR" in environ:
        AKIT_RESULTS_STATIC_RESOURCE_SRC_DIR = environ["AKIT_RESULTS_STATIC_RESOURCE_SRC_DIR"]

    AKIT_RESULTS_HTML_TEMPLATE = None
    if "AKIT_RESULTS_HTML_TEMPLATE" in environ:
        AKIT_RESULTS_HTML_TEMPLATE = environ["AKIT_RESULTS_HTML_TEMPLATE"]

    AKIT_TESTROOT = None
    if "AKIT_TESTROOT" in environ:
        AKIT_TESTROOT = environ["AKIT_TESTROOT"]

    AKIT_TRACEBACK_POLICY_OVERRIDE = None
    if "AKIT_TRACEBACK_POLICY_OVERRIDE" in environ:
        AKIT_TRACEBACK_POLICY_OVERRIDE = environ["AKIT_TRACEBACK_POLICY_OVERRIDE"]

    AKIT_UPNP_SCAN_INTEGRATION_BASE = None
    if "AKIT_UPNP_SCAN_INTEGRATION_BASE" in environ:
        AKIT_UPNP_SCAN_INTEGRATION_BASE = environ["AKIT_UPNP_SCAN_INTEGRATION_BASE"]

    AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE = None
    if "AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE" in environ:
        AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE = environ["AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE"]

    AKIT_UPNP_DYN_EXTENSIONS_MODULE = None
    if "AKIT_UPNP_DYN_EXTENSIONS_MODULE" in environ:
        AKIT_UPNP_DYN_EXTENSIONS_MODULE = environ["AKIT_UPNP_DYN_EXTENSIONS_MODULE"]
    
    AKIT_TIMETRAVEL = False
    if "AKIT_TIMETRAVEL" in environ:
        AKIT_TIMETRAVEL = environ["AKIT_TIMETRAVEL"].lower()

    AKIT_TIMEPORTALS = None
    if "AKIT_TIMEPORTALS" in environ:
        AKIT_TIMEPORTALS = string_to_bool(environ["AKIT_TIMEPORTALS"].lower())

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
