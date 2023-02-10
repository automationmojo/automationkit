
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

from typing import Any, List, OrderedDict, Sequence, Tuple

import collections
import json
import os
import sys
import uuid

from akit.environment.context import ContextUser
from akit.exceptions import AKitRuntimeError, AKitSemanticError, AKitSkipError
from akit.exceptions import format_exception
from akit.xlogging.foundations import getAutomatonKitLogger
from akit.xconfiguration import DiagnosticLabel, RuntimeConfigPaths

from akit.jsos import CHAR_RECORD_SEPERATOR
from akit.paths import get_path_for_diagnostics, get_path_for_output
from akit.results import ResultCode, ResultContainer, ResultNode, ResultType
from akit.compat import import_file
from akit.recorders import ResultRecorder

from akit.testing.testplus.testcollector import TestCollector
from akit.testing.testplus.registration.resourceregistry import resource_registry
from akit.testing.testplus.testgroup import TestGroup
from akit.testing.testplus.testref import TestRef
from akit.testing.testplus.markers import MetaFilter

from akit.timemachine import WELLKNOWN_PORTALS, timemachine_timeportal_code_append
from akit.xdebugger import WELLKNOWN_BREAKPOINTS, debugger_wellknown_breakpoint_code_append

logger = getAutomatonKitLogger()

TEMPLATE_TESTRUN_SEQUENCE_MODULE = '''"""
    ======================================= CODE GENERATED - DO NOT EDIT =======================================
    This is a code generated execution sequence document, do not manually edit this document.  The 'testplus'
    test framework generates this document in order to layout the test run scopes, parameter creations, and
    test calls in a user ledgible way which is easy to read and also to debug.
"""

__traceback_format_policy__ = "Brief"

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

class SequencerScopeBase:

    def __init__(self, sequencer: "TestSequencer", recorder: ResultRecorder):
        super().__init__()

        self._sequencer = sequencer
        self._recorder = recorder
        return

    def _mark_descendants_as_error(self, cursor, cursor_id, errmsg):

        for chkey in cursor.children:
            child = cursor.children[chkey]
            if not child.finalized:
                if isinstance(child, TestRef):
                    self._mark_test_as_error(child, cursor_id, errmsg)
                elif isinstance(child, TestGroup):
                    scope_id = str(uuid.uuid4())
                    scope_name = child.scope_name
                    result = self._sequencer.create_test_result_container(scope_id, scope_name, parent_inst=cursor_id)
                    self._recorder.record(result)
                    self._mark_descendants_as_error(child, scope_id, errmsg)

        return

    def _mark_descendants_skipped(self, cursor, cursor_id, reason, bug):

        for chkey in cursor.children:
            child = cursor.children[chkey]
            if not child.finalized:
                if isinstance(child, TestRef):
                    self._mark_test_as_skip(child, cursor_id, reason, bug)
                elif isinstance(child, TestGroup):
                    scope_id = str(uuid.uuid4())
                    scope_name = child.scope_name
                    result = self._sequencer.create_test_result_container(scope_id, scope_name, parent_inst=cursor_id)
                    self._recorder.record(result)
                    self._mark_descendants_skipped(child, scope_id, reason, bug)

        return

    def _mark_test_as_error(self, testref: TestRef, parent_id: str, errmsg: str):
        test_id = str(uuid.uuid4())
        result = self._sequencer.create_test_result_node(test_id, testref.test_name, testref.monikers, testref.pivots, parent_inst=parent_id)
        result.add_error(errmsg)
        result.finalize()
        self._recorder.record(result)
        return

    def _mark_test_as_skip(self, testref: TestRef, parent_id: str, reason: str, bug: str):
        test_id = str(uuid.uuid4())
        result = self._sequencer.create_test_result_node(test_id, testref.test_name, testref.monikers, testref.pivots, parent_inst=parent_id)
        result.mark_skip(reason, bug)
        result.finalize()
        self._recorder.record(result)
        return

class SequencerModuleScope(SequencerScopeBase):
    def __init__(self, sequencer: "TestSequencer", recorder: ResultRecorder, scope_name: str, **kwargs):
        super().__init__(sequencer, recorder)

        self._scope_name = scope_name
        self._scope_args = kwargs
        self._scope_id = None
        self._parent_scope_id = None
        self._scope_node = self._sequencer.find_treenode_for_scope(scope_name)
        return

    def __enter__(self):
        self._parent_scope_id, self._scope_id = self._sequencer.scope_id_create(self._scope_name)
        result = self._sequencer.create_test_result_container(self._scope_id, self._scope_name, parent_inst=self._parent_scope_id)
        self._recorder.record(result)
        logger.info("MODULE ENTER: {}, {}".format(self._scope_name, self._scope_id))
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        handled = False

        if ex_type is not None:

            if issubclass(ex_type, AKitSkipError):
                self._mark_descendants_skipped(self._scope_node, self._scope_id, ex_inst.reason, ex_inst.bug)
            else:
                errmsg = ""
                self._mark_descendants_as_error(self._scope_node,  self._scope_id, errmsg)

            # If an exceptions was thrown in this context, it means
            # that the exception occured during the setup for this
            # module, this means we need to mark all descendant tests
            # as error'd due to a setup failure.
            errmsg = "Exception raises setting up scope='{}'".format(self._scope_name)
            logger.exception(errmsg)
            handled = True

        self._scope_node.finalize()
        self._sequencer.scope_id_pop(self._scope_name)
        logger.info("MODULE EXIT: {}, {}".format(self._scope_name, self._scope_id))
        return handled

    

class SequencerSessionScope(SequencerScopeBase):
    def __init__(self, sequencer: "TestSequencer", recorder: ResultRecorder, root_result:ResultContainer):
        super().__init__(sequencer, recorder)
        
        self._scope_name = root_result.name
        self._scope_id = root_result.inst_id
        self._root_result = root_result
        self._scope_node = self._sequencer.testtree
        return

    def __enter__(self):
        self._sequencer.scope_id_push(self._scope_name, self._scope_id)
        logger.info("SESSION ENTER: {}".format(self._scope_id))
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        handled = False

        if ex_type is not None:

            if issubclass(ex_type, AKitSkipError):
                self._mark_descendants_skipped(self._scope_node, self._scope_id, ex_inst.reason, ex_inst.bug)
            else:
                errmsg = ""
                self._mark_descendants_as_error(self._scope_node,  self._scope_id, errmsg)

            # If an exceptions was thrown in this context, it means
            # that the exception occured during the setup for this
            # module, this means we need to mark all descendant tests
            # as error'd due to a setup failure.
            errmsg = "Exception raises setting up scope='{}'".format(self._scope_name)
            logger.exception(errmsg)
            handled = True

        self._scope_node.finalize()
        self._sequencer.scope_id_pop(self._scope_name)
        logger.info("SESSION EXIT: {}".format(self._scope_id))
        return handled

class SequencerTestScope:
    def __init__(self, sequencer: "TestSequencer", recorder: ResultRecorder, test_name: str, parameterized: OrderedDict[str, Any]={}):
        super().__init__()

        self._sequencer = sequencer
        self._recorder = recorder
        self._test_name = test_name
        self._scope_id = None
        self._parent_scope_id = None
        self._result = None
        self._scope_node = self._sequencer.find_treenode_for_scope(test_name)
        self._parameterized = parameterized
        self._monikers, self._pivots = self._get_monikers_and_pivots()
        self._context_identifier = "{}:{}".format(self._test_name, ",".join(self._monikers))
        return

    def _get_monikers_and_pivots(self) -> Tuple[List[str], OrderedDict[str, Any]]:
        """
            Creates a full context identifier based on the full testname and the identifiers of any
            parameterized parameters that are being passed to the test.
        """
        
        monikers = []
        pivots = collections.OrderedDict()

        if len(self._parameterized) > 0:

            for pname, pobj in self._parameterized.items():
                
                if hasattr(pobj, "moniker"):
                    monikers.append(pobj.moniker)
                else:
                    monikers.append(str(pobj))
                
                if hasattr(pobj, "pivots"):
                    pivots[pname] = pobj.pivots
                else:
                    pivots[pname] = str(pobj)

        return monikers, pivots

    def __enter__(self):
        self._parent_scope_id, self._scope_id = self._sequencer.scope_id_create(self._context_identifier)
        logger.info("TEST SCOPE ENTER: {}, {}".format(self._context_identifier, self._scope_id))
        self._result = self._sequencer.create_test_result_node(self._scope_id, self._test_name, self._monikers, self._pivots, parent_inst=self._parent_scope_id)
        self._test_scope_enter()
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        handled = True

        if ex_type is not None:
            
            # If an exceptions was thrown in this context, it means
            # that a test threw an exception.
            ex_lines = format_exception(ex_inst)

            if issubclass(ex_type, AKitSkipError):
                self._result.mark_skip(ex_inst.reason, ex_inst.bug)
            elif issubclass(ex_type, AssertionError):
                # The convention for test failures that all tests should throw
                # an AssertionError derived exception for failure conditions.
                # This is important because a failure condition implies an expectation
                # was checked and not met which implies a product code related failure
                
                self._result.add_failure(ex_lines)
            else:
                self._result.add_error(ex_lines)

            errmsg_lines = [
                "Exception raises setting up scope='{}'".format(self._test_name)
            ]
            for exln in ex_lines:
                errmsg_lines.append(exln.rstrip())

            errmsg = os.linesep.join(errmsg_lines)
            logger.error(errmsg)

            handled = True
        else:
            self._result.mark_passed()

        # Call test scope exit before we finalize our results
        self._test_scope_exit()

        self._result.finalize()
        self._recorder.record(self._result)

        self._scope_node.finalize()
        self._sequencer.scope_id_pop(self._context_identifier)

        logger.info("TEST SCOPE EXIT: {}, {}".format(self._context_identifier, self._scope_id))

        return handled

    def _test_scope_enter(self):
        return
    
    def _test_scope_exit(self):
        return

class SequencerTestSetupScope:
    def __init__(self, sequencer, recorder, test_name, **kwargs):
        super().__init__()

        self._sequencer = sequencer
        self._recorder = recorder
        self._test_name = test_name
        self._scope_name = "setup:{}".format(test_name)
        self._scope_args = kwargs
        self._scope_id = None
        self._parent_scope_id = None
        self._test_scope_node = self._sequencer.find_treenode_for_scope(test_name)
        return

    def __enter__(self):
        self._parent_scope_id, self._scope_id = self._sequencer.scope_id_create(self._scope_name)
        logger.info("TEST SETUP ENTER: {}, {}".format(self._scope_name, self._scope_id))
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

        self._test_scope_node.finalize()
        self._sequencer.scope_id_pop(self._scope_name)
        logger.info("TEST SETUP EXIT: {}, {}".format(self._scope_name, self._scope_id))
        return handled

class TestSequencer(ContextUser):
    """
        The :class:`TestSequencer` is a state machine that helps to orchestrate the flow fo the test run.  It ensures
        that the steps of the test flow are consistent between runs.
    """

    def __init__(self, jobtitle: str, root: str, includes: Sequence[str], excludes: Sequence[str], metafilters: List[MetaFilter]):
        """
            Creates a 'TestSequencer' object which is used to discover the tests and control the flow of a test run.

            :param jobtitle: The name of the test job.
            :param root: The path to the root folder that is the base of the tests.
            :param includes: List of expressions used to determine which tests to include.
                             (scope):(package).(package)@(module)#(testname)
            :param excludes: List of expressions used to determine which tests to exclued from the included tests.
            :param metafilters: List of expressions used to filter tests by metadata
        """
        super().__init__()

        self._jobtitle = jobtitle
        self._root = root
        self._includes = includes
        self._excludes = excludes
        self._metafilters = metafilters
        self._integrations = {}
        self._references = []
        self._scopes = {}
        self._scope_roots = []
        self._import_errors = {}
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

        environment_dict = self.create_password_masked_environment()

        package_dict = collections.OrderedDict()

        package_names = [k for k in sys.modules.keys()]
        package_names.sort()
        for pname in package_names:
            nxtmod = sys.modules[pname]
            if pname.find(".") == -1 and hasattr(nxtmod, "__file__"):
                package_dict[pname] = nxtmod.__file__

        startup_dict = collections.OrderedDict([
            ("command", " ".join(sys.argv)),
            ("environment", environment_dict),
            ("packages", package_dict)
        ])

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

    def create_job_result_container(self, scope_id: str, scope_name: str) -> ResultContainer:
        """
            Method for creating a result container.
        """
        rcontainer = ResultContainer(scope_id, scope_name, ResultType.JOB, parent_inst=None)
        return rcontainer

    def create_password_masked_environment(self):
        """
            Creates copy of the environment for writing to a file with the passwords masked.
        """
        environment_dict = collections.OrderedDict()

        env_keys = [k for k in os.environ.keys()]
        env_keys.sort()
        for ek in env_keys:
            environment_dict[ek] = os.environ[ek]

        for key in environment_dict.keys():
            if key.find("PASSWORD") > -1:
                environment_dict[key] = "(hidden)"
        
        return environment_dict

    def create_test_result_container(self, scope_id: str, scope_name: str, parent_inst: str) -> ResultContainer:
        """
            Method for creating a result container.
        """
        rcontainer = ResultContainer(scope_id, scope_name, ResultType.TEST_CONTAINER, parent_inst=parent_inst)
        return rcontainer
    
    def create_test_result_node(self, scope_id: str, name: str, monikers: List[str], pivots: OrderedDict[str, Any], parent_inst: str) -> ResultNode:
        """
            Method for creating a result node.
        """
        rnode = ResultNode(scope_id, name, monikers, pivots, ResultType.TEST, parent_inst=parent_inst)
        return rnode

    def diagnostic_capture_pre_testrun(self, level: int=9):
        """
            Perform a pre-run diagnostic on the devices in the test landscape.
        """

        prerun_info = self.context.lookup(RuntimeConfigPaths.DIAGNOSTIC_PRERUN)

        if prerun_info is not None:
            label = DiagnosticLabel.PRERUN_DIAGNOSTIC
            diagnostic_root = get_path_for_diagnostics(label)

            for _, integ_type in self._integrations.items():
                integ_type.diagnostic(label, level, diagnostic_root)

        return

    def diagnostic_capture_post_testrun(self, level: int=9):
        """
            Perform a post-run diagnostic on the devices in the test landscape.
        """
        postrun_info = self.context.lookup(RuntimeConfigPaths.DIAGNOSTIC_POSTRUN)

        if postrun_info is not None:

            label = DiagnosticLabel.POSTRUN_DIAGNOSTIC
            diagnostic_root = get_path_for_diagnostics(label)

            for _, integ_type in self._integrations.items():
                integ_type.diagnostic(label, level, diagnostic_root)

        return

    def discover(self, test_module=None, include_integrations: bool=True):
        """
            Initiates the discovery phase of the test run.
        """
        collector = TestCollector(self._root, excludes=self._excludes, metafilters=self._metafilters, test_module=test_module)

        # Discover the tests, integration points, and scopes.  If test modules is not None then
        # we are running tests from an individual module and we can limit discovery to the test module
        for inc_item in self._includes:
            collector.collect_references(inc_item)

        collector.finalize_collection()

        self._testtree = collector.test_tree
        self._references = collector.references

        testcount = len(self._references)
        if testcount > 0:
            if include_integrations:
                self._integrations, self._scopes = collector.collect_integrations_and_scopes()
            self._import_errors = collector.import_errors

        return testcount

    def enter_module_scope_context(self, scope_name):
        context = SequencerModuleScope(self, self._recorder, scope_name)
        return context

    def enter_session_scope_context(self):
        context = SequencerSessionScope(self, self._recorder, self._root_result)
        return context

    def enter_test_scope_context(self, test_name, parameterized: Sequence=[]):
        context = SequencerTestScope(self, self._recorder, test_name, parameterized=parameterized)
        return context

    def enter_test_setup_context(self, test_name):
        context = SequencerTestSetupScope(self, self._recorder, test_name)
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

        res_name = "<session>"

        self._recorder = recorder

        self._root_result = self.create_job_result_container(runid, res_name)
        recorder.record(self._root_result)

        if self._sequence_document is None:
            errmsg = "The 'execute_tests' method should not be called without first generating the test sequence document."
            raise AKitSemanticError(errmsg) from None

        # Import the test sequence document
        sequence_mod = import_file("sequence_document", self._sequence_document)
        sequence_mod.session(self)

        return

    def expand_test_tree_based_on_query(self):

        context_locals = {}

        # Walk the test tree and expand the parameters
        # self._testtree

        return

    def find_treenode_for_scope(self, scope_name, cursor=None):
        found = None

        if cursor is None:
            cursor = self._testtree

        if cursor.scope_name == scope_name:
            found = cursor
        elif isinstance(cursor, TestGroup):
            for child in cursor.children.values():
                found = self.find_treenode_for_scope(scope_name, cursor=child)
                if found is not None:
                    break

        return found

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
            raise AKitRuntimeError(errmsg) from None

        return

    def scope_id_push(self, scope_name, scope_id):
        self._scope_stack.append((scope_name, scope_id))
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

        debugger_wellknown_breakpoint_code_append(WELLKNOWN_BREAKPOINTS.TESTRUN_START, method_lines, current_indent)

        current_indent += timemachine_timeportal_code_append(WELLKNOWN_PORTALS.TESTRUN_START, method_lines, current_indent)

        method_lines.append('')
        method_lines.append('{}with sequencer.enter_session_scope_context() as ssc:'.format(current_indent))
        method_lines.append('')

        current_indent = current_indent + indent_space

        this_scope = root_node.get_resource_scope()

        # Import all the parameter source functions
        for _, porigin in this_scope.parameter_originations.items():
            method_lines.append('{}from {} import {}'.format(current_indent, porigin.source_module_name, porigin.source_function.__name__))
        method_lines.append('')

        # Create the calls to all of the root test scopes
        child_call_args = ['sequencer']

        # Create the variables with session scope
        for pname, porigin in this_scope.parameter_originations.items():
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

        # Create the calls to all of the root test scopes
        child_call_args = [arg for arg in scope_call_args]

        resource_scope = scope_node.get_resource_scope()

        # Import all the parameter source functions
        for _, porigin in resource_scope.parameter_originations.items():
            method_lines.append('{}from {} import {}'.format(current_indent, porigin.source_module_name, porigin.source_function.__name__))
        method_lines.append('')

        # Create the variables with session scope
        for pname, porigin in resource_scope.parameter_originations.items():

            sp_parameter_names = [pn for pn in porigin.source_signature.parameters.keys()]
            if 'constraints' in sp_parameter_names:
                constraints = {}
                if porigin.constraints is not None:
                    constraints = porigin.constraints
                method_lines.append('{}constraints={}'.format(current_indent, repr(constraints)))
            
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

                test_parameters = child_node.test_function_parameters

                test_local_args = []

                for param_name in test_parameters:
                    # If the test parameter is of test_scope origin
                    # then we need to add it to test_local_args so we
                    # can create an import for it.
                    if param_name in test_scope.parameter_originations:
                        param_obj = test_scope.parameter_originations[param_name]
                        test_local_args.append((param_name, param_obj))

                parameterized_args = ""

                method_lines.append("{}# ================ Test Scope: {} ================".format(current_indent, test_scope_name))
                method_lines.append('')
                # Import the test function and assign the test name
                method_lines.append("{}from {} import {}".format(current_indent, child_node.test_module_name, child_node.test_base_name))
                method_lines.append('{}test_scope_name = "{}"'.format(current_indent, test_scope_name))
                method_lines.append('')

                if len(test_local_args) > 0:
                    method_lines.append('{}with sequencer.enter_test_setup_context(test_scope_name) as tsetup:'.format(current_indent))
                    current_indent += indent_space

                    parameterized_args_names = []

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
                        if 'constraints' in ffuncargs:
                            constraints = {}
                            if param_obj.constraints is not None:
                                constraints = param_obj.constraints
                            method_lines.append('{}constraints={}'.format(current_indent, repr(constraints)))
                        ffuncargs_str = " ,".join(ffuncargs)
                        method_lines.append("{}for {} in {}({}):".format(current_indent, param_name, ffuncname, ffuncargs_str))
                        parameterized_args_names.append(param_name)
                        current_indent += indent_space
                
                    parameterized_args = ", ".join(map(lambda arg: "'{}': {}".format(arg, arg), parameterized_args_names))
                    if len(parameterized_args_names) == 1:
                        parameterized_args += ","

                    parameterized_args = ", parameterized={%s}" % (parameterized_args)

                    method_lines.append('')

                method_lines.append('{}with sequencer.enter_test_scope_context(test_scope_name{}) as tsc:'.format(current_indent, parameterized_args))
                current_indent += indent_space

                # Make the call to the test function
                test_args = []
                for param_name in test_parameters:
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
