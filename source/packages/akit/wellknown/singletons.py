
from typing import TYPE_CHECKING

from threading import Lock

from akit.extensionpoints import AKitExtensionPoints

if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

LANDSCAPE_SINGLETON = None

SINGLETON_LOCK = Lock()

def LandscapeSingleton() -> "Landscape":

    global SINGLETON_LOCK
    global LANDSCAPE_SINGLETON

    # If the singleton is already set, don't bother grabbing a lock
    # to set it.  The full path of the setting of the singleton will only
    # ever be taken once
    if LANDSCAPE_SINGLETON is None:
        SINGLETON_LOCK.acquire()
        try:
            if LANDSCAPE_SINGLETON is None:
                LandscapeType = AKitExtensionPoints().get_landscape_type()
                LANDSCAPE_SINGLETON = LandscapeType()
        finally:
            SINGLETON_LOCK.release()

    return LANDSCAPE_SINGLETON