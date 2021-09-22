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

from typing import List, Sequence, Tuple
from types import ModuleType

import fnmatch
import inspect
import os
import sys
import traceback

from akit.compat import import_file

from akit.coupling.integrationcoupling import is_integration_coupling
from akit.testing.unittest.scopecoupling import is_iteration_scope_coupling

from akit.paths import collect_python_modules

from akit.testing.expressions import parse_test_include_expression
from akit.testing.utilities import find_included_modules_under_root
from akit.testing.unittest.queries import collect_test_references, collect_testpacks
from akit.testing.unittest.testcontainer import TestContainer, inherits_from_testcontainer
from akit.testing.unittest.testpack import testpack_compare
from akit.testing.unittest.testref import TestRef

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

    def __init__(self, root: str, excludes: Sequence[str], method_prefix: str = "test", test_module: ModuleType = None):
        """
            Initializes a :class:`TestCollector` instance in order to process the test tree and
            collect references and test packages to be run.

            :param root: The root directory to scan for included tests
            :param excludes: A list or sequence of exclude expressions to apply during test collection operations.
            :param module_prefix: The prefix or word that test methods will start with.  The default is 'test'.
            :param test_module: A test module which is passed for the debug workflow where a test module is run directly
                                as a script using the generic_test_entrypoint or in the debugger by Right-Click

        """
        self._root = root
        self._root_directory_listing = None
        self._excludes = excludes
        self._method_prefix = method_prefix
        self._test_module = test_module
        self._test_references = {}
        self._test_packages = {}
        self._import_errors = {}
        self._excluded_testpacks = []
        self._excluded_tests = []
        self._excluded_files = []
        self._excluded_path_prefixes, self._excluded_specifically = catagorize_exclusions(self._excludes)
        return

    @property
    def import_errors(self):
        """
            A list of import errors that were encountered while collecting test references.
        """
        return self._import_errors

    @property
    def references(self):
        """
            A list of :class:`TestReferences` that were collected.
        """
        return self._test_references

    @property
    def test_packages(self):
        """
            A list of :class:`TestPackage` objects that were collected.
        """
        return self._test_packages

    def collect_integrations(self):
        """
            Iterates through all of the test references and collects the IntegrationCoupling(s) that
            are found.
        """

        integrations = {}
        for _, ref in self._test_references.items():
            for bcls in ref.testcontainer.__bases__:
                if is_integration_coupling(bcls):
                    mikey = bcls.__module__ + "." + bcls.__name__
                    if mikey in integrations:
                        integrations[mikey][1].append(ref)
                    else:
                        integrations[mikey] = (bcls, [ref])

        integlist = [ i for i in integrations.values()]

        return integlist

    def collect_references(self, expression: str):
        """
            Collects and appends the test references based on the expression provided and the excludes
            for this class.  The `collect_references` method is intended to be called multiple times,
            once with each include expression provided by the users.  The :class:`TestCollector` will
            extend its collection of reference with each successive call.

            :param expression: An include expression to process and collect references for.
        """

        expr_package, expr_module, expr_testclass, expr_testname = parse_test_include_expression(expression, self._test_module, self._method_prefix)

        # Find all the files that are included based on the expr_package, expr_module expressions
        included_files = []

        if self._test_module is not None:
            test_module_basename, _ = os.path.splitext(self._test_module.__file__)
            included_files.append(test_module_basename + ".py")
        elif expr_package is not None or expr_module is not None:
            included_files, excluded_files = find_included_modules_under_root(self._root,
                expr_package, expr_module, excluded_path_prefixes=self._excluded_path_prefixes)

        self._excluded_files.extend(excluded_files)

        test_references, testpack_references, import_errors = collect_test_references(
            self._root, included_files, expr_package, expr_module, expr_testclass, expr_testname, self._method_prefix)

        self._test_references.update(test_references)
        self._test_packages.update(testpack_references)

        self._import_errors.update(import_errors)

        for modname, ifile, errmsg in import_errors.values():
            logger.error("TestCase: Import error filename=%r" % ifile)

        return

    def collect_testpacks(self):
        """
            Goes through all of the test references and collects a list of the :class:`TestPack` types that are
            included in the collection of test references.  The :class:`TestPack` collection can be used to
            determine analyze the integrations and scopes that are associated with the collected test references.
        """
        # The testpack_table is filled with the top-level testpack types which
        # also are the top level scopes associated with an object.
        testpack_table = collect_testpacks(self._test_references)

        self._test_packages.update(testpack_table)

        # We need to go through all of the testpacks and walk the class hierarchy of each
        # and as we find a scope derived type, we need to add that type into a table based
        # on its level in the class hierarcy.  The testpack type ensures we have one reference
        # into the type hierarchy at level 0. We will be executing the scopes starting with
        # level 0 and moving up based on usage.

        # As we walk the tree we increment each scopes usage counter. When a scope exits, we can
        # decrement its reference count.  We will walk the full scope hierarchy as we run
        # the tests associated with each testpack, however, we only execute the enter code
        # when the scope is entered for the first time and we only execute the exit code when
        # the last reference count is removed.
        for _, nxt_tpack_val in self._test_packages.items():

            # The tope TestPack will always have a reference count of 1
            nxt_tpack_val.refcount = 1

            # Preset the level to 0 and weight to 1
            level = 0
            weight = 1

            found_at_level = [nxt_tpack_val]
            while True:
                search_scopes = found_at_level
                level += 1
                found_at_level = []
                for nxt_scope in search_scopes:
                    found_scopes = self._record_child_scopes_at_level(nxt_scope, level)
                    found_at_level.extend(found_scopes)
                    for fscope in found_scopes:
                        weight += ((fscope.refcount) * (level + 1))

                if len(found_at_level) == 0:
                    break

            # The weight of the TestPack is a combination of how deep the levels of scopes are under
            # the TestPack and the number of scopes.  We try to optimize the ordering of running
            # the TestPack(s) by weight
            nxt_tpack_val.weight = weight

        # Sort the testpack table by weight
        testpacks = [ v for v in self._test_packages.values()]
        testpacks.sort(key=testpack_compare, reverse=True)

        return testpacks

    def expand_testpacks(self):
        """
            The includes and excludes passed to the :class:`TestCollector` can also be used to find :class:`TestPack`(s).
            When an include specification includes a :class:`TestPack`, all the tests that are associated with that
            :class:`TestPack` are included in the test run.  They `expand_testpacks` method goes through all of the
            :class:`TestPack`(s), collect test references for all of the tests and then adds the test references to
            the list of included tests.
        """

        self._excluded_testpacks = []

        if self._excluded_specifically is not None:
            # Go through all of the exclude expressions and utilize them to mark the TestPack objects that
            # should be excluded from the test run
            for ex_expr in self._excluded_specifically:
                for tpack_name, tpack_obj in self._test_packages.items():
                    if tpack_name.startswith(ex_expr):
                        self._excluded_testpacks.append(tpack_name)

        # Go through all the excluded test packs and then remove them from the test packs catalog
        # by name
        for tpack_name in self._excluded_testpacks:
            del self._test_packages[tpack_name]

        # Go through all of the test package references and load the tests that are associated with the
        # test package
        import_errors = {}

        for tpack_name, tpack_obj in self._test_packages.items():
            searchin = tpack_obj.searchin
            if searchin is None:
                # If searchin was None, then we scan utilize the descendant directories of root
                searchin = [ dir for dir in self._directories_in_root() if not dir.endswith("__pycache__") ]

            scanfiles = []
            for sdir in searchin:
                scanfiles = collect_python_modules(sdir, max_depth=0)

                rootlen = len(self._root)
                for ifile in scanfiles:
                    _, fext = os.path.splitext(ifile)
                    if fext == ".py":
                        ifile_full = os.path.join(sdir, ifile)
                        if ifile_full not in import_errors:

                            modname = None
                            try:
                                ifilebase, _ = os.path.splitext(ifile_full)
                                ifileleaf = ifilebase[rootlen:].strip("/")
                                modname = ifileleaf.replace("/", ".")
                                mod = import_file(modname, ifile_full)

                                test_class_coll = inspect.getmembers(mod, inherits_from_testcontainer)
                                for _, testclass_obj in test_class_coll:
                                    test_class_name = testclass_obj.__module__ + "@" + testclass_obj.__name__
                                    if issubclass(testclass_obj, TestContainer) and issubclass(testclass_obj, tpack_obj):
                                        # If we don't have a testname expression then add all the test test methods for the class
                                        test_method_coll = inspect.getmembers(testclass_obj, inspect.isfunction)
                                        for method_name, method_obj in test_method_coll:
                                            if method_name.startswith(self._method_prefix):
                                                tname = test_class_name + "#" + method_name
                                                tref = TestRef(testclass_obj, method_obj)
                                                self._test_references[tname] = tref

                            except ImportError as imp_error:
                                errmsg = traceback.format_exc()
                                import_errors[ifile_full] = (modname, ifile, errmsg)

        self._excluded_tests = []
        if self._excluded_specifically is not None:
            # Go back through all of the exclude expressions and see if any of the excludes
            # apply to the test references directly
            for ex_expr in self._excluded_specifically:
                for test_name, test_reference in self._test_references.items():
                    if test_name.startswith(ex_expr):
                        self._excluded_tests.append((test_name, test_reference))

        # Go through all the excluded tests and then remove them from the test references catalog
        # by name
        for test_name, test_reference in self._excluded_tests:
            del self._test_references[test_name]
            if test_reference.testpack is not None:
                tpack = test_reference.testpack
                if test_name in tpack.test_references:
                    del tpack.test_references[test_name]

        # Go through all the testpacks an determine which ones need to be removed due to not having
        # any applicable tests to run.
        remove_testpacks = []
        for tpack_key, tpack_obj in self._test_packages.items():
            if tpack_obj.test_references is None or len(tpack_obj.test_references) == 0:
                remove_testpacks.append(tpack_key)

        for tpack_key in remove_testpacks:
            del self._test_packages[tpack_key]

        self._import_errors.update(import_errors)

        for modname, ifile, errmsg in import_errors.values():
            logger.error("TestPack: Import error filename=%r" % ifile)

        return

    def _record_child_scopes_at_level(self, scope_cls, level): # pylint: disable=no-self-use
        """
            Records all the scopes found in the hierarchy of a class at the level specified.
        """

        scopes_found = []

        for nxt_cls in scope_cls.__bases__:
            if is_iteration_scope_coupling(nxt_cls):
                if not hasattr(nxt_cls, "refcount"):
                    setattr(nxt_cls, "refcount", 1)
                else:
                    nxt_cls.refcount += 1
                scopes_found.append(nxt_cls)

        return scopes_found

    def _directories_in_root(self):
        """
            Gets a list of all the directories in the root directory tree.
        """

        if self._root_directory_listing is None:
            self._root_directory_listing = []
            for root, _, _ in os.walk(self._root, topdown = False):
                self._root_directory_listing.append(root)

        return self._root_directory_listing
