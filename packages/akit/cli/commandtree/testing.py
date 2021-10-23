
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import os
import sys

import click

from akit.environment.variables import LOG_LEVEL_NAMES
from akit.exceptions import AKitSemanticError

@click.group("testing")
def group_testing():
    return

HELP_ROOT = "The root directory to use when scanning for tests."
HELP_EXCLUDES = "Add a test inclusion expression."
HELP_INCLUDES = "Add a test exclusion expression."
HELP_OUTPUT = "The output directory where results and artifacts are collected."
HELP_START = r"A time stamp to associate with the start of the run. Example: 2020-10-17T15:30:11.989120  Bash: date +%Y-%m-%dT%H:%M:%S.%N"
HELP_BRANCH = "The name of the branch to associate with the test run results."
HELP_BUILD = "The name of the build to associate with the test run results."
HELP_FLAVOR = "The name of the flavor to associate with the test run results."
HELP_CONSOLE_LOG_LEVEL = "The logging level for console output."
HELP_FILE_LOG_LEVEL = "The logging level for logfile output."
HELP_DEBUG = "Output debug information to the console."
HELP_DEBUGGER = "Debugger to active during the test run."
HELP_BREAKPOINT = "The breakpoint to activate for the test run."

@click.command("query")
@click.option("--root", default=None, type=str, help=HELP_ROOT)
@click.option("--excludes", "-x", multiple=True, help=HELP_EXCLUDES)
@click.option("--includes", "-i", multiple=True, help=HELP_INCLUDES)
@click.option("--debug", default=False, type=bool, help=HELP_DEBUG)
def command_testing_query(root, includes, excludes, debug):
    # pylint: disable=unused-import,import-outside-toplevel

    # We do the imports of the automation framework code inside the action functions because
    # we don't want to startup loggin and the processing of inputs and environment variables
    # until we have entered an action method.  Thats way we know how to setup the environment.

    # IMPORTANT: We need to load the context first because it will trigger the loading
    # of the default user configuration
    from akit.environment.context import Context
    from akit.environment.variables import extend_path, AKIT_VARIABLES

    ctx = Context()
    env = ctx.lookup("/environment")

    # Set the jobtype
    env["jobtype"] = "testrun"

    test_root = None
    if root is not None:
        AKIT_VARIABLES.AKIT_TESTROOT = root
    elif AKIT_VARIABLES.AKIT_TESTROOT is not None:
        root = AKIT_VARIABLES.AKIT_TESTROOT
    else:
        root = "."

    test_root = os.path.abspath(os.path.expandvars(os.path.expanduser(root)))
    if not os.path.isdir(test_root):
        errmsg = "The specified root folder does not exist. root=%s" % root
        if test_root != root:
            errmsg += " expanded=%s" % test_root
        raise click.BadParameter(errmsg)
    env["testroot"] = test_root

    # Make sure we extend PATH to include the test root
    extend_path(test_root)

    # We use console activation because all our input output is going through the terminal
    import akit.environment.console
    from akit.xlogging.foundations import logging_initialize, getAutomatonKitLogger

    # Initialize logging
    logging_initialize()
    logger = getAutomatonKitLogger()

    from akit.testing.reflection import (
        TestRootType, lookup_default_test_job_type, lookup_test_root_type)

    root_type = lookup_test_root_type(test_root)

    # At this point in the code, we either lookup an existing test job or we create a test job
    # from the includes, excludes or test_module
    TestJobType = lookup_default_test_job_type(test_root)
    result_code = 0
    with TestJobType(logger, test_root, includes=includes, excludes=excludes) as tjob:
        query_results = tjob.query()

        if root_type == TestRootType.UNITTEST:
            for tpname, tpobj in query_results.items():
                print()
                print("TestPack - %s" % tpname)

                testnames = [k for k in tpobj.test_references.keys()]
                testnames.sort()
                for tname in testnames:
                    print("    " + tname)
        else:
            test_names = [tn for tn in query_results.keys()]
            test_names.sort()
            print()
            print("Tests:")
            for tname in test_names:
                tref = query_results[tname]
                print("    " + tname)
                param_names = [pn for pn in tref.subscriptions.keys()]
                param_names.sort()
                for pname in param_names:
                    pinfo = tref.subscriptions[pname]
                    print ("        {}: {}".format(pname, pinfo.describe_source()))


        print()

        if len(tjob.import_errors) > 0:
            print("IMPORT ERRORS:", file=sys.stderr)
            for ifilename in tjob.import_errors:
                imperr_msg = ifilename
                print("    " + imperr_msg, file=sys.stderr)
            print("", file=sys.stderr)

    return

@click.command("run")
@click.option("--root", default=None,  type=str, required=False, help=HELP_ROOT)
@click.option("--excludes", "-x", multiple=True, required=False, help=HELP_EXCLUDES)
@click.option("--includes", "-i", multiple=True, help=HELP_INCLUDES)
@click.option("--output", "-o", default=None, required=False, help=HELP_OUTPUT)
@click.option("--start", default=None, required=False, help=HELP_START)
@click.option("--branch", default=None, required=False, help=HELP_BRANCH)
@click.option("--build", default=None, required=False, help=HELP_BUILD)
@click.option("--flavor", default=None, required=False, help=HELP_FLAVOR)
@click.option("--console-level", default=None, required=False, type=click.Choice(LOG_LEVEL_NAMES, case_sensitive=False), help=HELP_CONSOLE_LOG_LEVEL)
@click.option("--logfile-level", default=None, required=False, type=click.Choice(LOG_LEVEL_NAMES, case_sensitive=False), help=HELP_FILE_LOG_LEVEL)
@click.option("--debugger", default=None, required=False, type=click.Choice(['pdb', 'debugpy']), help=HELP_DEBUGGER)
@click.option("--breakpoint", default=None, required=False, type=click.Choice(['test-discovery', 'testrun-start']), help=HELP_BREAKPOINT)
def command_testing_run(root, includes, excludes, output, start, branch, build, flavor, console_level, logfile_level, debugger, breakpoint):

    # pylint: disable=unused-import,import-outside-toplevel

    # We do the imports of the automation framework code inside the action functions because
    # we don't want to startup loggin and the processing of inputs and environment variables
    # until we have entered an action method.  Thats way we know how to setup the environment.

    # IMPORTANT: We need to load the context first because it will trigger the loading
    # of the default user configuration
    from akit.environment.context import Context

    from akit.compat import import_by_name
    from akit.environment.variables import extend_path, JOB_TYPES, AKIT_VARIABLES

    try:

        ctx = Context()
        env = ctx.lookup("/environment")

        # Set the jobtype
        env["jobtype"] = JOB_TYPES.TESTRUN

        if branch is not None:
            AKIT_VARIABLES.AKIT_BRANCH = branch

        if build is not None:
            AKIT_VARIABLES.AKIT_BUILD = build
        
        if flavor is not None:
            AKIT_VARIABLES.AKIT_FLAVOR = flavor

        if output is not None:
            AKIT_VARIABLES.AKIT_OUTPUT_DIRECTORY = output

        if start is not None:
            AKIT_VARIABLES.AKIT_STARTTIME = start

        # Process the commandline args here and then set the variables on the environment
        # as necessary.  We need to do this before we import activate.
        if breakpoint is not None:
            AKIT_VARIABLES.AKIT_BREAKPOINT = breakpoint
            env["breakpoint"] = breakpoint

            # If a breakpoint was passed bug the debugger was not, use 'debugpy' for the
            # default debugger.
            if debugger is None:
                debugger = 'debugpy'

        if debugger is not None:
            AKIT_VARIABLES.AKIT_DEBUGGER = debugger
            env["debugger"] = debugger

        test_root = None
        if root is not None:
            AKIT_VARIABLES.AKIT_TESTROOT = root
        elif AKIT_VARIABLES.AKIT_TESTROOT is not None:
            root = AKIT_VARIABLES.AKIT_TESTROOT
        else:
            root = "."

        test_root = os.path.abspath(os.path.expandvars(os.path.expanduser(root)))
        if not os.path.isdir(test_root):
            errmsg = "The specified root folder does not exist. root=%s" % root
            if test_root != root:
                errmsg += " expanded=%s" % test_root
            raise click.BadParameter(errmsg)
        env["testroot"] = test_root

        # Make sure we extend PATH to include the test root
        extend_path(test_root)

        # We perform activation a little later in the testrunner.py file so we can
        # handle exceptions in the context of testrunner_main function
        import akit.environment.activate
        from akit.xlogging.foundations import logging_initialize, getAutomatonKitLogger

        # Initialize logging
        logging_initialize()
        logger = getAutomatonKitLogger()

        from akit.testing.reflection import lookup_default_test_job_type

        # At this point in the code, we either lookup an existing test job or we create a test job
        # from the includes, excludes or test_module
        TestJobType = lookup_default_test_job_type(test_root)
        result_code = 0
        with TestJobType(logger, test_root, includes=includes, excludes=excludes) as tjob:
            result_code = tjob.execute()

        sys.exit(result_code)

    finally:
        pass

    return

group_testing.add_command(command_testing_query)
group_testing.add_command(command_testing_run)
