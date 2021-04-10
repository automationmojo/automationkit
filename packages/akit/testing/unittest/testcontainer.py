"""
.. module:: testcontainer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the base :class:`TestContainer` type and derived categorized test
        containers such as :class:`ArchitectureTestContainer`, :class:`BrickTestContainer`,
        :class:`LimitsTestContainer`, :class:`NegativeTestContainer`, :class:`BrickTestContainer`,
        :class:`SmokeTestContainer`, :class:`StressTestContainer`

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

from types import MethodType, TracebackType
from typing import Optional, Sequence

import inspect
import sys
import traceback
import uuid

from akit.metadata import Category, Priority
from akit.exceptions import AKitSkipError
from akit.results import ResultType, ResultNode
from akit.recorders import ResultRecorder
from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

class TEST_CATEGORIES:
    """
        Labels for the different types of test categories.
    """
    ARCHITECTURE = "ARCHITECTURE"
    BRICK = "BRICK"
    LIMITS = "LIMITS"
    NEGATIVE = "NEGATIVE"
    POSITIVE = "POSITIVE"
    STRESS = "STRESS"
    SMOKE = "SMOKE"

class TestContainer:
    """
        The `TestContainer` object is the base container object that all other test containers
        should derive from.  The 'akit' framework unitizes the `TestContainer` as a code construct
        that is used to link testcases to external resources and also as a declaritive way to
        link test cases to the scopes of execution that they should execute in.  `TestContainer`s
        provide:

        * class and instance methods
        * class and instance data
        * integrated entities
        * a distrubuted context
        * a target scope that resides in a hierachy of scopes with a determined path
          and code to be able to enter and exit the target scope

        To integrate a testcase into the 'Automation Kit' test environment, a tester creates a
        test container class that derives from `TestContainer` itself or from a derived test.

        Users can define an entire hierarchy of `TestContainer` object that are used to pass on
        inherited or shared functionality to a derived container, however the primary means of passing
        on functionality should not necessarily be through the inheritance of a container.

        The passing on of functionality should take place through the appropriate parent or mixin
        type.  For example functionality that is used to interact with an external resource might
        come in through the inclusion of an :class:`akit.mixins.integration.IntegrationMixIn`
        parent type.  The passing on of functionality that is used to interact with a test containers
        target scope of execution should be included through the :class:`akit.mixins.scopes.ScopeMixIn`.
    """

    def __init__(self, testmethod: MethodType, recorder: ResultRecorder, *args, extname: str = None, parameters: Optional[Sequence] = None, **kwargs):
        """
            Intializes an instance of the test container along with the test method that is to be run for
            a given test instance.

            :param testmethod: The test method to run for this instance of a test container.
            :param recorder: A recorder object to report test results to.
            :param *args: Handle the passing of positional parameters.
            :param extname: The extended name of the test container in the event that parameterization is used.
            :param parameters: The parameters to pass for the test instance to use.
            :param **kwargs: A catch all for any kwargs that are passed to the constructor.
        """
        self._testmethod = testmethod
        self._args = args
        self._extname = extname
        self._parameters = parameters
        self._kwargs = kwargs
        self._instance_id = str(uuid.uuid4())
        self._recorder = recorder
        self._cleanup_steps = []
        self._result = None
        return

    @property
    def instance_id(self) -> str:
        """
            The point in time uuid identifier for this instance of a particular test.
        """
        return self._instance_id

    @property
    def testname(self) -> str:
        """
            The full test name of the test.
        """
        tcls = self.__class__
        tname = "%s@%s#%s" % (tcls.__module__, tcls.__name__, self._testmethod.__name__)
        if self._extname is not None:
            tname = "%s[%s]" % (tname, self._extname)
        return tname

    @property
    def extname(self):
        """
            The extended name of the test based on the parameterized parameters for this test instance.
        """
        return self._extname

    @property
    def parameters(self):
        """
            The parameterized parameters for this test instance if there are any.
        """
        return self._parameters

    def run(self, parent_inst: str):
        """
            The 'run' method controls the sequence of steps for the setup for a test, the running of a test, and the
            cleanup after the test.  It also lays out the behaviors that occur when a test fails and handles
            the capture and reporting of test results.

            :param parent_inst: The instance id of the parent ResultNode instance to mark as the parent for the ResultNode
                                created for the results of this test.
        """

        self._result = ResultNode(self._instance_id, self.testname, ResultType.TEST, parent_inst=parent_inst)

        testname = self.testname
        try:
            logger.info("RUNNING: TestCase %s" % testname)
            try:
                self.setUp()

                try:
                    self._testmethod(self)
                    self._mark_pass()
                except AssertionError:
                    etype, einst, etb = sys.exc_info()
                    self._handle_failure(self._testmethod, etype, einst, etb)
                except Exception: # pylint: disable=broad-except
                    etype, einst, etb = sys.exc_info()
                    self._handle_error(self._testmethod, etype, einst, etb)

            except AKitSkipError as skp_err:
                self._mark_skip(skp_err.reason)
            except Exception: # pylint: disable=broad-except
                etype, einst, etb = sys.exc_info()
                self._handle_setup_error(etype, einst, etb)
            finally:
                cleanup_steps = list(self._cleanup_steps)
                while len(cleanup_steps) > 0:
                    cstep = cleanup_steps.pop()
                    try:
                        cstep()
                    except Exception: # pylint: disable=broad-except 
                        etype, einst, etb = sys.exc_info()
                        self._handle_cleanup_error(etype, einst, etb)

        finally:
            self._result.finalize()
            logger.info("    %s: TestCase %s" % (self._result.result_code.name, testname))

        self._recorder.record(self._result)

        return

    def setUp(self): # pylint: disable=no-self-use
        """
            The test method called to setup the test for a test instance.
        """
        return

    def _handle_failure(self, tmethod: MethodType, ftype: type, finst: Exception, ftb: TracebackType):
        """
            Handler for failure exceptions that occur during the running of the test.
        """
        fail_lines = traceback.format_exception(ftype, finst, ftb)
        self._result.add_failure(fail_lines)
        self._result.set_documentation(tmethod.__doc__)
        return

    def _handle_error(self, tmethod: MethodType, etype: type, einst: Exception, etb: TracebackType):
        """
            Handler for error exceptions that occur during the running of the test.
        """
        error_lines = traceback.format_exception(etype, einst, etb)
        self._result.add_error(error_lines)
        self._result.set_documentation(tmethod.__doc__)
        return

    def _handle_cleanup_error(self, etype: type, einst: Exception, etb: TracebackType):
        """
            Handles the cleanup step error by recording a warning.
        """
        warn_lines = traceback.format_exception(etype, einst, etb)
        self._result.add_warning(warn_lines)
        return

    def _handle_setup_error(self, etype: type, einst: Exception, etb: TracebackType):
        """
            Handles the setup error from the setup of this test instance.
        """
        error_lines = traceback.format_exception(etype, einst, etb)
        self._result.add_error(error_lines)
        return

    def _mark_pass(self):
        """
            Mark this test as passed.
        """
        return self._result.mark_passed()

    def _mark_skip(self, reason):
        """
            Mark this test as skipped.
        """
        return self._result.mark_skip(reason)

@Category(TEST_CATEGORIES.ARCHITECTURE)
class ArchitectureTestContainer(TestContainer):
    """
        The `ArchitectureTestContainer` is a categorized `TestContainer` derivative that can be used
        as a base type for derivative test containers.  The `ArchitectureTestContainer` attaches the
        'ARCHITECTURE' category to the tests that reside in the container.
    """

@Category(TEST_CATEGORIES.BRICK)
class BrickTestContainer(TestContainer):
    """
        The `BrickTestContainer` is a categorized `TestContainer` derivative that can be used
        as a base type for derivative test containers.  The `BrickTestContainer` attaches the
        'BRICK' category to the tests that reside in the container.
    """

@Category(TEST_CATEGORIES.LIMITS)
class LimitsTestContainer(TestContainer):
    """
        The `LimitsTestContainer` is a categorized `TestContainer` derivative that can be used
        as a base type for derivative test containers.  The `LimitsTestContainer` attaches the
        'LIMITS' category to the tests that reside in the container.
    """

@Category(TEST_CATEGORIES.NEGATIVE)
class NegativeTestContainer(TestContainer):
    """
        The `NegativeTestContainer` is a categorized `TestContainer` derivative that can be used
        as a base type for derivative test containers.  The `NegativeTestContainer` attaches the
        'NEGATIVE' category to the tests that reside in the container.
    """

@Category(TEST_CATEGORIES.POSITIVE)
class PositiveTestContainer(TestContainer):
    """
        The `PositiveTestContainer` is a categorized `TestContainer` derivative that can be used
        as a base type for derivative test containers.  The `PositiveTestContainer` attaches the
        'POSITIVE' category to the tests that reside in the container.
    """

@Category(TEST_CATEGORIES.STRESS)
class StressTestContainer(TestContainer):
    """
        The `StressTestContainer` is a categorized `TestContainer` derivative that can be used
        as a base type for derivative test containers.  The `StressTestContainer` attaches the
        'STRESS' category to the tests that reside in the container.
    """

@Priority(0)
@Category(TEST_CATEGORIES.SMOKE)
class SmokeTestContainer(TestContainer):
    """
        The `SmokeTestContainer` is a categorized `TestContainer` derivative that can be used
        as a base type for derivative test containers.  The `SmokeTestContainer` attaches the
        'SMOKE' category to the tests that reside in the container.
    """

def inherits_from_testcontainer(cls):
    """
        Helper method that detects if an objects type inherits from :class:`TestContainer` but
        ensures that the object is not a :class:`TestContainer` type from this file.
    """
    is_testcontainer = False
    if inspect.isclass(cls) and cls is not TestContainer and issubclass(cls, TestContainer):
        is_testcontainer = True
    return is_testcontainer
