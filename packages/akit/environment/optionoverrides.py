from typing import List

from datetime import datetime

from akit.environment.context import Context
from akit.environment.contextpaths import ContextPaths
from akit.environment.variables import AKIT_VARIABLES

ctx = Context()

def override_build_branch(branch_name: str):
    """
        This override function provides a mechanism overriding the AKIT_BUILD_BRANCH
        variable and context configuration setting.

        :param branch: The name of the branch the build came from.
    """
    ctx.insert(ContextPaths.BUILD_BRANCH, branch_name)
    AKIT_VARIABLES.AKIT_BUILD_BRANCH = branch_name
    return

def override_build_flavor(build_flavor: str):
    """
        This override function provides a mechanism overriding the AKIT_BUILD_BRANCH
        variable and context configuration setting.

        :param breakpoints: A list of wellknown breakpoints that have been activated.
    """
    ctx.insert(ContextPaths.BUILD_FLAVOR, build_flavor)
    AKIT_VARIABLES.AKIT_BUILD_FLAVOR = build_flavor
    return

def override_build_name(build_name: str):
    """
        This override function provides a mechanism overriding the AKIT_BUILD_BRANCH
        variable and context configuration setting.

        :param breakpoints: A list of wellknown breakpoints that have been activated.
    """
    ctx.insert(ContextPaths.BUILD_NAME, build_name)
    AKIT_VARIABLES.AKIT_BUILD_NAME = build_name
    return

def override_config_credentials(filename: str):
    """
        This override function provides a mechanism overriding the AKIT_CONFIG_CREDENTIALS
        variable and context configuration setting.

        :param filename: The full path to the file to set as the credentials file.
    """
    ctx.insert(ContextPaths.CONFIG_FILE_CREDENTIALS, filename)
    AKIT_VARIABLES.AKIT_CONFIG_CREDENTIALS = filename
    return

def override_config_landscape(filename: str):
    """
        This override function provides a mechanism overriding the AKIT_CONFIG_LANDSCAPE
        variable and context configuration setting.

        :param filename: The full path to the file to set as the landscape file.
    """
    ctx.insert(ContextPaths.CONFIG_FILE_LANDSCAPE, filename)
    AKIT_VARIABLES.AKIT_CONFIG_LANDSCAPE = filename
    return

def override_config_runtime(filename: str):
    """
        This override function provides a mechanism overriding the AKIT_CONFIG_RUNTIME
        variable and context configuration setting.

        :param filename: The full path to the file to set as the runtime file.
    """
    ctx.insert(ContextPaths.CONFIG_FILE_RUNTIME, filename)
    AKIT_VARIABLES.AKIT_CONFIG_RUNTIME = filename
    return

def override_config_runtime_name(runtime_name: str):
    """
        This override function provides a mechanism overriding the AKIT_CONFIG_RUNTIME_NAME
        variable and context configuration setting.

        :param runtime_name: The name of the runtime to use when selecting a runtime file.
    """
    last_runtime_name = AKIT_VARIABLES.AKIT_CONFIG_RUNTIME_NAME

    ctx.insert(ContextPaths.CONFIG_FILE_RUNTIME_NAME, runtime_name)
    AKIT_VARIABLES.AKIT_CONFIG_RUNTIME_NAME = runtime_name

    rf_head, rf_middle, rf_tail = AKIT_VARIABLES.AKIT_CONFIG_TOPOLOGY_NAME.rpartition(last_runtime_name, runtime_name)
    if rf_middle != last_runtime_name:
        errmsg = "We should have found the name '{}' in the runtime file path.".format(last_runtime_name)
        raise RuntimeError(errmsg)

    runtime_filename = "".join(rf_head, runtime_name, rf_tail)
    ctx.insert(ContextPaths.CONFIG_FILE_RUNTIME, runtime_filename)
    AKIT_VARIABLES.AKIT_CONFIG_RUNTIME = runtime_filename
    return

def override_config_topology(filename: str):
    """
        This override function provides a mechanism overriding the AKIT_CONFIG_TOPOLOGY
        variable and context configuration setting.

        :param filename: The full path to the file to set as the topology file.
    """
    ctx.insert(ContextPaths.CONFIG_FILE_TOPOLOGY, filename)
    AKIT_VARIABLES.AKIT_CONFIG_TOPOLOGY = filename
    return

def override_config_topology_name(topology_name: str):
    """
        This override function provides a mechanism overriding the AKIT_CONFIG_TOPOLOGY_NAME
        variable and context configuration setting.

        :param topology_name: The name of the topology to use when selecting a topology file.
    """
    last_topology_name = AKIT_VARIABLES.AKIT_CONFIG_TOPOLOGY_NAME

    ctx.insert(ContextPaths.CONFIG_FILE_TOPOLOGY_NAME, topology_name)
    AKIT_VARIABLES.AKIT_CONFIG_TOPOLOGY_NAME = topology_name

    tf_head, tf_middle, tf_tail = AKIT_VARIABLES.AKIT_CONFIG_TOPOLOGY_NAME.rpartition(last_topology_name, topology_name)
    if tf_middle != last_topology_name:
        errmsg = "We should have found the name '{}' in the topology file path.".format(last_topology_name)
        raise RuntimeError(errmsg)

    topology_filename = "".join(tf_head, topology_name, tf_tail)
    ctx.insert(ContextPaths.CONFIG_FILE_TOPOLOGY_NAME, topology_filename)
    AKIT_VARIABLES.AKIT_CONFIG_TOPOLOGY_NAME = topology_filename

    return

def override_config_user(filename: str):
    """
        This override function provides a mechanism overriding the AKIT_CONFIG_USER
        variable and context configuration setting.

        :param filename: The full path to the file to set as the topology file.
    """
    ctx.insert(ContextPaths.CONFIG_FILE_USER, filename)
    AKIT_VARIABLES.AKIT_CONFIG_USER = filename
    return

def override_debug_breakpoints(breakpoints: List[str]):
    """
        This override function provides a mechanism overriding the AKIT_BREAKPOINTS
        variable and context configuration setting.

        :param breakpoints: A list of wellknown breakpoints that have been activated.
    """
    ctx.insert(ContextPaths.DEBUG_BREAKPOINTS, breakpoints)
    AKIT_VARIABLES.AKIT_BREAKPOINTS = breakpoints
    return

def override_debug_debugger(debugger: str):
    """
        This override function provides a mechanism overriding the AKIT_DEBUGGER
        variable and context configuration setting.
    """
    ctx.insert(ContextPaths.DEBUG_DEBUGGER, debugger)
    AKIT_VARIABLES.AKIT_DEBUGGER = debugger
    return

def override_loglevel_console(level: str):
    """
        This override function provides a mechanism overriding the AKIT_LOG_LEVEL_CONSOLE
        variable and context configuration setting.
    """
    ctx.insert(ContextPaths.LOGGING_LEVEL_CONSOLE, level)
    AKIT_VARIABLES.AKIT_LOG_LEVEL_CONSOLE = level
    return

def override_loglevel_file(level: str):
    """
        This override function provides a mechanism overriding the AKIT_LOG_LEVEL_FILE
        variable and context configuration setting.
    """
    ctx.insert(ContextPaths.LOGGING_LEVEL_LOGFILE, level)
    AKIT_VARIABLES.AKIT_LOG_LEVEL_FILE = level
    return

def override_output_directory(output_directory: str):
    """
        This override function provides a mechanism overriding the AKIT_STARTTIME
        variable and context configuration setting.

        :param output_directory: The base directory that all output artifacts will be written under.
    """
    ctx.insert(ContextPaths.OUTPUT_DIRECTORY, output_directory)
    AKIT_VARIABLES.AKIT_OUTPUT_DIRECTORY = output_directory
    return

def override_runid(runid: str):
    """
        This override function provides a mechanism overriding the AKIT_RUNID
        variable and context configuration setting.

        :param runid: A uuid string that represents the instance of this automation run.
    """
    ctx.insert(ContextPaths.RUNID, runid)
    AKIT_VARIABLES.AKIT_RUNID = runid
    return

def override_starttime(starttime: datetime):
    """
        This override function provides a mechanism overriding the AKIT_STARTTIME
        variable and context configuration setting.

        :param starttime: The date and time to set as the starttime of this run.
    """
    ctx.insert(ContextPaths.STARTTIME, starttime)
    AKIT_VARIABLES.AKIT_STARTTIME = starttime
    return

def override_testroot(testroot: str):
    """
        This override function provides a mechanism overriding the AKIT_TESTROOT
        variable and context configuration setting.

        :param testroot: The full path of the root of the tests folder.
    """
    AKIT_VARIABLES.AKIT_TESTROOT = testroot
    ctx.insert(ContextPaths.TESTROOT, testroot)
    return

def override_timetravel(allowed: bool):
    """
        This override function provides a mechanism overriding the AKIT_TIMETRAVEL
        variable and context configuration setting.
    """
    ctx.insert(ContextPaths.TIMETRAVEL, allowed)
    AKIT_VARIABLES.AKIT_TIMETRAVEL = allowed
    return

def override_timeportals(active_portals: List[str]):
    """
        This override function provides a mechanism overriding the AKIT_TIMEPORTALS
        variable and context configuration setting.
    """
    ctx.insert(ContextPaths.TIMEPORTALS, active_portals)
    AKIT_VARIABLES.AKIT_TIMEPORTALS = active_portals
    return