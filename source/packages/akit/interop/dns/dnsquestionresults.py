
import threading
import weakref

class DnsQuestionResults:
    """
        The :class:`DnsQuestionResults` object is utilized to formulate DNS querys and to check to
        see if a :class:`DnsRecord` answers the query provided.
    """

    def __init__(self, owner):
        self._owner_ref = weakref.ref(owner)

        self._lock = threading.Lock()
        self._responses = []
        return
    
    @property
    def owner(self):
        return self._owner_ref()

    @property
    def responses(self):
        rlist = []

        self._lock.acquire()
        try:
            rlist = [r for r in self._responses]
        finally:
            self._lock.release()

        return rlist

    def add_response(self, response):
        self._responses.append(response)
        return
    
    def cleanup(self):
        return