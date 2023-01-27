"""
.. module:: timeouts
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains framework timeout constants.

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

import os

from typing import List, Optional

from datetime import datetime, timedelta

from akit.exceptions import AKitTimeoutError

DEFAULT_WAIT_DELAY = 0
DEFAULT_WAIT_INTERVAL = 5
DEFAULT_WAIT_TIMEOUT = 60

DEFAULT_SSH_COMMAND_TIMEOUT = 30

DEFAULT_WHATFOR_TEMPLATE = "Timeout waiting for {}"

MSG_TEMPL_TIME_COMPONENTS = "    timeout={} start_time={}, end_time={} now_time={} time_diff={}"

class TimeoutState:
    TimedOut = -1
    NotStarted = 0
    Tracking = 1
    Completed = 2
    Running = 3

class TimeoutContext:
    """
        The :class:`TimeoutContext` object is used to store the context used to track the timeout
        of a single operations or multiple consecutive operations.
    """
    def __init__(self, timeout: float, interval: float=0, delay: float=0, doevery: int=-1, what_for: Optional[str]=None):
        self._timeout = timeout
        self._interval = interval
        self._delay = delay
        self._doevery = doevery
        self._what_for = what_for

        self._loop_counter = 0
        self._now_time = None
        self._start_time = None
        self._end_time = None
        self._final_attempt = False
        self._wait_state = TimeoutState.NotStarted
        return

    @property
    def completed(self) -> bool:
        """
            Indicates the wait was successfully completed.
        """
        return self._wait_state == TimeoutState.Completed

    @property
    def end_time(self) -> datetime:
        """
            Property to retreive the current endtime
        """
        return self._end_time

    @property
    def delay(self) -> float:
        """
            Property for retreiving the delay value.
        """
        return self._delay

    @property
    def final_attempt(self) -> bool:
        """
            Property for retreiving the final_attempt marker and for monitoring and debugging
            calls to look at the final attempt marker.
        """
        return self._final_attempt

    @property
    def has_timed_out(self) -> bool:
        """
            Property indicating if the wait context reached its timeout while running.
        """
        htoval = self._wait_state != TimeoutState.Completed and self._now_time > self._end_time
        return htoval

    @property
    def interval(self) -> float:
        """
            Property for retreiving the interval value.
        """
        return self._interval

    @property
    def is_do_every_interval(self):
        dei = False
        if self._doevery > -1:
            dei = self._loop_counter % self._doevery == 0
        return dei

    @property
    def timeout(self) -> float:
        """
            Property for retreiving the timeout value.
        """
        return self._timeout

    @property
    def wait_state(self) -> TimeoutState:
        """
            Property to return the current wait state of the wait context.
        """
        return self._wait_state

    @property
    def what_for(self) -> str:
        """
            Property for retreiving the what_for value.
        """
        return self._what_for

    def continue_waiting(self):
        """
            Reset the wait context to a waiting state so we can continue waiting.
        """
        self._wait_state = TimeoutState.Running
        return

    def create_timeout(self, what_for: Optional[str]=None, detail: Optional[List[str]]=None, mark_timeout: Optional[bool]=True) -> AKitTimeoutError:
        """
            Helper method used to create detail :class:`AKitTimeoutError` exceptions
            that can be raised in the context of the looper method. 
        """
        if what_for is None:
            what_for = self._what_for

        err_msg = self.format_timeout_message(what_for, detail=detail)
        err_inst = AKitTimeoutError(err_msg)

        if mark_timeout:
            self.mark_timeout()

        return err_inst

    def extend_timeout(self, seconds: float):
        """
            Extend the timeout of the current wait context by the specified number of seconds.

            :param seconds: The time in seconds to extend the wait period.
        """
        self._end_time = self._end_time + timedelta(seconds=seconds)
        self._wait_state = TimeoutState.Running
        self._final_attempt = False
        return

    def format_timeout_message(self, what_for: str, detail: Optional[List[str]]=None) -> str:
        """
            Helper method used to create format a detailed error message for reporting a timeout condition.
        """
        diff_time = self._now_time - self._start_time
        err_msg_lines = [
            "Timeout waiting for {}:".format(what_for),
            MSG_TEMPL_TIME_COMPONENTS.format(self._timeout, self._start_time, self._end_time, self._now_time, diff_time),
        ]

        if detail is not None:
            err_msg_lines.extend(detail)

        err_msg = os.linesep.join(err_msg_lines)
        return err_msg

    def mark_begin(self):
        """
            Mark the wait context as running.
        """
        self._now_time = datetime.now()
        self._start_time = self._now_time
        self._end_time = self._start_time + timedelta(seconds=self._timeout)
        self._wait_state = TimeoutState.Running
        return

    def mark_complete(self):
        """
            Mark the wait context as complete.
        """
        self._wait_state = TimeoutState.Completed
        return

    def mark_final_attempt(self):
        """
            Mark the wait context as being in the final attempt condition.
        """
        self._final_attempt = True
        return

    def mark_time(self):
        """
            Called to mark the current time in the :class:`WaitContext` instance.
        """
        self._now_time = datetime.now()
        return

    def mark_timeout(self):
        """
            Called to mark the wait context as timed out.
        """
        self._wait_state = TimeoutState.TimedOut
        return

    def reduce_delay(self, secs):
        """
            Reduce the wait start delay.
        """
        if secs > self._delay:
            self._delay = 0
        else:
            self._delay = self._delay - secs
        return

    def should_continue(self) -> bool:
        """
            Indicates if a wait condition should continue based on time specifications and context.
        """
        self._now_time = datetime.now()
        self._loop_counter += 1

        scont = True

        if self._wait_state == TimeoutState.Completed:
            scont = False
        elif self._now_time > self._end_time:
            scont = False

        return scont
