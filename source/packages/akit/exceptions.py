"""
.. module:: exceptions
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the exceptions that are raised by the code in the Automation Kit

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

import inspect
from lib2to3.pytree import Base
import os
import traceback
from typing import Type

from akit.xinspect import get_caller_function_name
from akit.xformatting import split_and_indent_lines


MEMBER_TRACE_POLICY = "__traceback_format_policy__"


class TracebackFormatPolicy:
    Brief = "Brief"
    Full = "Full"
    Hide = "Hide"


VALID_MEMBER_TRACE_POLICY = ["Brief", "Full", "Hide"]


__traceback_format_policy__ = TracebackFormatPolicy.Hide


class TRACEBACK_CONFIG:
    TRACEBACK_POLICY_OVERRIDE = None


def akit_assert(eresult, errmsg, from_exception=None):
    if not eresult:
        raise AKitAssertionError(errmsg) from from_exception


def collect_stack_frames(ex_inst, max_full_display=1):

    global TRACEBACK_POLICY_OVERRIDE

    last_items = None
    tb_code = None
    tb_lineno = None

    tb_frames = []
    for tb_frame, tb_lineno in traceback.walk_tb(ex_inst.__traceback__):
        tb_frames.append((tb_frame, tb_lineno))
    tb_frames.reverse()

    traceback_list = []

    for tb_frame, tb_lineno in tb_frames:
        tb_code = tb_frame.f_code
        co_filename = tb_code.co_filename
        co_name = tb_code.co_name
        co_arg_names = tb_code.co_varnames[:tb_code.co_argcount]
        co_argcount = tb_code.co_argcount
        co_locals = tb_frame.f_locals

        co_format_policy = TracebackFormatPolicy.Full

        if TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE is None:
            co_module = inspect.getmodule(tb_code)
            if co_module and hasattr(co_module, MEMBER_TRACE_POLICY):
                cand_format_policy = getattr(co_module, MEMBER_TRACE_POLICY)
                if cand_format_policy in VALID_MEMBER_TRACE_POLICY:
                    co_format_policy = cand_format_policy
        else:
            co_format_policy = TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE

        items = [co_filename, tb_lineno, co_name, "", None]
        if last_items is not None:
            code_args = []
            for argidx in range(0, co_argcount):
                argname = co_arg_names[argidx]
                argval = co_locals[argname]
                code_args.append("%s=%r" % (argname, argval))

            last_items[-2] = "%s(%s)" % (co_name, ", ".join(code_args)) # pylint: disable=unsupported-assignment-operation

        last_items = items

        traceback_list.append(items)
        last_items = items

        if max_full_display > 0 and co_format_policy == TracebackFormatPolicy.Full \
            and os.path.exists(co_filename) and co_filename.endswith(".py"):
            context_lines, context_startline = inspect.getsourcelines(tb_code)
            context_lines = [cline.rstrip() for cline in context_lines]
            clindex = (tb_lineno - context_startline)
            last_items[-2] = context_lines[clindex].strip()
            last_items[-1] = context_lines
            max_full_display -= 1

    return traceback_list


def format_exception(ex_inst, max_full_display=1):
    exc_lines = []

    etypename = type(ex_inst).__name__
    eargs = ex_inst.args

    exmsg_lines = [
        "%s: %s" % (etypename, repr(eargs).rstrip(",")),
        "TRACEBACK (most recent call last):"
    ]

    stack_frames = collect_stack_frames(ex_inst, max_full_display=max_full_display)
    stack_frames_len = len(stack_frames)
    for co_filename, co_lineno, co_name, co_code, co_context in stack_frames:

        exmsg_lines.extend([
            '  File "%s", line %d, in %s' % (co_filename, co_lineno, co_name),
            "    %s" % co_code
        ])

        if hasattr(ex_inst, "context") and co_name in ex_inst.context:
            cxtinfo = ex_inst.context[co_name]
            exmsg_lines.append('    %s:' % cxtinfo["label"])
            exmsg_lines.extend(split_and_indent_lines(cxtinfo["content"], 2, indent=3))
        elif co_context is not None and len(co_context) > 0 and stack_frames_len > 1:
            exmsg_lines.append('    CONTEXT:')
            firstline = co_context[0]
            lstrip_len = len(firstline) - len(firstline.lstrip())
            co_context = [cline[lstrip_len:] for cline in co_context]
            co_context = ["      %s" % cline for cline in co_context]
            exmsg_lines.extend(co_context)
        exmsg_lines.append('')

    return exmsg_lines


class AKitErrorEnhancer:
    def __init__(self, *args, **kwargs):
        self._context = {}
        return

    @property
    def context(self):
        return self._context

    def add_context(self, content, label="CONTEXT"):
        """
            Adds context to an exception and associates it with the function context
            on the stack.
        """
        caller_name = get_caller_function_name()

        self._context[caller_name] = {
            "label": label,
            "content": content
        }

        return


class AKitBaseException(BaseException, AKitErrorEnhancer):
    """
        The base error object for Automation Kit errors that we don't want to be catchable as
        generic exceptions.  The :class:`AKitBaseException` object lets semantic errors and any
        other error that should not be caught bypass a generic exception hanlder.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return


class AKitError(Exception, AKitErrorEnhancer):
    """
        The base error object for Automation Kit errors.  The :class:`AKitError` serves as aa base
        type and also provides some additional functionality for adding context to errors and
        formatting exception output.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return


def add_exception_context(xcpt: BaseException, content, label="CONTEXT"):
    """
        Allows for the enhancing of Non Automation Kit exceptions.
    """

    # AKitErrorEnhancer just uses Duck typing so it should be safe to dynamically
    # append any exception that does not already inherit include AKitErrorEnhancer
    # in its base clases list.
    if AKitErrorEnhancer not in xcpt.__bases__:
        xcpt.__bases__ += (AKitErrorEnhancer,)
        xcpt._context = {}

    xcpt.add_context(content, label=label)

    return

# ==================================================================================
#                     CONFIGURATION - BASE ERROR CLASSIFICATIONS
# ==================================================================================
class AKitConfigurationError(AKitBaseException):
    """
        The base error object for errors that indicate that there is an issue related
        to improper configuration.
    """

class AKitInvalidConfigError(AKitConfigurationError):
    """
        This error is raised when an IntegrationCoupling object has been passed invalid configuration parameters.
    """

class AKitMissingConfigError(AKitConfigurationError):
    """
        This error is raised when an IntegrationCoupling object is missing required configuration parameters.
    """


# ==================================================================================
#                     IMPROPER USE - BASE ERROR CLASSIFICATIONS
# ==================================================================================
class AKitSemanticError(AKitBaseException):
    """
        The base error object for errors that indicate that there is an issue with
        a piece of automation code and with the way the Automation Kit code is being
        utilized.
    """


# ==================================================================================
#                        ENVIRONMENTAL - LANDSCAPE RELATED ERRORS
# ==================================================================================
class AKitLandscapeError(AKitError):
    """
        The base error object for errors that indicate that there is an issue related
        to the interaction, usage or consumption of an environmental resources.
    """

class AKitInitialConnectivityError(AKitLandscapeError):
    """
        This error is raised when an IntegrationCoupling object is unable to establish an initial level of
        connectivity with a connected resource.
    """

class AKitMissingResourceError(AKitLandscapeError):
    """
        This error is raised when an device or resources was declared in the landscape.yaml file
        but was not able to be found during device or resource discovery.
    """

class AKitResourceError(AKitLandscapeError):
    """
        This error is raised when a resource requirement was not able to be obtained.
    """

# ==================================================================================
#                           RUNTIME RELATED ERRORS
# ==================================================================================

class AKitRuntimeError(RuntimeError, AKitErrorEnhancer):
    """
        The base error object for errors that indicate that an error was produced during
        the execution of task or test code and the error was not able to be classified
        as Configuration, Landscape, or Semantic related.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitCommunicationsProtocolError(AKitRuntimeError):
    """
        This is the base error for exceptions that are related to communciations protocols
    """

class AKitEstablishPresenceError(AKitLandscapeError):
    """
        This error occurs when an integration coupling has trouble establishing a presence in the
        test landscape.
    """

class AKitCommandError(AKitCommunicationsProtocolError):
    """
        This error is the base error for HTTP requests based errors.
    """
    def __init__(self, message, status, stdout, stderr, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.status = status
        self.stdout = stdout
        self.stderr = stderr
        return

class AKitHTTPRequestError(AKitCommunicationsProtocolError):
    """
        This error is the base error for HTTP requests based errors.
    """
    def __init__(self, message, requrl, status_code, reason, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.requrl = requrl
        self.status_code = status_code
        self.reason = reason
        return

class AKitOpenWRTRequestError(AKitCommunicationsProtocolError):
    """
        This error is the base error OpenWRT inter-op command request errors.
    """

class AKitOutOfScopeError(AKitRuntimeError):
    """
        This error is raised when a method is called on a ScopeCoupling that is not in scope.  A test can have,
        multiple ScopeCoupling(s) and can run in multiple scopes but the test must be instantiated and run in
        each scope individually.
    """

class AKitReaderError(AKitRuntimeError):
    """
        This error indicates that an error was encoutered while attempting to read and extract data
        from text content.
    """

class AKitRequestStopError(AKitRuntimeError):
    """
        This error is raised when a test indicates it wants to stop an automation run.  The `TestSequencer`
        may or may not stop the automation run as a result of a test or scope raising this error.  The
        `TestSequencer` looks at the current runtime context which was set by the commandline arguements
        and will stop the test run if the runtime context indicates that stopping is allowed.
    """

class AKitScopeEntryError(AKitRuntimeError):
    """
        This error is raised when a ScopeCoupling was unable to complete the entry of a scope.
    """

class AKitSetupError(AKitRuntimeError):
    """
        An error occured during the setup of a Task, Test, Step or Process
    """

class AKitSkipError(AKitRuntimeError):
    """
        This error is raised when a test indicates it wants to be skipped while being run
    """
    def __init__(self, *args, reason=None, bug=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reason = reason
        self.bug = bug
        return

class AKitLooperError(AKitRuntimeError):
    """
        This error is raised when an error occurs with the use of the :class:`LooperPool` or
        :class:`Looper` objects.
    """

class AKitLooperQueueShutdownError(AKitRuntimeError):
    """
        This error is raised when work is being queued on a :class:`LooperQueue` thaat has
        been shutdown and when a worker thread is attempting to wait for work on an empty
        queue.
    """

class AKitUnknownParameterError(AKitRuntimeError):
    """
        This error is raised when the test framework encounters an unknown or unresolvable parameter.
    """

class AKitAbstractMethodError(AKitRuntimeError):
    """
        This error is raised when an abstract method has been called.
    """

class AKitNotImplementedError(NotImplementedError, AKitErrorEnhancer):
    """
        This error is raised when a method is called that has not yet been implemented.
    """

class AKitNotOverloadedError(AKitRuntimeError):
    """
        This error is raised when a method that must be overloaded has not been overridden.
    """
class AKitNotSupportedError(AKitRuntimeError):
    """
        This error is raised when a method that must be overloaded has not been overridden.
    """

class AKitRecursionError(RecursionError, AKitErrorEnhancer):
    """
        This error is raised when a method that must be overloaded has not been overridden.
    """
    def __init__(self, *args, reason=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reason = reason
        return

class AKitServiceUnAvailableError(AKitRuntimeError):
    """
        This error is raised when a service is requested that is not currently available.
    """

# ==================================================================================
#                           TOOLING ERRORS
# ==================================================================================

class AKitGeneratorError(AKitError):
    """
        This error is raised when a code generator tool has encountered an issue.
    """

class AKitGenerateItemError(AKitError):
    """
        This error is raised when a code generator tool has missing data or insuffient
        data to continue to generate the current item.
    """

# ==================================================================================
#                         ENHANCED BUILTIN ERRORS
# ==================================================================================

class AKitArithmeticError(ArithmeticError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitFloatingPointError(FloatingPointError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitOverflowError(OverflowError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitZeroDivisionError(ZeroDivisionError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitAssertionError(AssertionError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return
class AKitAttributeError(AttributeError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitBufferError(BufferError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitEOFError(EOFError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitImportError(ImportError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitModuleNotFoundError(ModuleNotFoundError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitLookupError(LookupError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitIndexError(LookupError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitKeyError(KeyError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitMemoryError(MemoryError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitNameError(NameError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitUnboundLocalError(UnboundLocalError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitOSError(OSError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitBlockingIOError(BlockingIOError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitChildProcessError(ChildProcessError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitConnectionError(ConnectionError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitBrokenPipeError(BrokenPipeError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitConnectionAbortedError(ConnectionAbortedError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitConnectionRefusedError(ConnectionRefusedError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitConnectionResetError(ConnectionResetError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitFileExistsError(FileExistsError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitFileNotFoundError(FileNotFoundError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitInterruptedError(InterruptedError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitIsADirectoryError(IsADirectoryError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitNotADirectoryError(NotADirectoryError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitPermissionError(PermissionError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitProcessLookupError(ProcessLookupError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitTimeoutError(TimeoutError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitReferenceError(ReferenceError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitSyntaxError(SyntaxError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitIndentationError(IndentationError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitTabError(TabError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitSystemError(SystemError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitTypeError(TypeError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitValueError(ValueError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitUnicodeError(UnicodeError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitUnicodeDecodeError(UnicodeDecodeError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitUnicodeEncodeError(UnicodeEncodeError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

class AKitUnicodeTranslateError(UnicodeTranslateError, AKitErrorEnhancer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return

