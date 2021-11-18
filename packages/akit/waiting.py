
from typing import Any, Dict, List, Optional

import os
import threading
import time

from datetime import date, datetime, timedelta

from typing import Protocol

from akit.exceptions import AKitTimeoutError
from akit.timeouts import (
    DEFAULT_WAIT_DELAY,
    DEFAULT_WAIT_INTERVAL,
    DEFAULT_WAIT_TIMEOUT
)

MSG_TEMPL_TIME_COMPONENTS = "    timeout={} start_time={}, end_time={} now_time={} time_diff={}"

class WaitContext:
    """
        The :class:`WaitContext` object is used to store the context used by the :function:`wait_for_it`
        helper function.  It provides a convenient way to ensure consistent detailed data capture for
        waitloops and thier associated detailed context and criteria.
    """
    def __init__(self, timeout, delay=0):
        self.timeout = timeout
        self.delay = delay
        self.now_time = datetime.now()
        self.start_time = self.now_time
        self.end_time = self.start_time + timedelta(seconds=timeout)
        self.final_attempt = False
        return

    def create_timeout(self, what_for, detail: Optional[List[str]]=None):
        """
            Helper method used to create detail :class:`AKitTimeoutError` exceptions
            that can be raised in the context of the looper method. 
        """
        err_msg = self.format_timeout_message(what_for, detail=detail)
        err_inst = AKitTimeoutError(err_msg)
        return err_inst

    def extend_timeout(self, seconds):
        self.end_time = self.end_time + timedelta(seconds=seconds)
        self.final_attempt = False
        return

    def format_timeout_message(self, what_for: str, detail: Optional[List[str]]=None):
        """
            Helper method used to create format a detailed error message for reporting a timeout condition.
        """
        diff_time = self.now_time - self.start_time
        err_msg_lines = [
            "Timeout waiting for {}:".format(what_for),
            MSG_TEMPL_TIME_COMPONENTS.format(self.timeout, self.start_time, self.end_time, self.now_time, diff_time),
        ]

        if detail is not None:
            err_msg_lines.extend(detail)

        err_msg = os.linesep.join(err_msg_lines)
        return err_msg

    def mark_time(self):
        """
            Called to mark the current time in the :class:`WaitContext` instance.
        """
        self.now_time = datetime.now()
        return

    def reduce_delay(self, secs):
        """
            Reduce the wait start delay.
        """
        if secs > self.delay:
            self.delay = 0
        else:
            self.delay = self.delay - secs
        return

    def should_continue(self):
        """
            Indicates if a wait condition should continue based on time specifications and context.
        """
        self.now_time = datetime.now()

        scont = True
        if self.now_time > self.end_time:
            scont = False

        return scont

class WaitCallback(Protocol):
    def __call__(self, wctx: WaitContext, *args, **kwargs) -> bool:
        """
            This specifies a callable object that can have variable arguments but
            that must have a final_attempt keywork arguement.  The expected behavior
            of the callback is to return false if the expected condition has not
            been meet.
        """



def wait_for_it(looper: WaitCallback, *args, what_for: Optional[str]=None, delay: float=DEFAULT_WAIT_DELAY,
                interval: float=DEFAULT_WAIT_INTERVAL, timeout: float=DEFAULT_WAIT_TIMEOUT,
                lkwargs: Dict[Any, Any]={}, wctx: Optional[WaitContext]=None):
    """
        Provides for convenient mechanism to wait for criteria to be met before proceeding.

        :param looper: A callback method that is repeatedly called while it returns `False` up-to
            the end of a timeout period, and that will return `True` if a waited on condition is
            met prior to a timeout condition being met.
        :param what_for: A breif description of what is being waited for.
        :param delay: An initial time delay to consume before beginning the waiting process
        :param interval: A period of time to delay between rechecks of the wait conditon
        :param timeout: The maximum period of time in seconds that should be waited before timing out.
        :param lkwargs: Additional keyword arguments to pass to the looper function

        :raises AKitTimeoutError: A timeout error with details around the wait condition.
    """

    if what_for is None:
        what_for = looper.__name__

    if wctx is None:
        wctx = WaitContext(timeout, delay=delay)

    if delay > 0:
        time.sleep(DEFAULT_WAIT_DELAY)

    condition_met = False

    while wctx.should_continue():
        condition_met = looper(wctx, *args, **lkwargs)
        if condition_met:
            break

        time.sleep(interval)
        now_time = datetime.now()

    if not condition_met:
        # Mark the time we are performing the final attempt
        wctx.mark_time()
        wctx.final_attempt = True
        condition_met = looper(wctx, *args, **lkwargs)

    if not condition_met:
        err_msg = wctx.format_timeout_message(what_for)
        raise AKitTimeoutError(err_msg) from None

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


