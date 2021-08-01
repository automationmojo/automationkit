
from akit.environment.context import Context


from akit.environment.context import Context
from akit.xlogging.foundations import getAutomatonKitLogger

context = Context()

logger = getAutomatonKitLogger()

class DEBUGGER:
    PDB = 'pdb'
    DEBUGPY = 'debugpy'

DEFAULT_DEBUG_PORT = 5678

class WELLKNOWN_BREAKPOINTS:
    TEST_DISCOVERY = "test-discovery"
    TESTRUN_START = "test-discovery"

def debugger_wellknown_breakpoint_entry(breakpoint_name: str):
    env = context.lookup("/environment")

    debugger = env["debugger"]
    breakpoint = env["breakpoint"]

    if breakpoint == breakpoint_name:
        if debugger == DEBUGGER.PDB:
            # The debug flag was passed on the commandline so we break here.'.format(current_indent))
            import pdb
            pdb.set_trace()
        elif debugger == DEBUGGER.DEBUGPY:
            logger.info("Waiting for debugger on port={}".format(DEFAULT_DEBUG_PORT))

            # The remote debug flag was passed on the commandline so we break here.'.format(current_indent))
            import debugpy
            debugpy.listen(DEFAULT_DEBUG_PORT)
            debugpy.wait_for_client()
            debugpy.breakpoint()
    return

def debugger_wellknown_breakpoint_code_append(breakpoint_name: str, code_lines: list, current_indent: str):

    env = context.lookup("/environment")

    debugger = env["debugger"]
    breakpoint = env["breakpoint"]

    if breakpoint == breakpoint_name:
        if debugger == DEBUGGER.PDB:
            code_lines.append('')
            code_lines.append('{}# The debug flag was passed on the commandline so we break here.'.format(current_indent))
            code_lines.append('{}import pdb'.format(current_indent))
            code_lines.append('{}pdb.set_trace()'.format(current_indent))
        elif debugger == DEBUGGER.DEBUGPY:
            code_lines.append('')
            code_lines.append('{}# The remote debug flag was passed on the commandline so we break here.'.format(current_indent))
            code_lines.append('{}import debugpy'.format(current_indent))
            code_lines.append('{}debugpy.listen(56789)'.format(current_indent))

            logger.info("Waiting for debugger on port=56789")

            code_lines.append('{}debugpy.wait_for_client()'.format(current_indent))
            code_lines.append('{}debugpy.breakpoint()'.format(current_indent))
    return