
from akit.exceptions import AKitValueError

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
