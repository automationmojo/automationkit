
import inspect
import threading
import time

from akit.environment.variables import AKIT_VARIABLES
from akit.xlogging.foundations import getAutomatonKitLogger
from akit.wellknownports import PORT_DEBUGPY_ASSISTANT

logger = getAutomatonKitLogger()

class DEBUGGER:
    PDB = 'pdb'
    DEBUGPY = 'debugpy'

DEFAULT_DEBUG_PORT = 5678

class WELLKNOWN_BREAKPOINTS:
    TEST_DISCOVERY = "test-discovery"
    TESTRUN_START = "testrun-start"

def in_vscode_debugger():
    invscode = False
    for frame in inspect.stack():
        if frame[1].endswith("pydevd.py"):
            invscode = True
            break
    return invscode

def debugger_wellknown_breakpoint_entry(breakpoint_name: str):

    debugger = AKIT_VARIABLES.AKIT_DEBUGGER
    breakpoints = AKIT_VARIABLES.AKIT_BREAKPOINTS

    if breakpoints is not None:
        if breakpoint_name in breakpoints:
            if debugger == DEBUGGER.PDB:
                # The debug flag was passed on the commandline so we break here.'.format(current_indent))
                import pdb
                pdb.set_trace()
            elif debugger == DEBUGGER.DEBUGPY:
                logger.info("Waiting for debugger on port={}".format(DEFAULT_DEBUG_PORT))

                invscode = in_vscode_debugger()

                # The remote debug flag was passed on the commandline so we break here.'.format(current_indent))
                import debugpy
                if invscode:
                    debugpy.listen(("0.0.0.0", DEFAULT_DEBUG_PORT))
                    debugpy.wait_for_client()
                debugpy.breakpoint()
    return

def debugger_wellknown_breakpoint_code_append(breakpoint_name: str, code_lines: list, current_indent: str):

    debugger = AKIT_VARIABLES.AKIT_DEBUGGER
    breakpoints = AKIT_VARIABLES.AKIT_BREAKPOINTS

    if breakpoints is not None:
        if breakpoint_name in breakpoints:
            if debugger == DEBUGGER.PDB:
                code_lines.append('')
                code_lines.append('{}# The debug flag was passed on the commandline so we break here.'.format(current_indent))
                code_lines.append('{}import pdb'.format(current_indent))
                code_lines.append('{}pdb.set_trace()'.format(current_indent))
            elif debugger == DEBUGGER.DEBUGPY:
                invscode = in_vscode_debugger()

                code_lines.append('')
                code_lines.append('{}# The remote debug flag was passed on the commandline so we break here.'.format(current_indent))
                code_lines.append('{}import debugpy'.format(current_indent))
                if invscode:
                    code_lines.append('{}debugpy.listen(("0.0.0.0", {}))'.format(current_indent, DEFAULT_DEBUG_PORT))
                    code_lines.append('{}debugpy.wait_for_client()'.format(current_indent))
                code_lines.append('{}debugpy.breakpoint()'.format(current_indent))

                logger.info("Waiting for debugger on port={}".format(DEFAULT_DEBUG_PORT))

    return


class DebugPyAssistant():
    """
        The DebugPyAssistant is used to setup a daemon thread that creates a remote debug
        endpoint that can optionally connected to in order to remote debug a process running
        in the automation environment.
    """

    def __init__(self, name="DebugPyAssistant", *, endpoint=("0.0.0.0", PORT_DEBUGPY_ASSISTANT)):
        self._endpoint = endpoint
        self._running = True

        self._debug_thread = threading.Thread(name=name, target=self._entry_debug_server, daemon=True)
        self._debug_thread.start()
        return

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def thread(self):
        return self._debug_thread

    def _entry_debug_server(self):

        import debugpy
        debugpy.listen(self._endpoint)
        
        while self._running:
            debugpy.wait_for_client()
            debugpy.breakpoint()

            # While we are connected to the debugger, have the debug assistant
            # thread loop
            while debugpy.is_client_connected():
                time.sleep(2)

        return

