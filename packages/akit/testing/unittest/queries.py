
from typing import Union

import inspect
import os
import fnmatch
import traceback

from akit.compat import import_file
from akit.exceptions import AKitSemanticError

from akit.testing.unittest.testcontainer import inherits_from_testcontainer
from akit.testing.unittest.testpack import DefaultTestPack, inherits_from_testpack
from akit.testing.unittest.testref import TestRef

from akit.testing.utilities import create_testpack_key

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

def collect_test_references(root, included_files, filter_package, filter_module, filter_testclass, filter_testname, method_prefix):
    """
        Finds the test references based on the expression provided and the excludes
        for this class.  The `find_test_references` method is intended to be called
        multiple times, once with each include expression provided by the users.

        :param expression: An include expression to process and collect references for.
    """

    test_references = {}
    testpack_references = {}

    import_errors = {}

    root_pkgname = os.path.basename(root)

    # Go through the files and import them, then go through the classes and find the TestPack and
    # TestContainer objects that match the specified include expression criteria
    rootlen = len(root)
    for ifile in included_files:
        modname = None
        try:
            ifilebase, _ = os.path.splitext(ifile)
            ifileleaf = ifilebase[rootlen:].strip("/")
            modname = "{}.{}".format(root_pkgname, ifileleaf.replace("/", "."))

            # Import the module for the file being processed
            mod = import_file(modname, ifile)

            # Go through all of the members of the
            test_class_coll = inspect.getmembers(mod, inspect.isclass)
            for testclass_name, testclass_obj in test_class_coll:
                tcobj_module_name = testclass_obj.__module__
                # We only want to include the classes that are from the target module
                if tcobj_module_name != modname:
                    continue

                test_class_name = testclass_obj.__module__ + "@" + testclass_obj.__name__
                if filter_testclass is not None and not fnmatch.fnmatch(testclass_name, filter_testclass):
                    continue

                if inherits_from_testcontainer(testclass_obj):
                    if filter_testname is not None:
                        # We have a testname expression so go through all the test methods and and check
                        # the test method names
                        test_method_coll = inspect.getmembers(testclass_obj, inspect.isfunction)
                        for method_name, method_obj in test_method_coll:
                            if method_name.startswith(method_prefix):
                                if fnmatch.fnmatch(method_name, filter_testname):
                                    tname = test_class_name + "#" + method_name
                                    tref = TestRef(testclass_obj, method_obj)
                                    test_references[tname] = tref
                    else:
                        include_class = False
                        if filter_testclass is None:
                            include_class = True
                        else:
                            class_name = testclass_obj.__name__
                            if fnmatch.fnmatch(filter_testclass, class_name):
                                include_class = True

                        if include_class:
                            # If we don't have a testname expression then add all the test test methods for the class
                            test_method_coll = inspect.getmembers(testclass_obj, inspect.isfunction)
                            for method_name, method_obj in test_method_coll:
                                if method_name.startswith(method_prefix):
                                    tname = test_class_name + "#" + method_name
                                    tref = TestRef(testclass_obj, method_obj)
                                    test_references[tname] = tref

                elif inherits_from_testpack(testclass_obj):
                    # If we find a TestPack object that matches the criteria, look to see if the
                    # expression had a testname.  If it didn't we should save the TestPack reference
                    # in order to load the tests from the test pack.
                    if filter_testname is None:
                        if filter_testclass is None:
                            testpack_references[test_class_name] = testclass_obj
                        else:
                            class_name = testclass_obj.__name__
                            if fnmatch.fnmatch(filter_testclass, class_name):
                                testpack_references[test_class_name] = testclass_obj

        except ImportError:
            errmsg = traceback.format_exc()
            print(errmsg)
            import_errors[ifile] = (modname, ifile, errmsg)

    import_errors.update(import_errors)

    for modname, ifile, errmsg in import_errors.values():
        logger.error("TestCase: Import error filename=%r" % ifile)

    return test_references, testpack_references, import_errors

def collect_testpacks(test_references):
    """
        Goes through all of the test references and collects a list of the :class:`TestPack` types that are
        included in the collection of test references.  The :class:`TestPack` collection can be used to
        determine analyze the integrations and scopes that are associated with the collected test references.
    """
    # The testpack_table is filled with the top-level testpack types which
    # also are the top level scopes associated with an object.
    testpack_table = {}

    default_testpack_refs = []

    def_tp_key = create_testpack_key(DefaultTestPack)

    # Walk through all the test references. For each test reference, find its immediate testpack
    # or if it doesn't have one assign it to the default testpack
    for ref_key, ref in test_references.items():

        # Go through all the parent objects and add the current test ref to each of the scope
        # classes found in the main class
        ref_testpacks = []
        for bcls in ref.testcontainer.__bases__:
            if inherits_from_testpack(bcls):
                ref_testpacks.append(bcls)

        # If we didn't find a TestPack derived object, then
        # add this test reference to the DefaultTestPack
        ref_leaf_testpack_count = len(ref_testpacks)
        if ref_leaf_testpack_count == 0:
            ref.testpack = DefaultTestPack
            default_testpack_refs.append(ref)

        elif ref_leaf_testpack_count == 1:
            leaf_testpack_cls = ref_testpacks[0]
            ref.testpack = leaf_testpack_cls

            if leaf_testpack_cls.test_references is None:
                leaf_testpack_cls.test_references = {}

            tpack_test_references = leaf_testpack_cls.test_references
            tpack_test_references[ref_key] = ref

            mtpkey = create_testpack_key(leaf_testpack_cls)
            if mtpkey not in testpack_table:
                testpack_table[mtpkey] = leaf_testpack_cls

        else:
            raise AKitSemanticError("Assigning a TestCollection to more than one TestPack is not currently supported.") from None

    if len(default_testpack_refs) > 0:
        DefaultTestPack.test_references = default_testpack_refs
        if def_tp_key not in testpack_table:
                testpack_table[def_tp_key] = DefaultTestPack

    return testpack_table

