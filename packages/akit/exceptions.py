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
import os
import traceback

from akit.xinspect import get_caller_function_name
from akit.xformatting import split_and_indent_lines

class AKitError(Exception):
    """
        The base error object for Automation Kit errors.  The :class:`AKitError` serves as aa base
        type and also provides some additional functionality for adding context to errors and
        formatting exception output.
    """
    def __init__(self, *args, **kwargs):
        super(AKitError, self).__init__(*args, **kwargs)
        self._context = {}
        return

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

    def format_exc(self):
        """
            Format the exception along with any added context.


        """
        etypename = type(self).__name__
        eargs = self.args


        exmsg_lines = [
            "%s: %s" % (etypename, repr(eargs).rstrip(",")),
            "TRACEBACK (most recent call last):"
        ]

        if len(self._context) > 0:
            stack_frames = self._collect_stack_frames()
            stack_frames_len = len(stack_frames)
            for co_filename, co_lineno, co_name, co_code, co_context in stack_frames:

                exmsg_lines.extend([
                    '  File "%s", line %d, in %s' % (co_filename, co_lineno, co_name),
                    "    %s" % co_code
                ])
                if co_name in self._context:
                    cxtinfo = self._context[co_name]
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

        exmsg = os.linesep.join(exmsg_lines)
        return exmsg

    def _collect_stack_frames(self):

        last_items = None
        tb_code = None
        tb_lineno = None
        traceback_list = []

        for tb_frame, tb_lineno in traceback.walk_tb(self.__traceback__):
            tb_code = tb_frame.f_code
            co_filename = tb_code.co_filename
            co_name = tb_code.co_name
            co_arg_names = tb_code.co_varnames[:tb_code.co_argcount]
            co_argcount = tb_code.co_argcount
            co_locals = tb_frame.f_locals

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

            if os.path.exists(co_filename) and co_filename.endswith(".py"):
                context_lines, context_startline = inspect.getsourcelines(tb_code)
                context_lines = [cline.rstrip() for cline in context_lines]
                clindex = (tb_lineno - context_startline)
                last_items[-2] = context_lines[clindex].strip()
                last_items[-1] = context_lines

        return traceback_list



# ==================================================================================
#                            BASE ERROR CLASSIFICATIONS
# ==================================================================================

class AKitConfigurationError(AKitError):
    """
        The base error object for errors that indicate that there is an issue related
        to improper configuration.
    """

class AKitLandscapeError(AKitError):
    """
        The base error object for errors that indicate that there is an issue related
        to the interaction usage or consumption of an environmental resources.
    """

class AKitRuntimeError(AKitError):
    """
        The base error object for errors that indicate that an error was produced during
        the execution of task or test code and the error was not able to be classified
        as Configuration, Landscape, or Semantic related.
    """

class AKitSemanticError(AKitError):
    """
        The base error object for errors that indicate that there is an issue with
        a piece of automation code and with the way the Automation Kit code is being
        utilized.
    """

# ==================================================================================
#                         CONFIGURATION RELATED ERRORS
# ==================================================================================

class AKitInvalidConfigError(AKitConfigurationError):
    """
        This error is raised when an IntegrationMixIn object has been passed invalid configuration parameters.
    """

class AKitMissingConfigError(AKitConfigurationError):
    """
        This error is raised when an IntegrationMixIn object is missing required configuration parameters.
    """


# ==================================================================================
#                           LANDSCAPE RELATED ERRORS
# ==================================================================================
class AKitInitialConnectivityError(AKitLandscapeError):
    """
        This error is raised when an IntegrationMixIn object is unable to establish an initial level of
        connectivity with a connected resource.
    """

class AKitMissingResourceError(AKitLandscapeError):
    """
        This error is raised when an device or resources was declared in the landscape.yaml file
        but was not able to be found during device or resource discovery.
    """

class AKitResourceError(AKitLandscapeError):
    """
        This error is raised when an IntegrationMixIn object was unable to obtain a required resource.
    """

# ==================================================================================
#                           RUNTIME RELATED ERRORS
# ==================================================================================

class AKitCommunicationsProtocolError(AKitRuntimeError):
    """
        This is the base error for exceptions that are related to communciations protocols
    """

class AKitEstablishPresenceError(AKitLandscapeError):
    """
        This error occurs when an integration mixin has trouble establishing a presence in the
        test landscape.
    """
class AKitHTTPRequestError(AKitCommunicationsProtocolError):
    """
        This error is the base error for HTTP requests based errors.
    """
class AKitOutOfScopeError(AKitRuntimeError):
    """
        This error is raised when a method is called on a ScopeMixIn that is not in scope.  A test can have,
        multiple ScopeMixIn(s) and can run in multiple scopes but the test must be instantiated and run in
        each scope individually.
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
        This error is raised when a ScopeMixIn was unable to complete the entry of a scope.
    """

class AKitSetupError(AKitRuntimeError):
    """
        An error occured during the setup of a Task, Test, Step or Process
    """

class AKitSkipError(AKitRuntimeError):
    """
        This error is raised when a test indicates it wants to be skipped while being run
    """
    def __init__(self, *args, reason=None, **kwargs):
        super(AKitSkipError, self).__init__(*args, **kwargs)
        self.reason = reason
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

class AKitTimeoutError(AKitRuntimeError):
    """
        This error is raised when a timeout occurs
    """

class AKitUnknownParameterError(AKitRuntimeError):
    """
        This error is raised when the test framework encounters an unknown or unresolvable parameter.
    """

# ==================================================================================
#                           SEMANTIC RELATED ERRORS
# ==================================================================================

class AKitAbstractMethodError(AKitSemanticError):
    """
        This error is raised when an abstract method has been called.
    """

class AKitNotImplementedError(AKitSemanticError):
    """
        This error is raised when a method is called that has not yet been implemented.
    """

class AKitNotOverloadedError(AKitSemanticError):
    """
        This error is raised when a method that must be overloaded has not been overridden.
    """
