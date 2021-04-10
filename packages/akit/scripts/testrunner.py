#!/usr/bin/env python3
"""
.. module:: testrunner.py
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Script used to run 'TestJobs', 'TestPacks' and 'Tests'.

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
import os
import sys

# IMPORTANT: We need to load the context first because it will trigger the loading
# of the default user configuration
from akit.environment.context import Context

from akit.compat import import_by_name
from akit.environment.variables import extend_path
from akit.environment.options import ENVIRONMENT_OPTIONS

def testrunner_main():
    """
        The main entry point function for the testrunner.py script.
    """
    # pylint: disable=unused-import,import-outside-toplevel

    parser = argparse.ArgumentParser()

    for opt_args, opt_kwargs in ENVIRONMENT_OPTIONS:
        parser.add_argument(*opt_args, **opt_kwargs)

    parser.add_argument("-r", "--root", dest="root", action="store", default=".", help="The root directory to scan for tests.")
    parser.add_argument("-j", "--job", dest="job", action="store", default=None, help="The identifier of the job to run.")
    parser.add_argument("-i", "--include", dest="includes", action="append", default=[], help="Add an include search statement.")
    parser.add_argument("-x", "--exclude", dest="excludes", action="append", default=[], help="Add an exclude filter statement.")

    args = parser.parse_args()

    try:
        ctx = Context()
        env = ctx.lookup("/environment")

        # Set the jobtype
        env["jobtype"] = "testrun"

        test_root = os.path.abspath(os.path.expandvars(os.path.expanduser(args.root)))
        if not os.path.isdir(test_root):
            errmsg = "The specified root folder does not exist. root=%s" % args.root
            if test_root != args.root:
                errmsg += " expanded=%s" % test_root
            raise argparse.ArgumentError("--root", errmsg)

        # Make sure we extend PATH to include the test root
        extend_path(test_root)

        # We perform activation a little later in the testrunner.py file so we can
        # handle exceptions in the context of testrunner_main function
        import akit.environment.activate
        from akit.xlogging.foundations import logging_initialize, getAutomatonKitLogger

        # Initialize logging
        logging_initialize()
        logger = getAutomatonKitLogger()

        job = args.job
        includes = args.includes
        excludes = args.excludes

        if job is None and includes is None:
            errmsg = "You must specify either --job or --includes in order to include at least one test to run."
            raise argparse.ArgumentError("--job", errmsg)

        if job is not None and (len(includes) > 0 or len(excludes) > 0):
            errmsg = "The --job arguement cannot be used with the --includes or --excludes flags."
            raise argparse.ArgumentError("--job", errmsg)

        from akit.testing.unittest.testjob import DefaultTestJob

        # At this point in the code, we either lookup an existing test job or we create a test job
        # from the includes, excludes or test_module
        TestJobType = DefaultTestJob
        if job is not None:
            job_parts = job.split("@")
            if len(job_parts) != 2:
                errmsg = "A --job parameter must be of the form 'package.module@JobClass'"
                raise argparse.ArgumentError("--job", errmsg)

            job_package, job_class = job_parts

            try:
                job_mod = import_by_name(job_package)
            except ImportError as imperr:
                errmsg = "Failure while importing job package %r"  % job_package
                raise argparse.ArgumentError("--job", errmsg) from imperr

            if not hasattr(job_mod, job_class):
                errmsg = "The job package %r does not have a job type %r." % (job_package, job_class)
                raise argparse.ArgumentError("--job", errmsg)

            TestJobType = getattr(job_mod, job_class)

        result_code = 0
        with TestJobType(logger, test_root, includes=includes, excludes=excludes) as tjob:
            result_code = tjob.execute()

        sys.exit(result_code)

    finally:
        pass

    return

if __name__ == "__main__":
    testrunner_main()
