
import traceback

def format_exc_lines():
    """
        Gets a 'format_exc' result and splits it into mutliple lines.
    """
    rtn_lines = traceback.format_exc().splitlines()
    return rtn_lines