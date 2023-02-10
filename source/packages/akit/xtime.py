"""
.. module:: xtime
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains framework time related functions which extend the functionality to
               the python :module:`time` and  :module:`datetime` modules.

.. note:: The modules that are named `xsomething` like this module are prefixed with an `x` character to
          indicate they extend the functionality of a base python module and the `x` is pre-pended to
          prevent module name collisions with python modules.

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

import time

from datetime import datetime

FORMAT_DATETIME = "%Y-%m-%dT%H%M!%S"

def current_time_millis() -> float:
    """
        Current system time in milliseconds

        :returns: Time in milliseconds
    """
    now_ms = time.time() * 1000
    return now_ms

def format_time_with_fractional(tsecs: float) -> str:
    """
        Format the time in seconds as a fractional in seconds.

        :param tsecs: Time in seconds as a float.

        :returns: Formatted time in (seconds).(fractions of seconds)
    """
    sec_comp = int(tsecs)
    frac_comp = (tsecs - sec_comp) * 1000
    dtstr = "%s.%06d" % (time.strftime(FORMAT_DATETIME, time.gmtime(sec_comp)), frac_comp)
    return dtstr

def parse_datetime(dtstr: str, datetime_format: str=FORMAT_DATETIME) -> datetime:
    """
        Parses a date time from string and includes the microseconds component.

        :param dtstr: The date in the form of a date time string.
        :param datetime_format: The format string to when parsing the datetime string.

        :returns: The datetime from the parsed string.
    """
    microsecs = 0

    if dtstr.find(".") > 0:
        dtstr, msecstr = dtstr.split(".")
        microsecs = int(msecstr)

    dtobj = datetime(*time.strptime(dtstr, datetime_format)[:6], microsecs)

    return dtobj
