
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import List

import os
import sys

import click

from akit.environment.variables import LOG_LEVEL_NAMES

from akit.cli.cmdtree.testing.constants import (
    HELP_ROOT,
    HELP_EXCLUDES,
    HELP_INCLUDES,
    HELP_OUTPUT,
    HELP_START,
    HELP_BRANCH,
    HELP_BUILD,
    HELP_FLAVOR,
    HELP_OWNER,
    HELP_CREDENTIALS,
    HELP_LANDSCAPE,
    HELP_LANDSCAPE_NAME,
    HELP_RUNTIME,
    HELP_RUNTIME_NAME,
    HELP_TOPOLOGY,
    HELP_TOPOLOGY_NAME,
    HELP_RUNID,
    HELP_CONSOLE_LOG_LEVEL,
    HELP_FILE_LOG_LEVEL,
    HELP_DEBUGGER,
    HELP_BREAKPOINT,
    HELP_TIMETRAVEL,
    HELP_TIMEPORTAL,
    HELP_PRERUN_DIAGNOSTIC,
    HELP_POSTRUN_DIAGNOSTIC,
    HELP_INCLUDE_MARKER_EXP,
    HELP_EXCLUDE_MARKER_EXP
)

@click.command("run", help="Command used to run collections of tests.")
@click.option("--root", default=None,  type=str, required=False, help=HELP_ROOT)
@click.option("--excludes", "-x", multiple=True, required=False, help=HELP_EXCLUDES)
@click.option("--includes", "-i", multiple=True, help=HELP_INCLUDES)
@click.option("--output", "-o", default=None, required=False, help=HELP_OUTPUT)
@click.option("--start", default=None, required=False, help=HELP_START)
@click.option("--runid", default=None, required=False, help=HELP_RUNID)
@click.option("--branch", default=None, required=False, help=HELP_BRANCH)
@click.option("--build", default=None, required=False, help=HELP_BUILD)
@click.option("--flavor", default=None, required=False, help=HELP_FLAVOR)
@click.option("--owner", default=None, required=False, help=HELP_OWNER)
@click.option("--credentials", "credentials_file", default=None, required=False, help=HELP_CREDENTIALS)
@click.option("--landscape", "landscape_file", default=None, required=False, help=HELP_LANDSCAPE)
@click.option("--landscape-name", "landscape_name", default=None, required=False, help=HELP_LANDSCAPE_NAME)
@click.option("--runtime", "runtime_file", default=None, required=False, help=HELP_RUNTIME)
@click.option("--runtime-name", "runtime_name", default=None, required=False, help=HELP_RUNTIME_NAME)
@click.option("--topology", "topology_file", default=None, required=False, help=HELP_TOPOLOGY)
@click.option("--topology-name", "topology_name", default=None, required=False, help=HELP_TOPOLOGY_NAME)
@click.option("--console-level", default=None, required=False, type=click.Choice(LOG_LEVEL_NAMES, case_sensitive=False), help=HELP_CONSOLE_LOG_LEVEL)
@click.option("--logfile-level", default=None, required=False, type=click.Choice(LOG_LEVEL_NAMES, case_sensitive=False), help=HELP_FILE_LOG_LEVEL)
@click.option("--debugger", default=None, required=False, type=click.Choice(['pdb', 'debugpy']), help=HELP_DEBUGGER)
@click.option("--breakpoint", "breakpoints", default=None, required=False, multiple=True, type=click.Choice(['test-discovery', 'testrun-start']), help=HELP_BREAKPOINT)
@click.option("--time-travel", is_flag=True, default=False, required=False, help=HELP_TIMETRAVEL)
@click.option("--time-portal", "timeportals", default=None, required=False, multiple=True, help=HELP_TIMEPORTAL)
@click.option("--prerun-diagnostic", is_flag=True, default=False, required=False, help=HELP_PRERUN_DIAGNOSTIC)
@click.option("--postrun-diagnostic", is_flag=True, default=False, required=False, help=HELP_POSTRUN_DIAGNOSTIC)
@click.option("--include-marker-exp", required=False, multiple=True, help=HELP_INCLUDE_MARKER_EXP)
@click.option("--exclude-marker-exp", required=False, multiple=True, help=HELP_EXCLUDE_MARKER_EXP)
def command_akit_testing_run(root, includes, excludes, output, start, runid, branch, build, flavor, owner,
                        credentials_file, landscape_file, landscape_name, runtime_file, runtime_name,
                        topology_file, topology_name, console_level, logfile_level,
                        debugger, breakpoints, time_travel, timeportals, prerun_diagnostic,
                        postrun_diagnostic, include_marker_exp, exclude_marker_exp):

    # pylint: disable=unused-import,import-outside-toplevel

    # We do the imports of the automation framework code inside the action functions because
    # we don't want to startup loggin and the processing of inputs and environment variables
    # until we have entered an action method.  Thats way we know how to setup the environment.

    # IMPORTANT: We need to load the context first because it will trigger the loading
    # of the default user configuration
    from akit.environment.context import Context
    from akit.environment.contextpaths import ContextPaths

    from akit.environment.variables import extend_path, JOB_TYPES, AKIT_VARIABLES
    
    from akit.environment.optionoverrides import (
        override_build_branch,
        override_build_flavor,
        override_build_owner,
        override_build_name,
        override_config_credentials,
        override_config_landscape,
        override_config_landscape_name,
        override_config_runtime,
        override_config_runtime_name,
        override_config_topology,
        override_config_topology_name,
        override_loglevel_console,
        override_loglevel_file,
        override_output_directory,
        override_runid,
        override_starttime,
        override_testroot,
        override_debug_breakpoints,
        override_debug_debugger,
        override_timetravel,
        override_timeportals
    )

    ctx = Context()
    env = ctx.lookup("/environment")

    # We need to set the job type before we trigger activation.
    env["jobtype"] = JOB_TYPES.TESTRUN

    # We perform activation a little later in the testrunner.py file so we can
    # handle exceptions in the context of testrunner_main function
    import akit.activation.testrun
    from akit.xlogging.foundations import logging_initialize, getAutomatonKitLogger
    from akit.testing.testplus.markers import MetaFilter, parse_marker_expression

    if branch is not None:
        override_build_branch(branch)

    if build is not None:
        override_build_name(build)
    
    if flavor is not None:
        override_build_flavor(flavor)
    
    if owner is not None:
        override_build_owner(owner)

    if credentials_file is not None:
        override_config_credentials(credentials_file)

    if landscape_file is not None and landscape_name is not None:
        errmsg = "The '--landscape-file' and '--landscape-name' options should not be used together."
        raise click.BadOptionUsage("landscape-name", errmsg)

    if landscape_file is not None:
        override_config_landscape(landscape_file)

    if landscape_name is not None:
        override_config_landscape_name(landscape_name)

    if landscape_file is not None or landscape_name is not None:
        landscape_filename = AKIT_VARIABLES.AKIT_CONFIG_LANDSCAPE
        option_name = "landscape" if landscape_file is not None else "landscape-name"
        if not os.path.exists(landscape_filename):
            errmsg = "The specified landscape file does not exist. filename={}".format(landscape_filename)
            raise click.BadOptionUsage(option_name, errmsg)

    if runtime_file is not None and runtime_name is not None:
        errmsg = "The '--runtime-file' and '--runtime-name' options should not be used together."
        raise click.BadOptionUsage("runtime-name", errmsg)

    if runtime_file is not None:
        override_config_runtime(runtime_file)
    
    if runtime_name is not None:
        override_config_runtime_name(runtime_name)
    
    if runtime_file is not None or runtime_name is not None:
        runtime_filename = AKIT_VARIABLES.AKIT_CONFIG_RUNTIME
        option_name = "runtime" if runtime_file is not None else "runtime-name"
        if not os.path.exists(runtime_filename):
            errmsg = "The specified runtime file does not exist. filename={}".format(runtime_filename)
            raise click.BadOptionUsage(option_name, errmsg)

    if topology_file is not None and topology_name is not None:
        errmsg = "The '--topology-file' and '--topology-name' options should not be used together."
        raise click.BadOptionUsage("option_name", errmsg)

    if topology_file is not None:
        override_config_topology(topology_file)
    
    if topology_name is not None:
        override_config_topology_name(topology_name)

    if topology_file is not None or topology_name is not None:
        topology_filename = AKIT_VARIABLES.AKIT_CONFIG_TOPOLOGY
        option_name = "topology" if topology_file is not None else "topology-name"
        if not os.path.exists(topology_filename):
            errmsg = "The specified topology file does not exist. filename={}".format(topology_filename)
            raise click.BadOptionUsage(option_name, errmsg)

    if console_level is not None:
        override_loglevel_console(console_level)

    if logfile_level is not None:
        override_loglevel_file(logfile_level)

    if output is not None:
        override_output_directory(output)

    if start is not None:
        override_starttime(start)
    
    if runid is not None:
        override_runid(runid)

    # Process the commandline args here and then set the variables on the environment
    # as necessary.  We need to do this before we import activate.
    if breakpoints is not None:
        override_debug_breakpoints(breakpoints)

        # If a breakpoint was passed bug the debugger was not, use 'debugpy' for the
        # default debugger.
        if debugger is None:
            override_debug_debugger('debugpy')

    if debugger is not None:
        override_debug_debugger('debugpy')

    if time_travel is not None:
        override_timetravel(time_travel)

    if timeportals is not None:
        override_timeportals(timeportals)

    if prerun_diagnostic:
        ctx.insert("/environment/configuration/diagnostics/prerun-diagnostic", {})
    
    if postrun_diagnostic:
        ctx.insert("/environment/configuration/diagnostics/postrun-diagnostic", {})

    if root is None:
        if AKIT_VARIABLES.AKIT_TESTROOT is not None:
            root = AKIT_VARIABLES.AKIT_TESTROOT
        elif ctx.lookup(ContextPaths.TESTROOT) is not None:
            root = ctx.lookup(ContextPaths.TESTROOT)
        else:
            root = "."

    test_root = os.path.abspath(os.path.expandvars(os.path.expanduser(root)))
    if not os.path.isdir(test_root):
        errmsg = "The specified root folder does not exist. root=%s" % root
        if test_root != root:
            errmsg += " expanded=%s" % test_root
        raise click.BadParameter(errmsg)

    override_testroot(root)

    # Make sure we extend PATH to include the test roots parent folder so imports will
    # work properly.
    test_root_parent = os.path.dirname(test_root)
    extend_path(test_root_parent)

    metafilters: List[MetaFilter] = []
    for imexp in include_marker_exp:
        imexp = imexp.strip("\"")
        imexp = imexp.strip("'")
        mfilter = parse_marker_expression("+" + imexp)
        metafilters.append(mfilter)

    for exmexp in exclude_marker_exp:
        exmexp = exmexp.strip("\"")
        imexp = imexp.strip("'")
        mfilter = parse_marker_expression("-" + imexp)
        metafilters.append(mfilter)

    # Initialize logging
    logging_initialize()
    logger = getAutomatonKitLogger()

    from akit.extensionpoints import AKitExtensionPoints
    akep = AKitExtensionPoints()

    # At this point in the code, we either lookup an existing test job or we create a test job
    # from the includes, excludes or test_module
    TestJobType = akep.get_testplus_default_job_type()
    result_code = 0
    with TestJobType(logger, test_root, includes=includes, excludes=excludes, metafilters=metafilters,
                     branch=branch, build=build, flavor=flavor) as tjob:
        result_code = tjob.execute()

    sys.exit(result_code)

    return