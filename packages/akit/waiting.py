
from typing import Any, Dict, List

import os
import time

from datetime import datetime, timedelta

from typing import Protocol

from akit.exceptions import AKitTimeoutError
from akit.timeouts import (
    DEFAULT_WAIT_DELAY,
    DEFAULT_WAIT_INTERVAL,
    DEFAULT_WAIT_TIMEOUT
)

MSG_TEMPL_TIME_COMPONENTS = "    timeout={} start_time={}, end_time={} now_time={} time_diff={}"

class WaitCallback(Protocol):
    def __call__(self, start: datetime, end: datetime, now:datetime, final_attempt: bool, *args, **kwargs) -> bool:
        """
            This specifies a callable object that can have variable arguments but
            that must have a final_attempt keywork arguement.  The expected behavior
            of the callback is to return false if the expected condition has not
            been meet.
        """

def wait_for_it(looper: WaitCallback, *, message: str, delay: float=DEFAULT_WAIT_DELAY,
                interval: float=DEFAULT_WAIT_INTERVAL, timeout: float=DEFAULT_WAIT_TIMEOUT,
                looper_args: List[Any], looper_kwargs: Dict[Any, Any]):

    if delay > 0:
        time.sleep(DEFAULT_WAIT_DELAY)

    condition_met = False

    start_time = datetime.now()
    now_time = start_time
    end_time = start_time + timedelta(seconds=timeout)
    while now_time < end_time:
        chk_res = looper(start_time, end_time, now_time, False, *looper_args, **looper_kwargs)
        if chk_res:
            condition_met = True
            break

        time.sleep(interval)
        now_time = datetime.now()

    if not condition_met:
        now_time = datetime.now()
        chk_res = looper(start_time, end_time, now_time, True, *looper_args, **looper_kwargs)
        if chk_res:
            condition_met = True

    if not condition_met:
        diff_time = now_time - start_time
        err_msg_lines = [
            "Timeout waiting for the following expected condition:",
            MSG_TEMPL_TIME_COMPONENTS.format(timeout, start_time, end_time, now_time, diff_time),
            "CONDITION: {}".format(message)
        ]
        err_msg = os.linesep.join(err_msg_lines)
        raise AKitTimeoutError(err_msg)

    return
