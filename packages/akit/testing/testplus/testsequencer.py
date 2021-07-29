
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
import traceback
import uuid

import akit.environment.activate # pylint: disable=unused-import
from akit.environment.context import ContextUser
from akit.exceptions import AKitRuntimeError, AKitSemanticError

from akit.jsos import CHAR_RECORD_SEPERATOR
from akit.mixins.scope import inherits_from_scope_mixin
from akit.paths import get_path_for_output
from akit.results import ResultCode, ResultContainer, ResultNode, ResultType
from akit.compat import import_file

from akit.testing.testplus.testcollector import TestCollector
from akit.testing.testplus.registration.resourceregistry import resource_registry
from akit.testing.testplus.testgroup import TestGroup
from akit.testing.testplus.testref import TestRef


logger = logging.getLogger("AKIT")

TEMPLATE_TESTRUN_SEQUENCE_MODULE = '''"""
    ======================================= CODE GENERATED - DO NOT EDIT =======================================
    This is a code generated execution sequence document, do not manually edit this document.  The 'testplus'
    test framework generates this document in order to layout the test run scopes, parameter creations, and
    test calls in a user ledgible way which is easy to read and also to debug.
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

class TEST_DEBUGGER:
    PDB = 'pdb'
    DEBUGPY = 'debugpy'

class SequencerModuleScope:
    def __init__(self, sequencer, recorder, scope_name, **kwargs):
        self._sequencer = sequencer
        self._recorder = recorder
        self._scope_name = scope_name
        self._scope_args = kwargs
        self._scope_id = None
        self._parent_scope_id = None
        return

    def __enter__(self):
        self._parent_scope_id, self._scope_id = self._sequencer.scope_id_create(self._scope_name)
        result = ResultContainer(self._scope_id, self._scope_name, ResultType.TEST_CONTAINER)
        self._recorder.record(result)
        logger.info("MODULE ENTER: {}, {}".format(self._scope_name, self._scope_id))
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        handled = False

        if ex_type is not None:
            # If an exceptions was thrown in this context, it means
            # that the exception occured during the setup for this
            # module, this means we need to mark all descendant tests
            # as error'd due to a setup failure.
            errmsg = "Exception raises setting up scope='{}'".format(self._scope_name)
            logger.exception(errmsg)
            handled = True

        self._sequencer.scope_id_pop(self._scope_name)
        logger.info("MODULE EXIT: {}, {}".format(self._scope_name, self._scope_id))
        return handled

class SequencerSessionScope:
    def __init__(self, sequencer, recorder, root_result):
        self._scope_name = root_result.result_name
        self._sequencer = sequencer
        self._recorder = recorder
        self._scope_id = root_result.result_inst
        self._root_result = root_result
        return

    def __enter__(self):
        self._sequencer.scope_id_push(self._scope_name, self._scope_id)
        logger.info("SESSION ENTER: {}".format(self._scope_id))
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        handled = True
        self._sequencer.scope_id_pop(self._scope_name)
        logger.info("SESSION EXIT: {}".format(self._scope_id))
        return handled

class SequencerTestScope:
    def __init__(self, sequencer, recorder, test_name, **kwargs):
        self._sequencer = sequencer
        self._recorder = recorder
        self._test_name = test_name
        self._scope_args = kwargs
        self._scope_id = None
        self._parent_scope_id = None
        self._result = None
        return

    def __enter__(self):
        self._parent_scope_id, self._scope_id = self._sequencer.scope_id_create(self._test_name)
        logger.info("TEST SCOPE ENTER: {}, {}".format(self._test_name, self._scope_id))
        self._result = ResultNode(self._scope_id, self._test_name, ResultType.TEST, parent_inst=self._parent_scope_id)
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        handled = True

        if ex_type is not None:
            # If an exceptions was thrown in this context, it means
            # that a test threw an exception.
            ex_lines = traceback.format_exception(ex_type, ex_inst, ex_tb)

            if issubclass(ex_type, AssertionError):
                # The convention for test failures that all tests should throw
                # an AssertionError derived exception for failure conditions.
                # This is important because a failure condition implies an expectation
                # was checked and not met which implies a product code related failure
                
                self._result.add_failure(ex_lines)
            else:
                self._result.add_error(ex_lines)

            errmsg = "Exception raises setting up scope='{}'".format(self._test_name)
            logger.error(errmsg)

            handled = True
        else:
            self._result.mark_passed()

        self._result.finalize()
        self._recorder.record(self._result)
        self._sequencer.scope_id_pop(self._test_name)

        logger.info("TEST SCOPE EXIT: {}, {}".format(self._test_name, self._scope_id))

        return handled


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
        self._integrations = {}
        self._references = []
        self._scopes = {}
        self._scope_roots = []
        self._import_errors = []
        self._testtree = None
        self._landscape = None
        self._sequence_document = None
        self._recorder = None
        self._root_result = None
        self._scope_stack = []
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

    def enter_module_scope_context(self, scope_name, **kwargs):
        context = SequencerModuleScope(self, self._recorder, scope_name)
        return context

    def enter_session_scope_context(self):
        context = SequencerSessionScope(self, self._recorder, self._root_result)
        return context

    def enter_test_scope_context(self, scope_name, **kwargs):
        context = SequencerTestScope(self, self._recorder, scope_name, **kwargs)
        return context

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

    def execute_tests(self, runid: str, recorder):
        """
            Called in order to execute the tests contained in the :class:`TestPacks` being run.
        """
        exit_code = 0

        res_name = "<session>"

        self._recorder = recorder

        self._root_result = ResultContainer(runid, res_name, ResultType.JOB)
        recorder.record(self._root_result)

        if self._sequence_document is None:
            errmsg = "The 'execute_tests' method should not be called without first generating the test sequence document."
            raise AKitSemanticError(errmsg)

        # Import the test sequence document
        sequence_mod = import_file("sequence_document", self._sequence_document)
        sequence_mod.session(self)

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

        self._sequence_document = outputfilename

        return

    def scope_id_create(self, scope_name):

        parent_id = None
        if len(self._scope_stack) > 0:
            parent_id = self._scope_stack[-1][1]

        scope_id = str(uuid.uuid4())
        self._scope_stack.append((scope_name, scope_id))

        return parent_id, scope_id

    def scope_id_pop(self, scope_name):

        top_entry_name, _ = self._scope_stack.pop()
        if top_entry_name != scope_name:
            errmsg = "Attempting to pop '{}' from the scope stack but encountered '{}'.".format(scope_name, top_entry_name)
            raise AKitRuntimeError(errmsg)

        return

    def scope_id_push(self, scope_name, scope_id):
        self._scope_stack.append((scope_name, scope_id))
        return

    def _generate_session_method(self, outf, root_node, indent_space):
        """
            Generates the :function:`session` entry point function or the test run
            sequence document.
        """
        env = self.context.lookup("/environment")

        debugger = env["debugger"]
        breakpoint = env["breakpoint"]

        scopes_called = []

        current_indent = indent_space

        method_lines = [
            'def session(sequencer):',
            '{}"""'.format(current_indent),
            '{}This is the entry point for the test run sequence document.'.format(indent_space),
            '{}"""'.format(current_indent)
        ]

        if breakpoint == "testrun-start":
            if debugger == TEST_DEBUGGER.PDB:
                method_lines.append('')
                method_lines.append('{}# The debug flag was passed on the commandline so we break here.'.format(current_indent))
                method_lines.append('{}import pdb'.format(current_indent))
                method_lines.append('{}pdb.set_trace()'.format(current_indent))
            elif debugger == TEST_DEBUGGER.DEBUGPY:
                method_lines.append('')
                method_lines.append('{}# The remote debug flag was passed on the commandline so we break here.'.format(current_indent))
                method_lines.append('{}import debugpy'.format(current_indent))
                method_lines.append('{}debugpy.listen(56789)'.format(current_indent))

                logger.info("Waiting for debugger on port=56789")

                method_lines.append('{}debugpy.wait_for_client()'.format(current_indent))
                method_lines.append('{}debugpy.breakpoint()'.format(current_indent))

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
                pre_test_scope_indent = current_indent

                # Generate a test run scope for this test
                test_scope_name = child_node.test_name
                test_scope = resource_registry.lookup_resource_scope(test_scope_name)
                if test_scope is None:
                    errmsg = "There was no test scope associated with scope '{}'".format(test_scope_name)
                    raise AKitSemanticError(errmsg)

                method_lines.append('{}with sequencer.enter_test_scope_context("{}") as tsc:'.format(current_indent, test_scope_name))
                current_indent += indent_space

                test_args = []
                test_local_args = []
                for param_name, param_obj in test_scope.parameters.items():
                    test_args.append(param_name)
                    if param_obj.assigned_scope == test_scope_name:
                        test_local_args.append((param_name, param_obj))
                
                if len(test_local_args) > 0:
                    # Import any factory functions that are used in test local factory methods
                    for param_name, param_obj in test_local_args:
                        fmodname = param_obj.source_module_name
                        ffuncname = param_obj.source_function_name
                        method_lines.append("{}from {} import {}".format(current_indent, fmodname, ffuncname))
                    method_lines.append('')

                    # Generate any local parameters
                    for param_name, param_obj in test_local_args:
                        ffuncname = param_obj.source_function_name
                        ffuncsig = param_obj.source_signature
                        ffuncargs = [pn for pn in ffuncsig.parameters]
                        ffuncargs_str = " ,".join(ffuncargs)
                        method_lines.append("{}for {} in {}({}):".format(current_indent, param_name, ffuncname, ffuncargs_str))
                        current_indent += indent_space

                # Import the test function
                method_lines.append("{}from {} import {}".format(current_indent, child_node.test_module_name, child_node.test_base_name))

                # Make the call to the test function
                test_args = []
                for param_name in child_node.subscriptions:
                    test_args.append(param_name)
                call_line = '{}{}({})'.format(current_indent, child_node.test_base_name, ", ".join(test_args))
                method_lines.append(call_line)
                method_lines.append('')

                # Restor the indent to before the test scope
                current_indent = pre_test_scope_indent
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
