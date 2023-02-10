"""
.. module:: testcollector
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the `TestCollector` object which is utilized to collection the
               information about the tests, scopes and integration that will be included in an
               automation run.

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

from typing import Dict, List, Sequence, Tuple, Union
from types import ModuleType

import fnmatch
import inspect
import os
import sys
import traceback

from akit.exceptions import AKitSemanticError, AKitUnknownParameterError
from akit.coupling.integrationcoupling import IntegrationCoupling, is_integration_coupling

from akit.testing.expressions import parse_test_include_expression
from akit.testing.utilities import find_included_modules_under_root
from akit.testing.testplus.queries import collect_test_references

from akit.testing.testplus.testgroup import TestGroup
from akit.testing.testplus.testref import TestRef
from akit.testing.testplus.registration.resourceregistry import resource_registry
from akit.testing.testplus.markers import MetaFilter

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

def catagorize_exclusions(excluded: str) -> Tuple[List[str], List[str]]:
    """
        Go through a list of exclusion expressions and divide them up by whether they are
        file based exclusions or an exclusion that targets python types or methods within
        a specific module.

        :param excluded: A list of exclusion expressions.

        :returns: A list of file exclusion expressions and a list of specific exclusions.
    """
    file_exclusions = []
    specific_exclusions = []

    if excluded is not None:
        for ex in excluded:
            if ex.find("@") < -1:
                path_prefix = ex.replace(".", os.sep)
                file_exclusions.append(path_prefix)
            else:
                specific_exclusions.append(ex)

    return file_exclusions, specific_exclusions

class TestCollector:
    """
        The :class:`TestCollector` object utilizes the include and exclude expressions along with any test_module
        provided to collect the information about the test references and the associated test packages that will
        be involved in test run.
    """

    def __init__(self, root: str, excludes: Sequence[str], metafilters: Sequence[MetaFilter], 
                 method_prefix: str = "test", test_module: ModuleType = None):
        """
            Initializes a :class:`TestCollector` instance in order to process the test tree and
            collect references and test packages to be run.

            :param root: The root directory to scan for included tests
            :param excludes: A list or sequence of exclude expressions to apply during test collection operations.
            :param metafilters: A list of metadata filters to apply during test collection operations.
            :param module_prefix: The prefix or word that test methods will start with.  The default is 'test'.
            :param test_module: A test module which is passed for the debug workflow where a test module is run directly
                                as a script using the generic_test_entrypoint or in the debugger by Right-Click

        """
        self._root = root
        self._root_directory_listing = None
        self._excludes = excludes
        self._metafilters = metafilters
        self._method_prefix = method_prefix
        self._test_module = test_module
        self._test_references: Dict[str, TestRef] = {}
        self._import_errors = {}
        self._excluded_tests = []
        self._excluded_files = []
        self._excluded_path_prefixes, self._excluded_specifically = catagorize_exclusions(self._excludes)
        self._test_tree = None
        return

    @property
    def import_errors(self):
        """
            A list of import errors that were encountered while collecting test references.
        """
        return self._import_errors

    @property
    def references(self) -> Dict[str, TestRef]:
        """
            A list of :class:`TestReferences` that were collected.
        """
        return self._test_references

    @property
    def test_tree(self) -> TestGroup:
        return self._test_tree

    def collect_integrations_and_scopes(self) -> List[IntegrationCoupling]:
        """
            Iterates through all of the test references and collects the IntegrationCoupling(s) and
            ScopeCouplings that are found.  The collected IntegrationCoupling(s) and ScopeCoupling(s) can
            be used by integrations and scopes to participate in test framework startup.
        """

        referenced_integrations = {}
        referenced_scopes = {}

        # All the implicit registration of all the integration, scope and resource parameters sources
        # should have happend by now.  The ResourceRegistry should have a partially populated scope
        # tree.
        resource_registry.finalize_startup(self._test_references)

        unknown_parameter = resource_registry.unknown_parameters

        if len(unknown_parameter) > 0:
            err_msg_lines = [
                "TestCollector: Unable to resolve the following parameters.",
                "Missing Parameters:"
            ]
            subscriber_key_list = [upn for upn in unknown_parameter.keys()]
            subscriber_key_list.sort()
            for subscriber in subscriber_key_list:
                missing_params = unknown_parameter[subscriber]
                err_msg_lines.append("    {}".format(subscriber))
                for mparam in missing_params:
                    err_msg_lines.append("        {}".format(mparam))
            err_msg = os.linesep.join(err_msg_lines)
            raise AKitUnknownParameterError(err_msg) from None

        referenced_integrations = resource_registry.referenced_integrations
        referenced_scopes = resource_registry.referenced_scopes

        return referenced_integrations, referenced_scopes

    def collect_references(self, expression: str):
        """
            Collects and appends the test references based on the expression provided and the excludes
            for this class.  The `collect_references` method is intended to be called multiple times,
            once with each include expression provided by the users.  The :class:`TestCollector` will
            extend its collection of reference with each successive call.

            :param expression: An include expression to process and collect references for.
        """

        expr_package, expr_module, expr_testclass, expr_testname = parse_test_include_expression(expression, self._test_module, self._method_prefix)

        if expr_testclass != None:
            raise AKitSemanticError("TestPlus style tests do not support tests inside of classes.") from None

        # Find all the files that are included based on the expr_package, expr_module expressions
        included_files = []
        excluded_files = []

        if expr_package is not None or expr_module is not None:
            included_files, excluded_files = find_included_modules_under_root(self._root,
                expr_package, expr_module, excluded_path_prefixes=self._excluded_path_prefixes)

        self._excluded_files.extend(excluded_files)

        test_references, import_errors = collect_test_references(
            self._root, included_files, expr_package, expr_module, expr_testname, self._method_prefix)

        self._test_references.update(test_references)

        self._import_errors.update(import_errors)

        for modname, ifile, errmsg in import_errors.values():
            logger.error("TestCase: Import error filename=%r" % ifile)

        return

    def finalize_collection(self):
        """
            Applies the metadata filters and then creates the test tree.
        """
        
        testref_key_list = [k for k in self._test_references.keys()]

        temp_tree = TestGroup("<session>")
        for _, trval in self._test_references.items():
            temp_tree.add_descendent(trval)

        # Go through all of the test references and have all of the them
        # resolve their metadata reference chains
        temp_tree.resolve_metadata()

        # Apply metafilters to remove any tests that don't meet any specified
        # meta criteria
        if self._metafilters is not None and len(self._metafilters) > 0:
            filtered_references = {}

            for tref_key in testref_key_list:
                tref_obj = self._test_references[tref_key]
                if tref_obj.is_member_of_metaset(self._metafilters):
                    filtered_references[tref_key] = tref_obj

            del self._test_references
            self._test_references = filtered_references

        self._test_tree = TestGroup("<session>")
        for _, trval in self._test_references.items():
            self._test_tree.add_descendent(trval)

        return