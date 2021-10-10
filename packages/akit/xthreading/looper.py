"""
.. module:: looper
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

from typing import Optional

from threading import Event, Thread

from akit.exceptions import AKitNotOverloadedError, AKitLooperError

from akit.xthreading.looperqueue import LooperQueue, LooperQueueShutdown

class Looper:
    """
        The :class:`Looper` is the worker thread for the :class:`LooperPool` object.
    """

    def __init__(self, queue:LooperQueue, name: Optional[str]=None, group: Optional[str]=None, daemon:Optional[bool]=None, **kwargs):
        self._name = name
        self._group = group
        self._kwargs = kwargs
        self._daemon = daemon

        self._running = False
        self._thread = None

        self._queue = queue

        self._exit_gate = None

        return

    def start(self):
        """
            Method for starting the looper.
        """
        self._exit_gate = Event()

        start_gate = Event()
        start_gate.clear()

        self._thread = Thread(target=self._loop_entry, name=self._name,
            args=(start_gate, self._queue), kwargs=None, daemon=self._daemon)

        self._thread.start()

        # Wait for the thread to start before we let the start method to return
        start_gate.wait()

        return

    def thread_get_name(self):
        return self._thread.name

    def thread_set_name(self, name):
        self._thread.name = name
        return

    def wait_for_exit(self, timeout: Optional[str]=None):
        """
            Method to wait for the looper thread to exit.
        """
        if self._exit_gate is None:
            raise AKitLooperError("Looper: wait_for_exit called before Looper was started.") from None

        self._exit_gate.wait(timeout=timeout)
        return

    def loop(self, packet) -> bool: # pylint: disable=no-self-use
        """
            Method that is overloaded by derived classes in order to implement a work loop.
        """
        raise AKitNotOverloadedError("Looper: _loop must be overloaded by derived classes.") from None

    def _loop_entry(self, start_gate: Event, queue: LooperQueue):
        """
            Protected method that serves as the thread target and that drives
            the work loop.
        """
        self._exit_gate.clear()

        self._running = True
        start_gate.set()
        start_gate = None

        while True:

            packet = queue.pop()

            # If we pop a LooperQueueShutdown from the queue
            # the queue is shut down and we should exit
            if isinstance(packet, LooperQueueShutdown):
                break

            # We may have been woken up so we can exit
            if packet is None or not self._running:
                break

            self.loop(packet)

            # end while True

        return
