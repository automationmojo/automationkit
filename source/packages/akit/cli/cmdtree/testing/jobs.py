
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

import click

from akit.environment.variables import LOG_LEVEL_NAMES

@click.group("jobs", help="Contains commands for working with test jobs.")
def group_akit_testing_jobs():
    return

HELP_ROOT = "The root directory to use when scanning for tests."
HELP_JOB = "The identifier of the job to run."
HELP_FILTER = "Add a job filter expression."
HELP_OUTPUT = "The output directory where results and artifacts are collected."
HELP_START = r"A time stamp to associate with the start of the run. Example: 2020-10-17T15:30:11.989120  Bash: date +%Y-%m-%dT%H:%M:%S.%N"
HELP_BRANCH = "The name of the branch to associate with the test run results."
HELP_BUILD = "The name of the build to associate with the test run results."
HELP_FLAVOR = "The name of the flavor to associate with the test run results."
HELP_CONSOLE_LOG_LEVEL = "The logging level for console output."
HELP_FILE_LOG_LEVEL = "The logging level for logfile output."
HELP_DEBUG = "Output debug information to the console."

@click.command("list")
@click.option("--root", default=".", type=str, help=HELP_ROOT)
@click.option("--filter", "-f", required=False, help=HELP_FILTER)
@click.option("--debug", default=False, type=bool, help=HELP_DEBUG)
def command_testing_jobs_list():
    return

@click.command("show")
@click.option("--root", default=".", type=str, help=HELP_ROOT)
@click.option("--job", "-j", required=True, help=HELP_JOB)
@click.option("--debug", default=False, type=bool, help=HELP_DEBUG)
def command_akit_testing_jobs_show():
    return

@click.command("run")
@click.option("--root", default=".", type=str, help=HELP_ROOT)
@click.option("--job", "-j", required=True, help=HELP_JOB)
@click.option("--output", "-o", required=False, help=HELP_OUTPUT)
@click.option("--start", default=None, required=False, help=HELP_START)
@click.option("--branch", default=None, required=False, help=HELP_BRANCH)
@click.option("--build", default=None, required=False, help=HELP_BUILD)
@click.option("--flavor", default=None, required=False, help=HELP_FLAVOR)
@click.option("--console-level", default=None, required=False, type=click.Choice(LOG_LEVEL_NAMES, case_sensitive=False), help=HELP_CONSOLE_LOG_LEVEL)
@click.option("--logfile-level", default=None, required=False, type=click.Choice(LOG_LEVEL_NAMES, case_sensitive=False), help=HELP_FILE_LOG_LEVEL)
def command_akit_testing_jobs_run(root, job, output, start, branch, build, flavor, console_level, logfile_level):

    # pylint: disable=unused-import,import-outside-toplevel

    # We do the imports of the automation framework code inside the action functions because
    # we don't want to startup loggin and the processing of inputs and environment variables
    # until we have entered an action method.  Thats way we know how to setup the environment.

    # IMPORTANT: We need to load the context first because it will trigger the loading
    # of the default user configuration
    from akit.environment.context import Context

    from akit.compat import import_by_name
    from akit.environment.variables import extend_path

    try:
        ctx = Context()
        ctx.insert("/environment/jobtype", 'testrun')

        test_root = os.path.abspath(os.path.expandvars(os.path.expanduser(root)))
        if not os.path.isdir(test_root):
            errmsg = "The specified root folder does not exist. root=%s" % root
            if test_root != root:
                errmsg += " expanded=%s" % test_root
            raise argparse.ArgumentError("--root", errmsg)

        # Make sure we extend PATH to include the test root
        extend_path(test_root)

        # We perform activation a little later in the testrunner.py file so we can
        # handle exceptions in the context of testrunner_main function
        import akit.activation.testrun
        from akit.xlogging.foundations import logging_initialize, getAutomatonKitLogger

        # Initialize logging
        logging_initialize()
        logger = getAutomatonKitLogger()

        from akit.extensionpoints import AKitExtensionPoints
        akep = AKitExtensionPoints()

        # At this point in the code, we either lookup an existing test job or we create a test job
        # from the includes, excludes or test_module
        TestJobType = akep.get_testplus_default_job_type()

        if job is not None:
            job_parts = job.split("@")
            if len(job_parts) != 2:
                errmsg = "A --job parameter must be of the form 'package.module@JobClass'"
                raise click.UsageError(errmsg)

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
        with TestJobType(logger, test_root) as tjob:
            result_code = tjob.execute()

        sys.exit(result_code)

    finally:
        pass

    return

group_akit_testing_jobs.add_command(command_akit_testing_jobs_show)
group_akit_testing_jobs.add_command(command_akit_testing_jobs_run)
