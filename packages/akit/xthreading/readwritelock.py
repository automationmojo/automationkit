
"""
.. module:: looperqueue
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains a :class:`LooperQueue` which provides a thread-safe queue for
        for the :class:`Looper` and :class:`LooperPool`.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import threading
import time

from akit.exceptions import AKitSemanticError

class ReadWriteLock:
    """
        The :class:`ReadWriteLock` implements a lock with read/write semantics that allows multiple
        readers threads to hold read access to the lock at a time or that allows a single writer to
        hold write access to the lock.
    """


    def __init__(self):
        """
            Initializes the :class:`ReadWriteLock`.
        """
        self._read_gate = threading.Event()
        self._read_gate.set()
        self._write_gate = threading.Semaphore(1)
        self._read_write_pivot = 0
        self._lock = threading.Lock()

        self._readers = []
        self._writer = None
        self._writers_waiting = 0
        return

    def acquire_read(self, timeout=None):
        """
            Method called by a thread to acquire read access on the :class:`ReadWriteLock`.
        """
        self._read_gate.wait()

        tid = threading.get_ident()
        start_time = time.time()
        stop_time = start_time + timeout

        try:
            self._lock.acquire()
            try:
                self._readers.append(tid)

                while True:
                    if self._read_write_pivot >= 0:
                        self._read_write_pivot += 1
                        break

                    self._lock.release()
                    try:
                        time_left = stop_time - time.time()
                        if time_left < 0:
                            raise TimeoutError("Timeout waiting on read lock.")

                        self._read_gate.wait(timeout=time_left)
                    finally:
                        self._lock.acquire()

            finally:
                self._lock.release()
        except TimeoutError as toerr:
            now_time = time.time()
            elapsed = now_time - start_time
            errmsg = "Timeout waiting to acquire read lock. start=%d end=%d elapsed=%d" % (start_time, now_time, elapsed)
            raise TimeoutError(errmsg) from toerr

        return

    def acquire_write(self, timeout=None):
        """
            Method called by a thread to acquire write access on the :class:`ReadWriteLock`.
        """
        tid = threading.get_ident()
        start_time = time.time()
        stop_time = start_time + timeout

        # Block new readers from starting to read
        self._read_gate.clear()

        try:
            self._lock.acquire()
            self._writers_waiting += 1
            try:
                while self._read_write_pivot != 0:
                    self._lock.release()
                    try:

                        time_left = stop_time - time.time()
                        if time_left < 0:
                            raise TimeoutError("Timeout waiting on write lock.")

                        self._write_gate.acquire(timeout=time_left)

                    finally:
                        self._lock.acquire()

                self._writers_waiting -= 1
                self._read_write_pivot = -1
                self._writer = tid
            finally:
                self._lock.release()
        except TimeoutError as toerr:
            now_time = time.time()
            elapsed = now_time - start_time
            errmsg = "Timeout waiting to acquire write lock. start=%d end=%d elapesed=%d" % (start_time, now_time, elapsed)
            raise TimeoutError(errmsg) from toerr

        return

    def release_read(self):
        """
            Method called by a thread to release read access on the :class:`ReadWriteLock`.
        """
        tid = threading.get_ident()

        self._lock.acquire()
        try:
            if tid not in self._readers:
                raise AKitSemanticError("Thread id(%d) attempting to release read lock when it was not owned." % tid) from None

            if self._read_write_pivot <= 0:
                raise AKitSemanticError("Thread id(%d) is attempting to release the ReadWriteLock when it is in a write or neutral state." % tid) from None

            self._read_write_pivot -= 1

        finally:
            self._lock.release()

        return

    def release_write(self):
        """
            Method called by a thread to release write access on the :class:`ReadWriteLock`.
        """
        tid = threading.get_ident()

        self._lock.acquire()
        try:
            if self._writer != tid:
                raise AKitSemanticError("Thread id(%d) attempting to release write lock when it was not owned." % tid) from None

            if self._read_write_pivot >= 0:
                raise AKitSemanticError("Thread id(%d) is attempting to release the ReadWriteLock when it is in a read or neutral state." % tid) from None

            self._read_write_pivot += 1

            # Make the decision to allow readers before we let any waiting writers change
            # the count of self._writers_waiting
            if self._writers_waiting == 0:
                self._read_gate.set()

            # Don't release the write gate until we have checked to see if another writer is waiting
            self._write_gate.release()
        finally:
            self._lock.release()

        return
