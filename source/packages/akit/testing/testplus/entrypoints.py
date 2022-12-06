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


from akit.environment.context import Context
from akit.environment.variables import LOG_LEVEL_NAMES

from akit.paths import get_path_for_testresults
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

    base_parser = argparse.ArgumentParser()

    base_parser.add_argument("-i", "--include", dest="includes", action="append", default=[], help="Add an include search statement.")
    base_parser.add_argument("-x", "--exclude", dest="excludes", action="append", default=[], help="Add an exclude filter statement.")
    base_parser.add_argument("--console-level", dest="consolelevel", action="store", default="INFO", choices=LOG_LEVEL_NAMES, help="The logging level for console output.")
    base_parser.add_argument("--logfile-level", dest="logfilelevel", action="store", default="DEBUG", choices=LOG_LEVEL_NAMES, help="The logging level for logfile output.")

    test_module = sys.modules["__main__"]

    ctx = Context()
    env = ctx.lookup("/environment")

    # Set the jobtype
    env["jobtype"] = "testrun"

    test_results_dir = get_path_for_testresults()
    if not os.path.exists(test_results_dir):
        os.makedirs(test_results_dir)
    env["output_directory"] = test_results_dir

    test_root = find_testmodule_root(test_module)
    module_fullname = find_testmodule_fullname(test_module)

    # Copy the test module to the name of the module_fullname name so the loader won't reload it
    sys.modules[module_fullname] = test_module


    if test_module.__name__ == "__main__":
        test_module.__name__ = module_fullname

        # Re-map the object classes from the module over to the module name we just registered the test
        # module under.
        test_class_coll = inspect.getmembers(test_module, inspect.isclass)
        for testclass_name, testclass_obj in test_class_coll:
            tcobj_module_name = testclass_obj.__module__
            if tcobj_module_name == "__main__":
                testclass_obj.__module__ = module_fullname

    args = base_parser.parse_args()

    logging_initialize()

    includes = args.includes
    excludes = args.excludes
    if len(includes) == 0:
        includes.append("*")

    result_code = 0
    with DefaultTestJob(logger, test_root, includes=includes, excludes=excludes, test_module=test_module) as tjob:
        result_code = tjob.execute()

    sys.exit(result_code)

    return
