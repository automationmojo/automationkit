
from akit.exceptions import AKitValueError

# NOTE: This file needs to be importable very early in the startup process
# so don't do any logging, use any external resources or dependencies
# in here.  The state of all functions should be threadsafe and self contained.
# The functions should only use what is passed in, process it, and provide an
# output.

STRINGS_FOR_FALSE = [
    "0",
    "FALSE",
    "NO",
    "OFF"
]

STRINGS_FOR_TRUE = [
    "1",
    "TRUE",
    "YES",
    "ON"
]

def string_to_bool(sval: str) -> bool:
    """
        Converts a string value to a boolean value.

        :returns: Coverted boolean result.
    """
    bval = None

    sval = sval.upper()
    if sval in STRINGS_FOR_FALSE:
        bval = False
    elif sval in STRINGS_FOR_TRUE:
        bval = True
    else:
        raise AKitValueError("Invalid parameter, unable to convert '{}' to bool.".format(sval))

    return bval
