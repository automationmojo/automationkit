
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
from akit.integration import landscaping

from akit.jsos import CHAR_RECORD_SEPERATOR
from akit.mixins.scope import inherits_from_scope_mixin
from akit.paths import get_path_for_output
from akit.results import ResultContainer, ResultType

from akit.testing.testplus.testcollector import TestCollector
from akit.testing.testplus.registration.resourceregistry import resource_registry
from akit.testing.testplus.testgroup import TestGroup
from akit.testing.testplus.testref import TestRef


logger = logging.getLogger("AKIT")

TEMPLATE_TESTRUN_SEQUENCE_MODULE = '''
"""
    This is a working copy of what I envision a code generated execution sequence document might look like.
    The general concept here is that if you generate a flat test execution sequence and run it, then it might
    make debugging the setup, teardown, and execution of tests easier.

    We are basically unrolling the iterators that would normally be used to execute a series of tests.  The execution
    sequence file would be available in the output folder along with the logs and such as an artifact of the test run.
"""
import logging

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()
'''

class TEST_SEQUENCER_PHASES:
    """
        Indicates the current state of the sequencer.
    """
    Initial = 0
    Discovery = 1
    Collection = 2
    Graph = 3
    Traversal = 4

class TEST_DEBUG_MODE:
    NONE = 0
    PDB = 1
    RPDB = 2

class TestSequencer(ContextUser):
    """
        The :class:`TestSequencer` is a state machine that helps to orchestrate the flow fo the test run.  It ensures
        that the steps of the test flow are consistent between runs.
    """

    def __init__(self, jobtitle: str, root: str, includes: Sequence[str], excludes: Sequence[str], debug_mode=TEST_DEBUG_MODE.NONE):
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
        self._debug_mode = debug_mode
        self._integrations = {}
        self._references = []
        self._scopes = {}
        self._scope_roots = []
        self._import_errors = []
        self._testtree = None
        self._landscape = None
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
    def references(self):
        """
            A list of :class:`TestRef` objects that are included in the test run.
        """
        return self._references

    @property
    def testnodes(self):
        """
        """
        root_nodes = [tnode for _, tnode in self._testtree]
        return root_nodes

    @property
    def testtree(self):
        """
        """
        return self._testtree

    def attach_to_framework(self, landscape):
        """
            Goes through all the integrations and provides them with an opportunity to
            attach to the test environment.
        """

        self._landscape = landscape

        for _, integ_type in self._integrations.items():
            integ_type.attach_to_framework(landscape)

        return

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

        for _, integ_type in self._integrations.items():
            integ_type.attach_to_environment()

        return

    def collect_resources(self):
        """
            Goes through all the integrations and provides them with an opportunity to
            collect shared resources that are required for testing.
        """

        for _, integ_type in self._integrations.items():
            integ_type.collect_resources()

        return

    def discover(self, test_module=None, include_integrations: bool=True):
        """
            Initiates the discovery phase of the test run.
        """
        collector = TestCollector(self._root, excludes=self._excludes, test_module=test_module)

        # Discover the tests, integration points, and scopes.  If test modules is not None then
        # we are running tests from an individual module and we can limit discovery to the test module
        for inc_item in self._includes:
            collector.collect_references(inc_item)

        self._testtree = TestGroup("<session>")
        self._references = collector.references
        for _, trval in self._references.items():
            self._testtree.add_descendent(trval)

        testcount = len(self._references)
        if testcount > 0:
            if include_integrations:
                self._integrations, self._scopes = collector.collect_integrations_and_scopes()
            self._import_errors = collector.import_errors

        return testcount

    def establish_integration_order(self):
        """
            Re-orders the integrations based on any declared precedences.
        """

        for _, integ_type in self._integrations.items():
            integ_type.establish_integration_order()

        return

    def establish_presence(self):
        """
            Goes through all the integrations and provides them with an opportunity to
            establish a presence or persistant services with the test resource or resources
            they are integrating into the automation run.
        """

        for _, integ_type in self._integrations.items():
            integ_type.establish_presence()

        return

    def execute_tests(self, runid: str, recorder, sequencer):
        """
            Called in order to execute the tests contained in the :class:`TestPacks` being run.
        """
        exit_code = 0

        res_name = "<session>"

        root_container = ResultContainer(runid, res_name, ResultType.JOB)
        recorder.record(root_container)

        for testref in sequencer():
            self._traverse_testpack(testref, recorder, parent_inst=runid)

        return exit_code

    def generate_testrun_sequence_document(self, outputfilename: str, indent_space="    "):

        with open(outputfilename, 'w') as sdf:
            current_node = self._testtree

            sdf.write(TEMPLATE_TESTRUN_SEQUENCE_MODULE)

            scopes_called = self._generate_session_method(sdf, self._testtree, indent_space)

            while len(scopes_called) > 0:
                sdf.write(os.linesep)
                scope_module, scope_name, scope_node, scope_call_args = scopes_called.pop(0)
                child_scopes_called = self._generate_scope_method(sdf, scope_module, scope_name, scope_node, scope_call_args, indent_space)
                child_scopes_called.extend(scopes_called)
                scopes_called = child_scopes_called

        return

    def _generate_session_method(self, outf, root_node, indent_space):
        """
            Generates the :function:`session` entry point function or the test run
            sequence document.
        """
        scopes_called = []

        current_indent = indent_space

        method_lines = [
            'def session(sequencer):',
            '{}"""'.format(current_indent),
            '{}This is the entry point for the test run sequence document.'.format(indent_space),
            '{}"""'.format(current_indent)
        ]

        if self._debug_mode == TEST_DEBUG_MODE.PDB:
            method_lines.append('')
            method_lines.append('{}# The debug flag was passed on the commandline so we break here.'.format(current_indent))
            method_lines.append('{}import pdb'.format(current_indent))
            method_lines.append('{}pdb.set_trace()'.format(current_indent))
        elif self._debug_mode == TEST_DEBUG_MODE.RPDB:
            method_lines.append('')
            method_lines.append('{}# The remote debug flag was passed on the commandline so we break here.'.format(current_indent))
            method_lines.append('{}import rpdb'.format(current_indent))
            method_lines.append('{}debugger = rpdb.Rpdb(port=12345)'.format(current_indent))
            method_lines.append('{}debugger.set_trace()'.format(current_indent))

        method_lines.append('')
        method_lines.append('{}with sequencer.enter_session_scope_context() as ssc:'.format(current_indent))
        method_lines.append('')

        current_indent = current_indent + indent_space

        this_scope = root_node.get_resource_scope()
        # Import all the parameter source functions
        for _, porigin in this_scope.parameters.items():
            method_lines.append('{}from {} import {}'.format(current_indent, porigin.source_module_name, porigin.source_function.__name__))
        method_lines.append('')

        # Create the calls to all of the root test scopes
        child_call_args = ['sequencer']

        # Create the variables with session scope
        for pname, porigin in this_scope.parameters.items():
            source_func_call = porigin.generate_call()
            method_lines.append('{}for {} in {}:'.format(current_indent, pname, source_func_call))
            child_call_args.append(pname)
            current_indent = current_indent + indent_space

        child_name_list = [cnk for cnk in root_node.children.keys()]
        child_name_list.sort()
        for child_name in child_name_list:
            child_node = root_node.children[child_name]
            scope_module = child_name
            if child_node.package:
                scope_module = child_node.package + "." + child_name
            scope_name = scope_module.replace(".", "_")
            call_line = '{}scope_{}({})'.format(current_indent, scope_name, ", ".join(child_call_args))
            method_lines.append(call_line)
            scopes_called.append((scope_module, scope_name, child_node, child_call_args))

        method_lines.append('')
        method_lines.append('{}return'.format(indent_space))
        method_lines.append('')

        method_content = os.linesep.join(method_lines)
        outf.write(method_content)

        return scopes_called

    def _generate_scope_method(self, outf, scope_module, scope_name, scope_node, scope_call_args, indent_space):
        scopes_called = []

        current_indent = "    "

        method_lines = [
            'def scope_{}({}):'.format(scope_name, ", ".join(scope_call_args)),
            '{}"""'.format(current_indent),
            "{}This is the entry point for the '{}' test scope.".format(current_indent, scope_name),
            '{}"""'.format(current_indent),
            '',
            '{}with sequencer.enter_module_scope_context("{}") as msc:'.format(current_indent, scope_module)
        ]

        current_indent = current_indent + indent_space

        this_scope = scope_node.get_resource_scope()

        # Import all the parameter source functions
        for _, porigin in this_scope.parameters.items():
            method_lines.append('{}from {} import {}'.format(current_indent, porigin.source_module_name, porigin.source_function.__name__))
        method_lines.append('')

        # Create the calls to all of the root test scopes
        child_call_args = [arg for arg in scope_call_args]

        # Create the variables with session scope
        for pname, porigin in this_scope.parameters.items():
            source_func_call = porigin.generate_call()
            method_lines.append('{}for {} in {}:'.format(current_indent, pname, source_func_call))
            child_call_args.append(pname)
            current_indent = current_indent + indent_space

        child_name_list = [cnk for cnk in scope_node.children.keys()]
        child_name_list.sort()
        for child_name in child_name_list:
            child_node = scope_node.children[child_name]
            if isinstance(child_node, TestRef):
                test_args = []
                for param_name in child_node.subscriptions:
                    test_args.append(param_name)
                call_line = '{}{}({})'.format(current_indent, child_node.test_base_name, ", ".join(test_args))
                method_lines.append(call_line)
            else:
                scope_module = child_name
                if child_node.package:
                    scope_module = child_node.package + "." + child_name
                scope_name = scope_module.replace(".", "_")
                call_line = '{}scope_{}({})'.format(current_indent, scope_name, ", ".join(child_call_args))
                method_lines.append(call_line)
                scopes_called.append((scope_module, scope_name, child_node, child_call_args))

        method_lines.append('')
        method_lines.append('{}return'.format(indent_space))
        method_lines.append('')

        method_content = os.linesep.join(method_lines)
        outf.write(method_content)

        return scopes_called

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
