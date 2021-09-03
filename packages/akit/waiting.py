
from typing import Any, Dict, List

import os
import time

from typing_extensions import Protocol

from akit.exceptions import AKitTimeoutError
from akit.timeouts import (
    DEFAULT_WAIT_DELAY,
    DEFAULT_WAIT_INTERVAL,
    DEFAULT_WAIT_TIMEOUT
)

MSG_TEMPL_TIME_COMPONENTS = "    start_time={}, end_time={} now_time={} time_diff={}"

class WaitCallback(Protocol):
    def __call__(self, *args, wfi_final_attempt: bool, **kwargs) -> bool:
        """
            This specifies a callable object that can have variable arguments but
            that must have a wfi_final_attempt keywork arguement.  The expected behavior
            of the callback is to return false if the expected condition has not
            been meet.
        """

def wait_for_it(looper: WaitCallback, *, message: str, delay: float=DEFAULT_WAIT_DELAY,
                interval: float=DEFAULT_WAIT_INTERVAL, timeout: float=DEFAULT_WAIT_TIMEOUT,
                looper_args: List[Any], looper_kwargs: Dict[Any, Any]):

    if delay > 0:
        time.sleep(DEFAULT_WAIT_DELAY)

    condition_met = False

    start_time = time.time()
    now_time = start_time
    end_time = start_time + timeout
    while now_time < end_time:
        chk_res = looper(*looper_args, wfi_final_attempt=False, **looper_kwargs)
        if chk_res:
            condition_met = True
            break

        time.sleep(interval)
        now_time = time.time()

    if not condition_met:
        chk_res = looper(*looper_args, wfi_final_attempt=True, **looper_kwargs)
        if chk_res:
            condition_met = True

    if not condition_met:
        diff_time = now_time - start_time
        err_msg_lines = [
            "Timeout waiting for the following expected condition:",
            MSG_TEMPL_TIME_COMPONENTS.format(start_time, end_time, now_time, diff_time),
            "CONDITION: {}".format(message)
        ]
        err_msg = os.linesep.join(err_msg_lines)
        raise AKitTimeoutError(err_msg)

    return
