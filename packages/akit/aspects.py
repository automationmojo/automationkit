"""
.. module:: aspects
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`Aspects` class and the constants used to provide aspect behaviors.

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

from typing import List, Optional, Union

from enum import IntEnum

from logging import Logger

from akit.timeouts import TimeoutContext
from akit.xlogging.foundations import getAutomatonKitLogger

class ActionPattern(IntEnum):
    """
        A action pattern to use when using apspects to change the behavior of an API.
    """
    SINGLE_CALL = 0
    SINGLE_CONNECTED_CALL = 1
    DO_UNTIL_SUCCESS = 2
    DO_WHILE_SUCCESS = 3
    DO_UNTIL_CONNECTION_FAILURE = 4

class LoggingPattern:
    """
        A logging pattern to use when logging commands.
    """
    ALL_RESULTS = 0
    FAILURE_ONLY = 1
    SUCCESS_ONLY = 2


DEFAULT_COMPLETION_TIMEOUT = 600
DEFAULT_COMPLETION_INTERVAL = 10

DEFAULT_INACTIVITY_TIMEOUT = 600
DEFAULT_INACTIVITY_INTERVAL = .5

DEFAULT_MONITOR_DELAY = 30

DEFAULT_RETRY_LOGGING_INTERVAL = 5

DEFAULT_LOGGING_PATTERN = LoggingPattern.ALL_RESULTS

DEFAULT_MUST_CONNECT = False

DEFAULT_ALLOWED_ERROR_CODES: List[int] = []

class Aspects:
    """
        Aspects are utilized with the interop APIs and agents such as the :class:`SSHAgent` class in order
        to modify the behavior of APIs with respect to retry parameter such as timeout, interval, looping patterns
        logging, etc.  The aspects object provides a way to package this common criteria into a single parameter
        or constant you can  pass to multiple APIs
    """

    def __init__(self, action_pattern: ActionPattern = ActionPattern.SINGLE_CALL,
                       completion_timeout: float = DEFAULT_COMPLETION_TIMEOUT,
                       completion_interval: float = DEFAULT_COMPLETION_INTERVAL,
                       inactivity_timeout: float = DEFAULT_INACTIVITY_TIMEOUT,
                       inactivity_interval: float = DEFAULT_INACTIVITY_INTERVAL,
                       monitor_delay: float = DEFAULT_MONITOR_DELAY,
                       logging_pattern: LoggingPattern = DEFAULT_LOGGING_PATTERN,
                       retry_logging_interval: int = DEFAULT_RETRY_LOGGING_INTERVAL,
                       allowed_error_codes: List[int] = DEFAULT_ALLOWED_ERROR_CODES,
                       must_connect: bool = DEFAULT_MUST_CONNECT,
                       logger: Optional[Logger]=None):
        """
            Creates an :class:`Aspects` instance package.

            :param action_pattern: The :class:`ActionPattern` that the API should exhibit such as
                                   SINGULAR, DO_UNTIL_SUCCESS, DO_WHILE_SUCCESS
            :param completion_timeout: The time in seconds as a float that is the max time before
                                       timeout for the activity to complete.
            :param completion_interval: The time in seconds as a float that is waited before reattempting
                                        an activity.
            :param inactivity_timeout: The time in seconds as a float that is the max time before timeout
                                       that is waited before a :class:`TimeoutError` is raised due to inactivity.
            :param inactivity_interval: The time in seconds as a float that is waited before reattempting an activity.
            :param retry_logging_interval: The logging interval for retry loops.
            :param allowed_error_codes: A list of error codes that allow retry
            :param must_connect: Used to indicate that connection failures should be raised.
        """
        self.action_pattern = action_pattern
        self.completion_timeout = completion_timeout
        self.completion_interval = completion_interval
        self.inactivity_timeout = inactivity_timeout
        self.inactivity_interval = inactivity_interval
        self.monitor_delay = monitor_delay
        self.logging_pattern = logging_pattern
        self.retry_logging_interval = retry_logging_interval
        self.allowed_error_codes = allowed_error_codes
        self.must_connect=must_connect

        if logger is None:
            self.logger = getAutomatonKitLogger()
        else:
            self.logger = logger

        return

class AspectsCmd(Aspects):
    """
    """
    def __init__(self, expected_status: Union[int, List[int]]=0,
                       user: Optional[str]=None,
                       pty_params: Optional[dict]=None,
                       action_pattern: ActionPattern = ActionPattern.SINGLE_CALL,
                       completion_timeout: float = DEFAULT_COMPLETION_TIMEOUT,
                       completion_interval: float = DEFAULT_COMPLETION_INTERVAL,
                       inactivity_timeout: float = DEFAULT_INACTIVITY_TIMEOUT,
                       inactivity_interval: float = DEFAULT_INACTIVITY_INTERVAL,
                       monitor_delay: float = DEFAULT_MONITOR_DELAY,
                       logging_pattern: LoggingPattern = DEFAULT_LOGGING_PATTERN,
                       retry_logging_interval: int = DEFAULT_RETRY_LOGGING_INTERVAL,
                       allowed_error_codes: List[int] = DEFAULT_ALLOWED_ERROR_CODES,
                       logger: Optional[Logger]=None):
        
        Aspects.__init__(self, action_pattern=action_pattern, completion_timeout=completion_timeout,
                            completion_interval=completion_interval, inactivity_timeout=inactivity_timeout,
                            inactivity_interval=inactivity_interval, monitor_delay=monitor_delay,
                            logging_pattern=logging_pattern, retry_logging_interval=retry_logging_interval,
                            allowed_error_codes=allowed_error_codes, logger=logger)
        
        self.expected_status = expected_status
        self.user = user
        self.pty_params = pty_params
        return

class AspectsUPnP(Aspects):
    """
    """
    def __init__(self, action_pattern: ActionPattern = ActionPattern.SINGLE_CONNECTED_CALL,
                       completion_timeout: float = DEFAULT_COMPLETION_TIMEOUT,
                       completion_interval: float = DEFAULT_COMPLETION_INTERVAL,
                       inactivity_timeout: float = DEFAULT_INACTIVITY_TIMEOUT,
                       inactivity_interval: float = DEFAULT_INACTIVITY_INTERVAL,
                       monitor_delay: float = DEFAULT_MONITOR_DELAY,
                       logging_pattern: LoggingPattern = DEFAULT_LOGGING_PATTERN,
                       retry_logging_interval: int = DEFAULT_RETRY_LOGGING_INTERVAL,
                       allowed_error_codes: List[int] = DEFAULT_ALLOWED_ERROR_CODES,
                       must_connect: bool = DEFAULT_MUST_CONNECT,
                       logger: Optional[Logger]=None):
        
        Aspects.__init__(self, action_pattern=action_pattern, completion_timeout=completion_timeout,
                            completion_interval=completion_interval, inactivity_timeout=inactivity_timeout,
                            inactivity_interval=inactivity_interval, monitor_delay=monitor_delay,
                            logging_pattern=logging_pattern, retry_logging_interval=retry_logging_interval,
                            allowed_error_codes=allowed_error_codes, must_connect=must_connect, logger=logger)
        return


DEFAULT_ASPECTS = Aspects()
DEFAULT_CMD_ASPECTS = AspectsCmd()
DEFAULT_UPNP_ASPECTS = AspectsUPnP()
