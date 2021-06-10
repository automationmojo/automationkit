
"""
.. module:: testsequencer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the base :class:`TestSequencer` type which is use to control
        the flow of the automation environment startup and test execution sequence.

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

from typing import Sequence

import logging
import json
import os
import sys
import uuid

import akit.environment.activate # pylint: disable=unused-import
from akit.environment.context import ContextUser

from akit.jsos import CHAR_RECORD_SEPERATOR
from akit.mixins.scope import inherits_from_scope_mixin
from akit.paths import get_path_for_output
from akit.results import ResultContainer, ResultType
from akit.testing.testplus.testcollector import TestCollector


logger = logging.getLogger("AKIT")

class TEST_SEQUENCER_PHASES:
    """
        Indicates the current state of the sequencer.
    """
    Initial = 0
    Discovery = 1
    Collection = 2
    Graph = 3
    Traversal = 4

class TestSequencer(ContextUser):
    """
        The :class:`TestSequencer` is a state machine that helps to orchestrate the flow fo the test run.  It ensures
        that the steps of the test flow are consistent between runs.
    """

    def __init__(self, jobtitle: str, root: str, includes: Sequence[str], excludes: Sequence[str]):
        """
            Creates a 'TestSequencer' object which is used to discover the tests and control the flow of a test run.

            :param jobtitle: The name of the test job.
            :param root: The path to the root folder that is the base of the tests.
            :param includes: List of expressions used to determine which tests to include.
                             (scope):(package).(package)@(module)#(testname)
            :param excludes: List of expressions used to determine which tests to exclued from the included tests.

        """
        self._jobtitle = jobtitle
        self._root = root
        self._includes = includes
        self._excludes = excludes
        self._integrations = []
        self._references = []
        self._scopes = []
        self._scope_roots = []
        self._import_errors = []
        self._testpacks = []
        return

    def __enter__(self):
        """
            Provides 'with' statement scope semantics for the :class:`TestSequencer`
        """
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        """
            Provides 'with' statement scope semantics for the :class:`TestSequencer`
        """
        return False

    @property
    def import_errors(self):
        """
            A list of import errors that were encountered during the sequencing of the test run.
        """
        return self._import_errors

    @property
    def testpacks(self):
        """
            A list of :class:`TestPack` objects that are included in the test run.
        """
        return self._testpacks

    def attach_to_environment(self, landscape):
        """
            Goes through all the integrations and provides them with an opportunity to
            attach to the test environment.
        """

        results_dir = get_path_for_output()
        
        environment_dict = {}
        environment_dict.update(os.environ)
        
        for key in environment_dict.keys():
            if key.find("PASSWORD") > -1:
                environment_dict[key] = "(hidden)"

        packages = {}
        for mname, mobj in sys.modules.items():
            if mname.find(".") == -1 and hasattr(mobj, "__file__"):
                packages[mname] = mobj.__file__

        startup_dict = {
            "environment": environment_dict,
            "command": " ".join(sys.argv),
            "packages": packages
        }

        startup_full = os.path.join(results_dir, "startup-configuration.json")
        with open(startup_full, 'w') as suf:
            json.dump(startup_dict, suf, indent=True)

        for integ, _ in self._integrations:
            integ.attach_to_environment(landscape)

        return

    def collect_resources(self):
        """
            Goes through all the integrations and provides them with an opportunity to
            collect shared resources that are required for testing.
        """

        for integ, _ in self._integrations:
            integ.collect_resources()

        return

    def establish_integration_order(self):
        """
            Re-orders the integrations based on any declared precedences.
        """

        for integ, _ in self._integrations:
            integ.establish_integration_order()

        return

    def establish_connectivity(self):
        """
            Goes through all the integrations and provides them with an opportunity to
            establish connectivity with the test resource or resources they are integrating
            into the automation run.
        """

        for integ, _ in self._integrations:
            integ.establish_connectivity()

        return

    def discover(self, test_module=None):
        """
            Initiates the discovery phase of the test run.
        """
        collector = TestCollector(self._root, excludes=self._excludes, test_module=test_module)

        # Discover the tests, integration points, and scopes.  If test modules is not None then
        # we are running tests from an individual module and we can limit discovery to the test module
        for inc_item in self._includes:
            collector.collect_references(inc_item)

        collector.expand_testpacks()

        self._references = collector.references

        testcount = len(self._references)
        if testcount > 0:
            self._integrations = collector.collect_integrations()
            self._testpacks = collector.collect_testpacks()
            self._import_errors = collector.import_errors

        return testcount

    def execute_testpacks(self, runid: str, recorder, sequencer):
        """
            Called in order to execute the tests contained in the :class:`TestPacks` being run.
        """
        exit_code = 0

        res_name = "(root)"

        root_container = ResultContainer(runid, res_name, ResultType.JOB)
        recorder.record(root_container)

        for tpack in sequencer():
            self._traverse_testpack(tpack, recorder, parent_inst=runid)

        return exit_code

    def parse_extended_args(self, base_parser): # pylint: disable=no-self-use,unused-argument
        """
            Called for the sequencer to parse the extended arguments to be passed on to integrations and mixins.
        """
        return

    def publish_integrations(self): # pylint: disable=no-self-use
        """
            Called for the sequencer to publish the integrations that it found during discovery.
        """
        return

    def record_import_errors(self, outputfilename: str):
        """
            Method that writes out the import errors to the active results directory.
        """
        with open(outputfilename, 'w') as ief:
            for modname, filename, errmsg in self._import_errors.values():
                ief.write(CHAR_RECORD_SEPERATOR)
                ieitem = {
                    "module": modname,
                    "filename": filename,
                    "trace": errmsg.splitlines(False)
                }
                json.dump(ieitem, ief, indent=4)

        return

    def _traverse_testpack(self, testpack, recorder, parent_inst=None):
        """
            This function is called in order to traverse the execution of a TestPack and its associated scope tree.  The
            `_traverse_testpack` method calls the scopes_enter method which intern will call scope_enter on its inherited scopes
            creating the correct test scope required by all of the tests in the `TestPack`.  It will then run all of the tests
            that belong to the `TestPack` and then call scopes_exit in order to tear down any scopes no longer needed by any
            `TestPack`.  The scopes can be shared scopes that can be shared across `TestPack`(s) and the scopes are reference
            counted in order to know when the last `TestPack` is finished using the scope.
        """
        testpack_key = testpack.__module__ + "." + testpack.__name__
        logger.info("TESTPACK ENTER: %s" % testpack_key)

        try:
            res_inst = str(uuid.uuid4())

            result_container = ResultContainer(res_inst, testpack_key, ResultType.TEST_CONTAINER, parent_inst=parent_inst)
            recorder.record(result_container)

            self._enter_testpack(testpack)

            for _, tref in testpack.test_references.items():

                testinst = None
                try:
                    # Create an instance of the test case using the test reference
                    testinst = tref.create_instance(recorder)
                except Exception: # pylint: disable=broad-except
                    logger.exception("Error creating test instance.")
                    raise

                try:
                    # Run the test, it shouldn't raise any exceptions unless a stop
                    # is raised or a framework exception occurs
                    testinst.run(result_container.result_inst)
                except Exception: # pylint: disable=broad-except
                    logger.exception("Error running test instance.")
                    raise
        finally:
            try:
                self._exit_testpack(testpack)
            except Exception: # pylint: disable=broad-except
                logger.exception("Error exiting testpack.")
                raise

            logger.info("TESTPACK EXIT: %s%s" % (testpack_key, os.linesep))

        return

    def _enter_testpack(self, leaf_scope): # pylint: disable=no-self-use
        rev_mro = list(leaf_scope.__mro__)
        rev_mro.reverse()

        for nxt_cls in rev_mro:
            if inherits_from_scope_mixin(nxt_cls):
                # We only want to call scope_enter when we find the type it is directly
                # implemented on
                if "scope_enter" in nxt_cls.__dict__:
                    nxt_cls.scope_enter()
                    if not hasattr(nxt_cls, "scope_enter_count"):
                        nxt_cls.scope_enter_count = 1
                    else:
                        nxt_cls.scope_enter_count += 1

        return

    def _exit_testpack(self, leaf_scope): # pylint: disable=no-self-use
        norm_mro = list(leaf_scope.__mro__)

        for nxt_cls in norm_mro:
            if inherits_from_scope_mixin(nxt_cls):
                if "scope_enter" in nxt_cls.__dict__:
                    # We only want to call scope_enter when we find the type it is directly
                    # implemented on
                    if "scope_exit" in nxt_cls.__dict__:
                        nxt_cls.scope_exit()

                    if hasattr(nxt_cls, "scope_enter_count"):
                        nxt_cls.scope_enter_count -= 1
                    else:
                        logger.error("The scope class '%s' should have had a 'scope_enter_count' class variable." % nxt_cls.__name__)
                elif "scope_exit" in nxt_cls.__dict__:
                    nxt_cls.scope_exit()
                    logger.warn("Found 'scope_exit' on class '%s' which did not have a 'scope_enter'." % nxt_cls.__name__)
        return
