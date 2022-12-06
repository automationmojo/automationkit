"""
.. module:: waiting
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

from typing import Any, Callable, Dict, List, Optional, Protocol

import os
import threading
import time

from datetime import datetime, timedelta

from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Column

from akit.comparisons import compare_any_of_same_type

from akit.timeouts import (
    TimeoutContext,
    TimeoutState,
    DEFAULT_WAIT_DELAY,
    DEFAULT_WAIT_INTERVAL,
    DEFAULT_WAIT_TIMEOUT,
    DEFAULT_WHATFOR_TEMPLATE
)

class WaitContext(TimeoutContext):
    """
        Place holder for differences that might arise between the base TimeoutContext and
        the WaitContext used for wait loops.
    """

class WaitCallback(Protocol):
    def __call__(self, wctx: TimeoutContext, *args, **kwargs) -> bool:
        """
            This specifies a callable object that can have variable arguments but
            that must have a final_attempt keywork arguement.  The expected behavior
            of the callback is to return false if the expected condition has not
            been meet.
        """


def wait_for_it(looper: WaitCallback, *largs, what_for: Optional[str]=None, delay: float=DEFAULT_WAIT_DELAY,
                interval: float=DEFAULT_WAIT_INTERVAL, timeout: float=DEFAULT_WAIT_TIMEOUT,
                lkwargs: Dict[Any, Any]={}, wctx: Optional[WaitContext]=None):
    """
        Provides for convenient mechanism to wait for criteria to be met before proceeding.

        :param looper: A callback method that is repeatedly called while it returns `False` up-to
            the end of a timeout period, and that will return `True` if a waited on condition is
            met prior to a timeout condition being met.
        :param largs: Arguements to pass to the looper callback function.
        :param what_for: A breif description of what is being waited for.
        :param delay: An initial time delay to consume before beginning the waiting process.
        :param interval: A period of time to delay between rechecks of the wait conditon
        :param timeout: The maximum period of time in seconds that should be waited before timing out.
        :param lkwargs: Additional keyword arguments to pass to the looper function

        :raises AKitTimeoutError: A timeout error with details around the wait condition.

        ..note: The 'delay', 'interval' and 'timeout' parameters will be ignored if the 'wctx' parameter
                is passed as the wctx (WaitContext) parameter includes these values with it.
    """

    if what_for is None:
        what_for = DEFAULT_WHATFOR_TEMPLATE.format(looper.__name__)

    if wctx is None:
        wctx = WaitContext(timeout, interval=interval, delay=delay, what_for=what_for)

    if wctx.delay > 0:
        time.sleep(DEFAULT_WAIT_DELAY)

    wctx.mark_begin()

    condition_met = False

    while True:
        condition_met = looper(wctx, *largs, **lkwargs)
        if condition_met:
            wctx.mark_complete()
            break

        if not wctx.should_continue():
            break

        if wctx.interval > 0:
            time.sleep(wctx.interval)

    if not condition_met:
        # Mark the time we are performing the final attempt
        wctx.mark_time()
        wctx.mark_final_attempt()
        condition_met = looper(wctx, *largs, **lkwargs)

    if not condition_met:
        toerr = wctx.create_timeout(what_for)
        raise toerr

    wctx.mark_complete()

    return


class WaitGate:

    def __init__(self, gate: threading.Event, message: Optional[str]=None, timeout: Optional[float]=None,
                 timeout_args: Optional[list]=None):
        self._gate = gate
        self._messaage = message
        self._timeout = timeout
        self._timeout_args = timeout_args
        return

    @property
    def gate(self) -> threading.Event:
        return self._gate

    @property
    def message(self) -> str:
        return self._message

    @property
    def timeout(self) -> float:
        return self._timeout

    @property
    def timeout_args(self) -> list:
        return self._timeout_args

    def clear(self):
        self._gate.clear()
        return

    def is_set(self) -> bool:
        rtnval = self._gate.is_set()
        return rtnval

    def set(self):
        self._gate.set()
        return

    def wait(self, timeout: Optional[float]=None, raise_timeout=False):

        if timeout is None:
            timeout = self._timeout

        rtnval = self._gate.wait(timeout=self._timeout)
        if not rtnval:
            errmsg = ""
            raise TimeoutError(errmsg)

        return rtnval

class WaitingScope:
    def __init__(self, gates: List[WaitGate],):
        self._gates = gates
        return

    def __enter__(self):
        for gate in self._gates:
            gate.clear()
        return
    
    def __exit__(self, ex_type, ex_inst, ex_tb):
        return
    
    def wait(self):

        for gate in self.gates:
            gate.wait()

        return

class MultiEvent:

    def __init__(self, contexts: List[object]):
        self._contexts = contexts
        return


class ProgressOfDurationWaitContext(WaitContext):


    def __init__(self, progress: Progress, task_name: str, timeout: float, delay: float=0, what_for: Optional[str]=None):
        WaitContext.__init__(self, timeout, delay=delay, what_for=what_for)
        self._progress = progress
        self._time_delta_secs = None

        self._task_name = task_name
        self._task_id = None
        return

    def mark_begin(self):
        """
            Mark the wait context as running.
        """

        self._now_time = datetime.now()
        self._start_time = self._now_time
        self._end_time = self._start_time + timedelta(seconds=self._timeout)

        self._time_delta_secs = (self._end_time - self._start_time).total_seconds()
        self._task_id = self._progress.add_task(self._task_name, total=self._time_delta_secs)
        self._progress.update(self._task_id, completed=0)

        self._wait_state = TimeoutState.Running
        return

    def mark_complete(self):
        """
            Mark the wait context as complete.
        """
        self._wait_state = TimeoutState.Completed
        self.render_complete()
        return

    def mark_timeout(self):
        """
            Called to mark the wait context as timed out.
        """
        self._wait_state = TimeoutState.TimedOut
        self.render_timeout()
        return

    def render_complete(self):
        if self._task_id is not None:
            self._progress.update(self._task_id, completed=self._time_delta_secs)
        return

    def render_progress(self):
        current_secs = (self._now_time - self._start_time).total_seconds()

        if self._task_id is not None:
            self._progress.update(self._task_id, completed=current_secs)

        return

    def render_timeout(self):
        self._progress.update(self._task_id, completed=self._time_delta_secs)
        return

    def should_continue(self) -> bool:
        """
            Indicates if a wait condition should continue based on time specifications and context.
        """
        self._now_time = datetime.now()

        scont = True

        if self._wait_state == TimeoutState.Completed:
            scont = False
        elif self._now_time > self._end_time:
            scont = False

        self.render_progress()

        return scont

    def create_rich_progress() -> Progress:
        desc_column = TextColumn("{task.description}", table_column=Column(ratio=1))
        bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
        time_remaining = TimeRemainingColumn()
        progress = Progress(desc_column, bar_column, "[progress.percentage]{task.percentage:>3.0f}%", time_remaining, expand=True)
        return progress

def wait_for_result_from_call(wctx: WaitContext, callable: Callable, expected: Any, *args, **kwargs):
    """
        Wait for the 'callable' provided to return the expeted result.
    """

    found = callable(*args, **kwargs)

    comp_result = compare_any_of_same_type(expected, found)
    if not comp_result and wctx.final_attempt:
        callable_name = callable.__name__
        whatfor = "for {} to return the expected result {}.  last={}".format(callable_name, expected, found)
        toerr = wctx.create_timeout(whatfor)
        raise toerr

    return comp_result
