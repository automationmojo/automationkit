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


from threading import RLock, Semaphore

from akit.exceptions import AKitLooperError


class LooperQueueShutdown:
    """
        The :class:`LooperShutdown` object provides a mechanism to tell :class:`Looper` threads
        the queue is shutdown and to exit.
    """

class LooperQueue:
    """
        The :class:`LooperQueue` provides an encapsulation of a queue, semaphore, and lock combination
        to be utilized and passed as one object.  Makes it easy to share the queue, semaphore, and
        lock between the :class:`LooperPool` and the :class:`Looper` threaded objects.
    """

    def __init__(self):
        self._queue = []
        self._queue_available = Semaphore(value=0)
        self._queue_lock = RLock()
        self._queue_shutdown = None
        return

    def push_work(self, packet: object):
        """
            Pushes a work packet for the :class:`LooperPool` threads to work on.
        """
        available = 0

        self._queue_lock.acquire()
        try:
            if self._queue_shutdown is not None:
                raise AKitLooperError("The queue has been shutdown, no more work is allowed to be queued.") from None

            self._queue.append(packet)
            self._queue_available.release()

            available = len(self._queue)
        finally:
            self._queue_lock.release()

        return available

    def push_work_packets(self, packets: list):
        """
            Pushes a list of work packets for the :class:`LooperPool` threads to work on.
        """

        available = 0

        self._queue_lock.acquire()
        try:
            if self._queue_shutdown is not None:
                raise AKitLooperError("The queue has been shutdown, no more work is allowed to be queued.") from None

            self._queue.extend(packets)
            self._queue_available.release()

            available = len(self._queue)
        finally:
            self._queue_lock.release()

        return available

    def pop(self):
        """
            Remove the next work packet from the :class:`LooperQueue` work queue.
        """
        packet= None

        self._queue_available.acquire()
        self._queue_lock.acquire()
        try:
            if len(self._queue) > 0:
                packet = self._queue.pop(0)

                if self._queue_shutdown is not None:
                    self._queue_shutdown.release()
        finally:
            self._queue_lock.release()

        return packet

    def shutdown_and_wait(self, notices):
        """
            Starts the queue shutdown and waits for the last work time to be removed
            from the queue.
        """

        self._queue_lock.acquire()
        try:
            for _ in range(0, notices):
                self._queue.append(LooperQueueShutdown())

            wcount = (len(self._queue) - 1) * -1
            self._queue_shutdown = Semaphore(value=wcount)
        finally:
            self._queue_lock.release()

        return
