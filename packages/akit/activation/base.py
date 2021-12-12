"""
.. module:: activate
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is utilized by test files to ensure the test environment is initialized in
               the correct order.

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

import inspect
import os
import sys

from datetime import datetime
from akit.exceptions import AKitSemanticError

from akit.xtime import parse_datetime

# Perform a sematic check to see who is importing the akit.activation.base module.  We
# need to make sure that the user is following the proper semantics and importing an activation
# profile and not directly importing this module.  This will enforce the setting of the
# activation profile in the global variables and enforce a proper environment activation
# sequence is followed.
importer_frame = sys._getframe()
while True:
    importer_frame = importer_frame.f_back
    if importer_frame.f_code.co_filename.find("importlib") < 0:
        break
if "__activation_profile__" not in importer_frame.f_locals:
    errmsg = "The 'akit.activation.base' should not be directly imported." \
             "  The environment activation should always happen by importing" \
             " an activation profile module."
    raise AKitSemanticError(errmsg)

# =======================================================================================
# The way we start up the test framework and the order which things come up in is a very
# important part of the automation process.  It effects whether or not logging is brought
# up consistently before all modules start using it.  It ensures that no matter how we
# enter into an automation process, whether via a test runner, terminal, or debugging a single
# file that we properly parse arguments and settings and launch the automation process
# consistently.
#
# Because of these necessities, we setup the activate module so it is the first thing
# scripts and tests files that consume the test framework will import to ensure the
# startup process is always consistent
#
# The framework has a special activation module :module:`akit.environment.console` that is
# used when bringing up the test framework in a console.  This special method redirects

# Step 1 - Force the default configuration to load if it is not already loaded
from akit.environment.configuration import RUNTIME_CONFIGURATION

# Step 2 - Process the environment variables that are used to overwride the
# default configuration
from akit.environment.variables import AKIT_VARIABLES, LOG_LEVEL_NAMES, normalize_variable_whitespace

# Step 3 - Load the user configuration and add it to the RUNTIME_CONFIGURATION 'ChainMap' so
# the user settings take precedence over the runtime default settings.
from akit.environment.configuration import load_runtime_configuration

THIS_DIR = os.path.dirname(__file__)

AKIT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))

DEFAULT_PATH_EXPANSIONS = [
    os.path.expanduser,
    os.path.expandvars,
    os.path.abspath
]
def expand_path(path_in, expansions=DEFAULT_PATH_EXPANSIONS):

    path_out = path_in
    for expansion_func in expansions:
        path_out = expansion_func(path_out)

    return path_out

runtime_config = load_runtime_configuration()
RUNTIME_CONFIGURATION.update(runtime_config)

if AKIT_VARIABLES.AKIT_CONSOLE_LOG_LEVEL is not None and AKIT_VARIABLES.AKIT_CONSOLE_LOG_LEVEL in LOG_LEVEL_NAMES:
    console_level = AKIT_VARIABLES.AKIT_CONSOLE_LOG_LEVEL
else:
    console_level = "INFO"

if AKIT_VARIABLES.AKIT_FILE_LOG_LEVEL is not None and AKIT_VARIABLES.AKIT_FILE_LOG_LEVEL in LOG_LEVEL_NAMES:
    logfile_level = AKIT_VARIABLES.AKIT_FILE_LOG_LEVEL
else:
    logfile_level = "DEBUG"

# Step 5 - Force the context to load with defaults ifz it is not already loaded
# and setup the run type if not already set
from akit.environment.context import Context # pylint: disable=wrong-import-position

ctx = Context()

# The environment element holds the resulting variables that are a result of the
# startup process
env = ctx.lookup("/environment")

env["branch"] = AKIT_VARIABLES.AKIT_BRANCH
env["build"] = AKIT_VARIABLES.AKIT_BUILD
env["flavor"] = AKIT_VARIABLES.AKIT_FLAVOR
env["breakpoint"] = AKIT_VARIABLES.AKIT_BREAKPOINT
env["debugger"] = AKIT_VARIABLES.AKIT_DEBUGGER
env["testroot"] = AKIT_VARIABLES.AKIT_TESTROOT

if AKIT_VARIABLES.AKIT_STARTTIME is not None:
    starttime = parse_datetime(AKIT_VARIABLES.AKIT_STARTTIME)
    env["starttime"] = starttime
else:
    env["starttime"] = datetime.now()
env["runid"] = AKIT_VARIABLES.AKIT_RUNID


conf = ctx.lookup("/environment/configuration")

conf["credentials"] = AKIT_VARIABLES.AKIT_CREDENTIALS

conf["skip-devices-override"] = []
if AKIT_VARIABLES.AKIT_SKIP_DEVICES is not None:
    devices_list = normalize_variable_whitespace(AKIT_VARIABLES.AKIT_SKIP_DEVICES).split(" ")
    conf["skip-devices-override"] = devices_list

fill_dict = {
    "starttime": str(env["starttime"]).replace(" ", "T")
}

jobtype = env["jobtype"]
if AKIT_VARIABLES.AKIT_OUTPUT_DIRECTORY is not None:
    outdir_full = expand_path(AKIT_VARIABLES.AKIT_OUTPUT_DIRECTORY % fill_dict)
    env["output_directory"] = outdir_full
else:
    if jobtype == "console":
        outdir_template = conf.lookup("/paths/consoleresults")
        outdir_full = expand_path(outdir_template % fill_dict)
        env["output_directory"] = outdir_full
    else:
        env["jobtype"] = "testrun"
        outdir_template = conf.lookup("/paths/testresults")
        outdir_full = expand_path(outdir_template % fill_dict)
        env["output_directory"] = outdir_full

results_configuration = {}
results_configuration["static-resource-dest-dir"] = expand_path(AKIT_VARIABLES.AKIT_RESULTS_STATIC_RESOURCE_DEST_DIR)
results_configuration["static-resource-src-dir"] = expand_path(AKIT_VARIABLES.AKIT_RESULTS_STATIC_RESOURCE_SRC_DIR)

if AKIT_VARIABLES.AKIT_RESULTS_HTML_TEMPLATE is not None:
    results_configuration["html-template"] = AKIT_VARIABLES.AKIT_RESULTS_HTML_TEMPLATE
else:
    results_configuration["html-template"] = expand_path(os.path.join(AKIT_DIR, "templates", "testsummary.html"))

conf["results-configuration"] = results_configuration

if jobtype != "console":
    env["behaviors"] = {
        "log-landscape-declaration": True,
        "log-landscape-scan": True
    }

loglevels = conf.lookup("/logging/levels")
loglevels["console"] = console_level
loglevels["logfile"] = logfile_level

# Step 5 - Import the logging module so we get an initial configuration that
# points to standard out
import akit.xlogging.foundations # pylint: disable=unused-import,wrong-import-position
