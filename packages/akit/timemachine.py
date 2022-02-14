
from typing import List, Optional

import os

from functools import wraps

from akit.environment.variables import AKIT_VARIABLES

class WELLKNOWN_PORTALS:
    TEST_DISCOVERY = "test-discovery"
    TESTRUN_START = "testrun-start"

class NetherPortal:
    """
        When you open a portal, if you are not time traveling, then you must pass
        from one realm to the next by going through 'The Nether'. There isn't much
        going on in 'The Nether' but keep a sharp eye out for 'The Creeper'.
    """
    
    def __init__(self):
        return

    def __enter__(self):

        # ░░░░░░░░░░░░░░░░░░░░░░░░░░
        # ░▓▓▓▒▒▒▓▓▓███▒▒▒███▓▓▓▒▒▒░
        # ░███▓▓▓▒▒▒▓▓▓███▒▒▒███▓▓▓░
        # ░▓▓▓░░░░░░▒▒▒▓▓▓░░░░░░███░
        # ░▒▒▒░░░░░░▓▓▓███░░░░░░▓▓▓░
        # ░▓▓▓▒▒▒███░░░░░░▓▓▓▒▒▒███░
        # ░▒▒▒███░░░░░░░░░░░░███▓▓▓░
        # ░███▓▓▓░░░░░░░░░░░░▒▒▒███░
        # ░▒▒▒███░░░███▒▒▒░░░▓▓▓▒▒▒░
        # ░▓▓▓▒▒▒▓▓▓▒▒▒███▓▓▓▒▒▒███░
        # ░▓▓▓▒▒▒▓▓▓▒▒▒███▓▓▓▒▒▒███░
        # ░░░░░░░░░░░░░░░░░░░░░░░░░░
        #    ░▒▒▒▓▓▓███▓▓▓▒▒▒███░
        #    ░▓▓▓▒▒▒▓▓▓███▓▓▓▒▒▒░
        #    ░███▓▓▓▒▒▒▓▓▓███▓▓▓░
        #    ░▒▒▒███▓▓▓███▓▓▓▒▒▒░
        #    ░███▓▓▓▒▒▒▓▓▓▒▒▒███░
        #    ░▓▓▓▒▒▒███▒▒▒▓▓▓▒▒▒░
        #    ░▒▒▒▓▓▓▒▒▒▓▓▓▒▒▒▓▓▓░
        # ░░░░░░░░░░░░░░░░░░░░░░░░░░
        # ░███▓▓▓▓▒▒▒▒░░▓▓▓▓████▒▒▒░
        # ░▒▒▒████▓▓▓▓░░████▒▒▒▒▓▓▓░
        # ░███▓▓▓▓████░░▓▓▓▓████▒▒▒░
        # ░░░░░░░░░░░░░░░░░░░░░░░░░░

        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        return False


THE_NETHER = NetherPortal()

timetravel_session_name = None

class TimePortal:
    """
        By creating a time portal, you pass into a place where time is somewhat
        expanded, because your generating tons of data, but where every trace of
        your existance is mapped.
    """
    
    def __init__(self, session_name):
        self._session_name = session_name
        self._tracer = None
        return

    def __enter__(self):
        # pycrunch_trace has a difficult way to setup configuration, so
        # don't import the "Trace" object until we have setup the
        # output directory and are ready to load the config.
        from pycrunch_trace.client.api.trace import Trace

        self._tracer = Trace()
        self._tracer.start(self._session_name)
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        self._tracer.stop()
        return False


def timeportal(portal_name: str, *, activations: Optional[List[str]]=None):
    """
       Starts tracing using PyCrunch tracing toolkit
    """
    def _decorator(func):

        @wraps(func)
        def wrapper(*args, **kws):
        
            session_name = str(func.__name__)

            with open_time_portal(portal_name, activations=activations) as portal:
                results = func(*args, **kws)
                return results

        return wrapper

    return _decorator


def open_time_portal(portal_name: str, activations: List[str]=[]):
    """
    """

    global timetravel_session_name

    portal = THE_NETHER

    activate_time_portal = False
    if AKIT_VARIABLES.AKIT_TIMETRAVEL:
        if portal_name in AKIT_VARIABLES.AKIT_TIMEPORTALS:
            activate_time_portal = True
        if len(activations) > 0:
            for akey in activations:
                if akey in AKIT_VARIABLES.AKIT_TIMEPORTALS:
                    activate_time_portal = True

    if activate_time_portal:
        if timetravel_session_name is None:
            from pycrunch_trace.config import config as pytrace_config
            from pathlib import Path
            from akit.paths import get_path_for_output

            output_path = get_path_for_output()

            timetravel_session_name = "timetravel_" + AKIT_VARIABLES.AKIT_RUNID.replace("-", "_")

            timetravel_directory = os.path.join(output_path, "timetravel")
            if not os.path.exists(timetravel_directory):
                os.makedirs(timetravel_directory)

            session_directory = os.path.join(output_path, "timetravel", timetravel_session_name)
            if not os.path.exists(session_directory):
                os.makedirs(session_directory)

            pytrace_config.working_directory = Path(output_path)
            pytrace_config.recording_directory = Path(timetravel_directory)

            portal = TimePortal(timetravel_session_name)

    return portal

def timemachine_timeportal_code_append(timeportal_name: str, code_lines: list, current_indent: str):

    add_indent = ""

    if AKIT_VARIABLES.AKIT_TIMETRAVEL and timeportal_name in AKIT_VARIABLES.AKIT_TIMEPORTALS:
        code_lines.append('')
        code_lines.append('{}# The time-travel flag was set and the "{}" portal was activated.'.format(
                            current_indent, timeportal_name))
        code_lines.append('{}from akit.timemachine import open_time_portal'.format(current_indent))
        code_lines.append('{}with open_time_portal("{}") as portal:'.format(current_indent, timeportal_name))

        add_indent = "    "

    return add_indent