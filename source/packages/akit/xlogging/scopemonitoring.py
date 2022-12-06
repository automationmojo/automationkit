"""
.. module:: scopemonitor
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`ScopeMonitor` object which monitors thread entrapment
               withing a specified scope.

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

import os
import threading
import time
import uuid

from datetime import datetime, timedelta

from akit.timeouts import TimeoutContext

from akit.xcollections import insert_into_ordered_list_ascending
from akit.xformatting import split_and_indent_lines
from akit.xlogging.foundations import getAutomatonKitLogger

DEFAULT_MONITORED_SCOPE_NOTIFY_DELAY = timedelta(seconds=60)

logger = getAutomatonKitLogger()

class MonitoredScope:
    """
        The :class:`MonitoredScope` object is utilized in order to provide monitoring on threads
        that are entering sections of code that might have a tendency to block and cause disruptions
        in automation processes.  The monitored scope allows for the creation of scopes of code execution
        that can capture contextual information and hand it to a monitor thread that can then log an error
        message if the thread entering the monitored context does not return from the context with a
        specified period of time.

        This solves the problem of reducing log clutter by not having to log at the entry of problematic
        sections of code, but delay the logging until the thread has failed to exit in a timely manner and
        ensure the logging can happen by passing the work off to another thread that is running in a safer
        context.
    """

    ERROR_COMPARISON_TYPE_MESSAGE = "Comparison is only support between two 'ScopeMonitor' objects."

    def __init__(self, label, message, timeout_ctx: TimeoutContext, notify_delay: timedelta=DEFAULT_MONITORED_SCOPE_NOTIFY_DELAY):
        self._id = str(uuid.uuid4())
        self._label = label
        self._message = message
        self._timeout_ctx = timeout_ctx
        self._notify_delay = notify_delay

        self._diag_func = None
        self._diag_args = None
        self._diag_kwargs = None

        self._exited = False
        self._triggered = False
        return

    def __enter__(self):
        """
        """
        global global_scope_monitor

        if global_scope_monitor is None:
            global_scope_monitor = ScopeMonitor()

        self._timeout_ctx.mark_begin()

        global_scope_monitor.register_monitor(self)

        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        """
        """
        self._exited = True

        return False

    def __eq__(self, other: "ScopeMonitor"):
        """
            Perform comparison between ScopeMonitor(left) == ScopeMonitor(right)
        """
        if not isinstance(other, ScopeMonitor):
            raise ValueError(self.ERROR_COMPARISON_TYPE_MESSAGE)

        return self._timeout_ctx.end_time == other._timeout_ctx.end_time

    def __ge__(self, other: "ScopeMonitor"):
        """
            Perform comparison between ScopeMonitor(left) >= ScopeMonitor(right)
        """
        if not isinstance(other, ScopeMonitor):
            raise ValueError(self.ERROR_COMPARISON_TYPE_MESSAGE)

        return self._timeout_ctx.end_time >= other._timeout_ctx.end_time

    def __gt__(self, other: "ScopeMonitor"):
        """
            Perform comparison between ScopeMonitor(left) > ScopeMonitor(right)
        """
        if not isinstance(other, ScopeMonitor):
            raise ValueError(self.ERROR_COMPARISON_TYPE_MESSAGE)

        return self._timeout_ctx.end_time > other._timeout_ctx.end_time

    def __le__(self, other: "ScopeMonitor"):
        """
            Perform comparison between ScopeMonitor(left) <= ScopeMonitor(right)
        """
        if not isinstance(other, ScopeMonitor):
            raise ValueError(self.ERROR_COMPARISON_TYPE_MESSAGE)

        return self._timeout_ctx.end_time <= other._timeout_ctx.end_time

    def __lt__(self, other: "ScopeMonitor"):
        """
            Perform comparison between ScopeMonitor(left) < ScopeMonitor(right)
        """
        if not isinstance(other, ScopeMonitor):
            raise ValueError(self.ERROR_COMPARISON_TYPE_MESSAGE)

        return self._timeout_ctx.end_time < other._timeout_ctx.end_time

    def __ne__(self, other: "ScopeMonitor"):
        """
            Perform comparison between ScopeMonitor(left) != ScopeMonitor(right)
        """
        if not isinstance(other, ScopeMonitor):
            raise ValueError(self.ERROR_COMPARISON_TYPE_MESSAGE)

        return self._timeout_ctx.end_time != other._timeout_ctx.end_time

    @property
    def exited(self):
        """
            Return true if the thread that entered the MonitoredScope has exited.
        """
        return self._exited

    @property
    def expired(self):
        """
            Returns true if the MonitoredScope instance has not been exited by the calling
            thread before it has expired.
        """
        is_expired = False
        now = datetime.now()
        if now > (self._timeout_ctx.end_time + self._notify_delay):
            is_expired = True
        return is_expired

    @property
    def id(self):
        """
            The unique identifier for this MonitoredScope instance.
        """
        return self._id

    @property
    def label(self):
        """
            The human readable label has been assigned to identify this scope.
        """
        return self._label

    @property
    def message(self):
        """
            The message that will be logged if this MonitoredScope is not exited before
            the timemout has expired.
        """
        return self._message

    def set_diagnostic(self, diagnostic_function, *args, **kwargs):
        """
            Sets the diagnostic function and its associated args which will be run if
            the :class:`MonitoredScope` is not exited before it has expired.
        """
        self._diag_func = diagnostic_function
        self._diag_args = args
        self._diag_kwargs = kwargs
        return

    def trigger_notification(self):
        """
            On the first trigger of a notification.  Runs the diagnostic function, logs the label and
            message along with the information collected by the diagnostic function.
        """
        if not self._triggered:
            self._triggered = True
            if self.expired:

                errlines = [
                    "MonitoredScope({}): Timeout waiting for thread to exit monitored scope.".format(self._label),
                    "MESSAGE: {}".format(self._message),

                ]

                if  self._diag_func:
                    errlines.append("DIAGNOSTIC:")

                    diagmsg = self._diag_func(*self._diag_args, **self._diag_kwargs)
                    errlines.extend(split_and_indent_lines(diagmsg, 1))

                errmsg = os.linesep.join(errlines)
                logger.error(errmsg)

        return

class ScopeMonitor:
    """
        The :class:`ScopeMonitor` object is utilized to provide monitoring of threads that are entering
        sections of code that might have a tendency to block and cause disruptions in automation processes.

        The :class:`ScopeMonitor` takes pre-dictive work packets for logging from threads entering critical
        sections of code monitored by :class:`MonitoredScope` instances used in a 'with' statement.

        ..code-block:: python

            with MonitoredScope("RunCommand", "Running command on cluster node (%s)" % nodeip) as mscope:
                cluster.run_cmd(1, "echo blah")

        The use of a :class:`MonitoredScope` remove the necessity to log prior to entering a critical
        section of code but allows log entrys to be pre-emptively handed off to the :class:`ScopeMonitor`
        thread for contingent processing should a the thread fail to return from the critical section of
        code in a timely manner.
    """

    SCOPE_MONITOR_INTERVAL = 5

    instance = None
    initialized = False

    def __new__(cls, *_args, **_kwargs):
        """
            Constructs new instances of the :class:`ScopeMonitor` object. The
            :class:`ScopeMonitor` object is a singleton so following instantiations
            of the object will reference the existing singleton
        """

        if cls.instance is None:
            cls.instance = super(ScopeMonitor, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        thisType = type(self)
        if not thisType.initialized:
            thisType.initialized = True

            self._monitors = []
            self._monitors_lock = threading.RLock()

            self._timer = threading.Timer(self.SCOPE_MONITOR_INTERVAL, self._monitor_tick)
        return

    def register_monitor(self, monitor: MonitoredScope):
        """
            Register a monitor context with the :class:`ScopeMonitor` singleton.

            :param monitor: The monitor context to add to the the list of monitored scopes.
        """

        self._monitors_lock.acquire()
        try:
            insert_into_ordered_list_ascending(self._monitors, monitor)
        finally:
            self._monitors_lock.release()

        return

    def _monitor_tick(self):

        self._monitors_lock.acquire()
        try:
            if len(self._monitors) > 0:
                while True:
                    firstMonitor = self._monitors[0]
                    if firstMonitor.expired:
                        firstMonitor.trigger_notification()
                        del self._monitors[0]
                    else:
                        break
        finally:
            self._monitors_lock.release()

        return


global_scope_monitor = None
