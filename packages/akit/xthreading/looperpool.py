
"""
.. module:: akit.xthreading.looper
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains a Looper for repeating a loop function useful
        for repeated, work packet or queue processing.

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

from threading import RLock

from akit.exceptions import AKitLooperError

from akit.xthreading.looper import Looper
from akit.xthreading.looperqueue import LooperQueue

class LooperPool:
    """
        The :class:`LooperPool` provides a convenient way to setup a thread pool and worker threads.  The
        :class:`LooperPool` is passed a type derived from :class:`Looper` in order to customize the work
        performed by the :class:`LooperPool`
    """

    def __init__(self, looper_type, group_name: str=None, min: int=5, max: int=10, highwater: int=5, daemon=True, **kwargs):
        self._looper_type = looper_type
        self._group_name = group_name
        self._min = min
        self._max = max
        self._highwater = highwater
        self._kwargs = kwargs

        self._queue = LooperQueue()

        self._running = False

        self._threads_lock = RLock()
        self._threads = []
        self._thread_count = 0
        return

    def push_work(self, packet: object):
        """
            Pushes a work packet for the :class:`LooperPool` threads to work on.
        """

        if self._running:
            available = self._queue.push_work(packet)
            if available > self._highwater:
                self._threads_lock.acquire()
                try:
                    if self._thread_count < max:
                        self._locked_start_looper()
                finally:
                    self._threads_lock.release()
        else:
            raise AKitLooperError("LooperPool: push_work called after the looper pool has been shutdown.")

        return available

    def push_work_packets(self, packets: list):
        """
            Pushes a list of work packets for the :class:`LooperPool` threads to work on.
        """

        if self._running:
            available = self._queue.push_work_packets(packets)
            if available > self._highwater:
                self._threads_lock.acquire()
                try:
                    if self._thread_count < max:
                        self._locked_start_looper()
                finally:
                    self._threads_lock.release()
        else:
            raise AKitLooperError("LooperPool: push_work_packets called after the looper pool has been shutdown.")

        return available

    def shutdown(self):
        """
            Shutdown the :class:`LooperPool` and its worker threads.
        """

        # Set running to False to disallow the queueing of new work
        self._running = False

        

        return

    def start(self):
        """
            Starts the :class:`LooperPool` with the minimum number of threads.
        """

        if self._running:
            raise AKitLooperError("LooperPool: start called while LooperPool is already running")

        self._threads_lock.acquire()
        try:
            # We start up the minimum number of threads
            for _ in range(0, min):
                self._locked_start_looper()
        finally:
            self._threads_lock.release()

        return

    def _locked_start_looper(self):
        """
            Starts up a new :class:`Looper` worker thread.
        """

        try:
            self._thread_count += 1
            looper_name = "%s-%d" % (self._group_name, self._thread_count)
            looper = self._looper_type(self._queue, name=looper_name, group=self._group_name, daemon=True, **self._kwargs)
            looper.start()
            self._threads.append(looper)
        except:
            self._thread_count -= 1
            raise

        return