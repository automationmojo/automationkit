
from enum import IntEnum

class UpnpEventVarState(IntEnum):
    """
        An enumeration that indicates the state of the event variable.
    """
    UnInitialized = 0
    Default = 1
    Valid = 2
    Stale = 3
