
from typing import Union

import inspect
import os
import fnmatch
import traceback

from akit.compat import import_file
from akit.paths import collect_python_modules

from akit.testing.testcontainer import inherits_from_testcontainer
from akit.testing.testpack import DefaultTestPack, inherits_from_testpack
from akit.testing.testref import TestRef
from akit.testing.utilities import create_testpack_key

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

def find_included_modules_under_root(root: str, package: Union[str, None], module: str, excluded_path_prefixes: list = []):
    """
        Walks through a directory tree starting at a root directory and finds all of the files that corresponded to
        the package, module expressions specified.

        :param root: The root directory to start from when performing the tree walk to look
                     for included tests.
        :param package: The package name component if there is one.  The package components are the directories
                        with __init__.py files up to the file where the module file itself is found. It could be
                        that there is only a module name.
        :param module: The module name component.  There must be a module because that is the file where the tests
                       are found.
    """


    included_file_candidates = []

    if package is None:
        # If package is None, then we had a single item expression, this means
        # we can look for a single file, or a directory with lots of files.
        filenames = os.listdir(root)
        for fname in filenames:
            if fnmatch.fnmatch(fname, module):
                ffull = os.path.join(root, fname)
                if os.path.isfile(ffull):
                    fbase, fext = os.path.splitext(fname)
                    if fext == ".py" and fbase != "__init__":
                        included_file_candidates.append(ffull)
                elif os.path.isdir(ffull):
                    included_file_candidates.extend(collect_python_modules(ffull))
    else:
        pkgpathpfx = package.replace(".", "/")
        fullpathpfx = pkgpathpfx + "/" + module
        for dirpath, _, filenames in os.walk(root):
            dirleaf = dirpath[len(root):].lstrip(os.sep)

            # If we are in the testroot, then dirleaf will be len 0
            if len(dirleaf) > 0:
                if dirleaf.startswith(fullpathpfx) or fnmatch.fnmatch(dirleaf, fullpathpfx):
                    included_file_candidates.extend(collect_python_modules(dirpath))
                elif dirleaf.startswith(pkgpathpfx) or fnmatch.fnmatch(dirleaf, pkgpathpfx):
                    for fname in filenames:
                        fbase, fext = os.path.splitext(fname)
                        if fext == ".py" and fbase != "__init__" and \
                            fbase.startswith(module) and fnmatch.fnmatch(fbase, module):
                            ffull = os.path.join(dirpath, fname)
                            included_file_candidates.append(ffull)

    included_files = []
    excluded_files = []

    while len(included_file_candidates) > 0:
        candidate_file = included_file_candidates.pop(0)

        keep_file = True
        for expfx in excluded_path_prefixes:
            if candidate_file.beginswith(expfx):
                keep_file = False
                break

        if keep_file:
            included_files.append(candidate_file)
        else:
            excluded_files.append(candidate_file)

    return included_files, excluded_files

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

    # Go through the files and import them, then go through the classes and find the TestPack and
    # TestContainer objects that match the specified include expression criteria
    rootlen = len(root)
    for ifile in included_files:
        modname = None
        try:
            ifilebase, _ = os.path.splitext(ifile)
            ifileleaf = ifilebase[rootlen:].strip("/")
            modname = ifileleaf.replace("/", ".")

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

        # If we didn't find a TestPackMixIn derived object, then
        # add this test reference to the DefaultTestPackMixIn
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
            raise Exception("Assigning a TestCollection to more than one TestPack is not currently supported.")

    if len(default_testpack_refs) > 0:
        DefaultTestPack.test_references = default_testpack_refs
        if def_tp_key not in testpack_table:
                testpack_table[def_tp_key] = DefaultTestPack

    return testpack_table