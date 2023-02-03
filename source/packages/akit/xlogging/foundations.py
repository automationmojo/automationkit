"""
.. module:: foundations
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains framework logging functions which extend the functionality to
        the python :module:`logging` module.

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


import fnmatch
import logging
import os
import sys
import time
import traceback


from akit.environment.context import Context
from akit.environment.variables import AKIT_VARIABLES


class AKitLogLevels:
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    SECTION = 100
    RENDER = 200
    QUIET = 1000


logging.addLevelName(AKitLogLevels.SECTION, "SECTION")
logging.addLevelName(AKitLogLevels.RENDER, "RENDER")
logging.addLevelName(AKitLogLevels.QUIET, "QUIET")


# Start Logging to Standard Out.  We need to make sure it is initialized to something as early as possible,
# but we may not have a file to write to yet until logging_initialize is called by a proper entry point
logging.basicConfig(level=logging.NOTSET)


DEFAULT_LOGGER_NAME = "AKIT"

LOGGING_SECTION_MARKER = "="
LOGGING_SECTION_MARKER_LENGTH = 80

DEFAULT_LOGFILE_FORMAT = '[%(asctime)s][%(name)s][%(levelname)s][%(message)s]'


def format_log_section_header(title):
    """
        Formats a log section header by centering the title inside of the section marker character string.
    """
    title_upper = " %s " % title.strip().upper()
    marker_count = LOGGING_SECTION_MARKER_LENGTH - len(title_upper)
    marker_half = marker_count >> 1
    marker_prefix = LOGGING_SECTION_MARKER * marker_half
    marker_suffix = LOGGING_SECTION_MARKER * (marker_count - marker_half)
    header = "\n%s%s%s\n" % (marker_prefix, title_upper, marker_suffix)
    return header


OTHER_LOGGER_FILTERS = []


class AKitLogFormatter(logging.Formatter):
    """
    Formatter instances are used to convert a LogRecord to text.

    Formatters need to know how a LogRecord is constructed. They are
    responsible for converting a LogRecord to (usually) a string which can
    be interpreted by either a human or an external system. The base Formatter
    allows a formatting string to be specified. If none is supplied, the
    style-dependent default value, "%(message)s", "{message}", or
    "${message}", is used.

    The Formatter can be initialized with a format string which makes use of
    knowledge of the LogRecord attributes - e.g. the default value mentioned
    above makes use of the fact that the user's message and arguments are pre-
    formatted into a LogRecord's message attribute. Currently, the useful
    attributes in a LogRecord are described by:

    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """

    converter = time.localtime

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        """
        Initialize the formatter with specified format strings.

        Initialize the formatter either with the specified format string, or a
        default as described above. Allow for specialized date formatting with
        the optional datefmt argument. If datefmt is omitted, you get an
        ISO8601-like (or RFC 3339-like) format.

        Use a style parameter of '%', '{' or '$' to specify that you want to
        use one of %-formatting, :meth:`str.format` (``{}``) formatting or
        :class:`string.Template` formatting in your format string.

        .. versionchanged:: 3.2
           Added the ``style`` parameter.
        """
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)
        return

    def formatException(self, ei):
        """
        Format and return the specified exception information as a string.

        This default implementation just uses
        traceback.print_exception()
        """
        s = super().formatException(ei)
        return s

    def formatStack(self, stack_info):
        """
        This method is provided as an extension point for specialized
        formatting of stack information.

        The input data is a string as returned from a call to
        :func:`traceback.print_stack`, but with the last trailing newline
        removed.

        The base implementation just returns the value passed in.
        """
        return stack_info

    def format(self, record):
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        """
        record.message = record.getMessage()

        if record.levelno < AKitLogLevels.SECTION:
            s = super().format(record)
        else:
            s = record.message

        return s


class LoggingManagerWrapper:
    """
        There is [under normal circumstances] just one Manager instance, which
        holds the hierarchy of loggers.
    """
    # pylint: disable=protected-access

    def __init__(self, manager):
        """
            Initialize the manager with the root node of the logger hierarchy.
        """
        self.manager = manager
        return

    @property
    def disable(self):
        """
            Git if logging is disabled.
        """
        return self.manager.disable

    @property
    def emittedNoHandlerWarning(self):
        """
            Get if the emittion of handler warnings is turned off.
        """
        return self.manager.emittedNoHandlerWarning

    @property
    def loggerClass(self):
        """
            Returns the logger Class.
        """
        return self.manager.loggerClass

    @property
    def loggerDict(self):
        """
            Returns a dictionary of the loggers.
        """
        return self.manager.loggerDict

    @property
    def logRecordFactory(self):
        """
            Returns the log record factory.
        """
        return self.manager.logRecordFactory

    @property
    def root(self):
        """
            Returns the root logger.
        """
        return self.manager.root

    def getLogger(self, name):
        """
            Get a logger with the specified name (channel name), creating it
            if it doesn't yet exist. This name is a dot-separated hierarchical
            name, such as "a", "a.b", "a.b.c" or similar.

            If a PlaceHolder existed for the specified name [i.e. the logger
            didn't exist but a child of it did], replace it with the created
            logger and fix up the parent/child references which pointed to the
            placeholder to now point to the logger.
        """
        rv = None

        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')

        logging._acquireLock()
        try:
            if name in self.loggerDict:
                rv = self.loggerDict[name]
                if isinstance(rv, logging.PlaceHolder):
                    ph = rv
                    rv = (self.loggerClass or logging._loggerClass)(name)
                    rv.manager = self
                    self.loggerDict[name] = rv
                    self._fixupChildren(ph, rv)
                    self._fixupParents(rv)
            else:
                rv = (self.loggerClass or logging._loggerClass)(name)
                rv.manager = self
                self.loggerDict[name] = rv
                self._fixupParents(rv)
        finally:
            logging._releaseLock()

        return rv

    def matchLoggers(self, pattern):
        """
            Finds all the loggers whose name match the associated pattern.
        """
        logger_dict = {}

        logging._acquireLock()
        try:
            for lname in self.manager.loggerDict.keys():
                if fnmatch.fnmatch(lname, pattern):
                    logger_dict[lname] = self.manager.loggerDict[lname]
        finally:
            logging._releaseLock()

        return logger_dict

    def setLoggerClass(self, klass):
        """
            Set the class to be used when instantiating a logger with this Manager.
        """
        self.manager.setLoggerClass(klass)
        return

    def setLogRecordFactory(self, factory):
        """
            Set the factory to be used when instantiating a log record with this
            Manager.
        """
        self.manager.setLogRecordFactory(factory)
        return

    def _fixupParents(self, alogger):
        """
            Ensure that there are either loggers or placeholders all the way
            from the specified logger to the root of the logger hierarchy.
        """
        self.manager._fixupParents(alogger)
        return

    def _fixupChildren(self, ph, alogger):
        """
            Ensure that children of the placeholder ph are connected to the
            specified logger.
        """
        self.manager._fixupChildren(ph, alogger)
        return

    def _clear_cache(self):
        """
            Clear the cache for all loggers in loggerDict
            Called when level changes are made
        """
        self.manager._clear_cache()
        return


class LoggingDefaults:
    """
        Makes all the default values associated with logging available.
    """
    DefaultFileLoggingHandler = logging.FileHandler



class AKitLoggerWrapper:
    """
        We utilize a log wrapper so we can re-initialize logging and switch out the logger
        without invalidating references to the logger that we have given out.
    """

    def __init__(self, logger):
        self._logger = logger
        return

    def critical(self, msg, *args, **kwargs):
        """
            Log 'msg % args' with severity 'CRITICAL'.

            To pass exception information, use the keyword argument exc_info with
            a true value, e.g.

            logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        self._logger.critical(msg, *args, **kwargs)
        return

    def debug(self, msg, *args, **kwargs):
        """
            Log 'msg % args' with severity 'DEBUG'.

            To pass exception information, use the keyword argument exc_info with
            a true value, e.g.

            logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        self._logger.debug(msg, *args, **kwargs)
        return

    def test_begin(self, testname, **test_args):
        """
        """
        info_msg_lines = [
            "TEST BEGIN - {}".format(testname),
            "    ARGS:"
        ]

        for arg_name, arg_value in test_args.items():

            arg_value_debug = None
            if hasattr(arg_value, "__debug_repr__"):
                arg_value_debug= arg_value.__debug_repr__()
            else:
                arg_value_debug = str(arg_value)

            info_msg_lines.append("    {} = {}".format(arg_name, arg_value_debug))

        info_msg = os.linesep.join(info_msg_lines)

        self._logger.info(info_msg)
        return

    def test_end(self, testname):
        self._logger.info("TEST END - {}".format(testname))
        return

    def error(self, msg, *args, **kwargs):
        """
            Log 'msg % args' with severity 'ERROR'.

            To pass exception information, use the keyword argument exc_info with
            a true value, e.g.

            logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        self._logger.error(msg, *args, **kwargs)
        return

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
            Convenience method for logging an ERROR with exception information.
        """
        self._logger.exception(msg, *args, exc_info=exc_info, **kwargs)
        return

    def fatal(self, msg, *args, **kwargs):
        """
            Log 'msg % args' with severity 'CRITICAL'.

            To pass exception information, use the keyword argument exc_info with
            a true value, e.g.

            logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        self._logger.critical(msg, *args, **kwargs)
        return

    def info(self, msg, *args, **kwargs):
        """
            Log 'msg % args' with severity 'INFO'.

            To pass exception information, use the keyword argument exc_info with
            a true value, e.g.

            logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        self._logger.info(msg, *args, **kwargs)
        return

    def render(self, line):
        """
            Logs a log section marker
        """
        self._logger.log(AKitLogLevels.RENDER, line)
        return

    def section(self, title):
        """
            Logs a log section marker
        """
        marker = format_log_section_header(title)
        self._logger.log(AKitLogLevels.SECTION, marker)
        return

    def warning(self, msg, *args, **kwargs):
        """
            Log 'msg % args' with severity 'WARNING'.

            To pass exception information, use the keyword argument exc_info with
            a true value, e.g.

            logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        self._logger.warning(msg, *args, **kwargs)
        return

    def warn(self, msg, *args, **kwargs):
        """
            Log 'msg % args' with severity 'WARNING'.

            To pass exception information, use the keyword argument exc_info with
            a true value, e.g.

            logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        self._logger.warning(msg, *args, **kwargs)
        return


class LessThanRecordFilter(logging.Filter):
    """
        Filters records with a log level < WARNING
    """

    def __init__(self, filter_at_level):
        super(LessThanRecordFilter, self).__init__("LessThanFilter")
        self._filter_at_level = filter_at_level
        return

    def filter(self, record): # pylint: disable=no-self-use
        """
            Performs the filtering of records.
        """
        process_rec = record.levelno < self._filter_at_level
        return process_rec


class OtherFilter(logging.Filter):
    """
        Filters records with a name that match a prefix expression and marks them as other.
    """
    def __init__(self, prefix):
        super(OtherFilter, self).__init__("OtherFilter")
        self.prefix = prefix
        return

    def filter(self, record):
        """
            Performs the filtering of records.
        """
        record.is_other = fnmatch.fnmatch(record.name, self.prefix)
        return record.is_other


class RelevantFilter(logging.Filter):
    """
        Allows records that are not marked as other.
    """
    def __init__(self):
        super(RelevantFilter, self).__init__("RelevantFilter")
        return

    def filter(self, record): # pylint: disable=no-self-use
        """
            Performs the filtering of records.
        """
        process_rec = True
        if hasattr(record, "is_other"):
            if record.is_other:
                process_rec = False
        return process_rec


logging_initialized = False


def logging_initialize():
    """
        Method used to configure the automation kit logging based on the environmental parameters
        specified and then reinitialize the logging.
    """
    global logging_initialized

    if not logging_initialized:
        logging_initialized = True

        ctx = Context()

        env = ctx.lookup("/environment")
        conf = ctx.lookup("/configuration")
        logging_conf = conf["logging"]

        consolelevel = AKIT_VARIABLES.AKIT_LOG_LEVEL_CONSOLE
        logfilelevel = AKIT_VARIABLES.AKIT_LOG_LEVEL_FILE

        logname_template = logging_conf["logname"]
        logname = env.fill_template(logname_template)

        output_directory = env["output_directory"]
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        log_branches = []
        if "branched" in logging_conf:
            log_branches = logging_conf["branched"]


        # Setup the log files
        _reinitialize_logging(consolelevel, logfilelevel, output_directory, logname, log_branches)

    return


def logging_create_branch_logger(logger_name, logfilename, log_level):
    """
        Method that allows for the creation of a separate logfile for specific loggers in order
        to reduce the noise in the main logfile.  A common use for this would be to redirect
        logging from specific modules such as 'paramiko' and 'httplib' to thier own log files.

        :param logger_name: The name of the logger to create a branch log for.
    """
    root_logger = logging.getLogger()

    if logger_name in root_logger.manager.loggerDict:
        target_logger = logging.getLogger(logger_name)

        # Setup the relevant log file which will get all the
        # log entries from loggers that satisified a relevant
        # logger name prefix match
        handler = logging.FileHandler(logfilename)
        handler.setLevel(log_level)
        for handler in target_logger.handlers:
            target_logger.removeHandler(handler)
        target_logger.addHandler(handler)

    return


def _reinitialize_logging(consolelevel, logfilelevel, output_dir, logfile_basename, log_branches):
    """
        Helper method to re-initialize the logging when the path to the output directory changes
        shortly after startup of the framework.  This method also handles the configuration of
        output levels, stdout and stderr file wrappers.
    """

    consolelevel_strerr = logging.WARNING

    console_filter = LessThanRecordFilter(logging.WARNING)
    console_filter_stderr = None

    if isinstance(consolelevel, str):
        consolelevel_upper = consolelevel.upper()
        if consolelevel_upper == "QUIET":
            consolelevel = AKitLogLevels.QUIET
            consolelevel_strerr = AKitLogLevels.QUIET
            console_filter = LessThanRecordFilter(AKitLogLevels.QUIET)
            console_filter_stderr = LessThanRecordFilter(AKitLogLevels.QUIET)

        elif hasattr(logging, consolelevel_upper):
            consolelevel = getattr(logging, consolelevel_upper)
        else:
            consolelevel = logging.INFO
    else:
        print("")
        print("NOTE: Console logging set to %r" % consolelevel)
        print("NOTE: outputdir=%s" % output_dir)
        print("")

        consolelevel = logging.WARNING

    basecomp, extcomp = os.path.splitext(logfile_basename)

    ctx = Context()
    env = ctx.lookup("/environment")

    debug_logfilename = os.path.join(output_dir, basecomp + ".DEBUG" + extcomp)
    other_logfilename = os.path.join(output_dir, basecomp + ".OTHER" + extcomp)

    env["logfile_debug"] = debug_logfilename
    env["logfile_other"] = other_logfilename

    rel_logfilename = os.path.join(output_dir, basecomp + extcomp)

    logging.Logger.manager = LoggingManagerWrapper(logging.Logger.manager)

    # Remove all the log handlers from the root logger
    root_logger = logging.getLogger()
    for lhandler in root_logger.handlers:
        root_logger.removeHandler(lhandler)

    # Set the root logger to NOTSET, so we don't impose an effective log
    # level on child loggers
    root_logger.setLevel(logging.NOTSET)

    # Setup the debug logfile
    base_handler = LoggingDefaults.DefaultFileLoggingHandler(debug_logfilename)
    base_handler.setFormatter(AKitLogFormatter(DEFAULT_LOGFILE_FORMAT))
    base_handler.setLevel(logging.NOTSET)
    root_logger.addHandler(base_handler)

    # Setup the other log handler and other filter, we
    # need to add the other log handler before adding
    # the relevant log handler
    other_handler = LoggingDefaults.DefaultFileLoggingHandler(other_logfilename)
    other_handler.setFormatter(AKitLogFormatter(DEFAULT_LOGFILE_FORMAT))
    other_handler.setLevel(logfilelevel)
    for other_expr in OTHER_LOGGER_FILTERS:
        other_handler.addFilter(OtherFilter(other_expr))
    root_logger.addHandler(other_handler)

    # Setup the relevant log file which will get all the
    # log entries from loggers that satisified a relevant
    # logger name prefix match
    rel_handler = LoggingDefaults.DefaultFileLoggingHandler(rel_logfilename)
    rel_handler.setFormatter(AKitLogFormatter(DEFAULT_LOGFILE_FORMAT))
    rel_handler.setLevel(logfilelevel)
    rel_handler.addFilter(RelevantFilter())
    root_logger.addHandler(rel_handler)

    # Setup the stdout logger with the correct console level and
    # filter the log entries from the stdout handler that are
    # greater than Info level
    stdout_logger = logging.StreamHandler(sys.stdout)
    stdout_logger.setLevel(consolelevel)
    stdout_logger.addFilter(console_filter)

    stderr_logger = logging.StreamHandler(sys.stderr)
    stderr_logger.setLevel(consolelevel_strerr)
    if console_filter_stderr is not None:
        stderr_logger.addFilter(console_filter_stderr)

    root_logger.addHandler(stdout_logger)
    root_logger.addHandler(stderr_logger)

    for binfo in log_branches:
        try:
            logger_name = binfo["name"]
            logfilename = binfo["logname"]
            log_level = binfo["loglevel"]

            logging_create_branch_logger(logger_name, logfilename, log_level)
        except Exception: # pylint: disable=broad-except
            errmsg = "Error configuration branch logger." + os.linesep
            errmsg = traceback.format_exc()
            root_logger.error(errmsg)

    akit_logger = getAutomatonKitLogger()
    akit_logger.section("Logging Initialized")

    return


akit_logger_table = {}


def getAutomatonKitLogger(logger_name: str=None) -> AKitLoggerWrapper:
    """
        Gets an automation kit logger by name. AutomationKit loggers are different
        in that they are a logger wrapper which means the characteristics of the loggers
        can be changed latter without corrupting any previous references handed out to
        any particular loggers.

        :param logger_name: The name of the logger to obtain. The default is the AutomationKit logger.
    """
    global akit_logger_table

    if logger_name is None:
        logger_name = DEFAULT_LOGGER_NAME

    logger = None

    if logger_name in akit_logger_table:
        logger = akit_logger_table[logger_name]
    else:
        logger = AKitLoggerWrapper(logging.getLogger(logger_name))

    return logger
