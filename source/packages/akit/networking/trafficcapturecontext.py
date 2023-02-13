
from typing import Callable

import threading
import weakref

class TrafficCaptureContext:

    def __init__(self, owner: object, identifier: str, fromip: str, destroy_method: Callable):
        self._owner_ref = weakref.ref(owner)
        self._identifier = identifier
        self._fromip = fromip
        self._destroy_method = destroy_method
        self._lock = threading.Lock()
        self._captures = []
        return

    def __enter__(self):
        return self
    
    def __exit__(self, ex_type, ex_inst, ex_tb):
        self._destroy_method(self)
        return False

    @property
    def captures(self):
        rtnlist = None

        self._lock.acquire()
        try:
            rtnlist = [c for c in self._captures]
        finally:
            self._lock.release()

        return rtnlist
    
    @property
    def owner(self):
        return self._owner_ref()

    @property
    def fromip(self):
        self._fromip

    @property
    def identifier(self):
        return self._identifier

    def append_capture(self, req_headers: dict, req_body: str):

        self._lock.acquire()
        try:
            self._captures.append((req_headers, req_body))
        finally:
            self._lock.release()

        return