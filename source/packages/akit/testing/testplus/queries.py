
from typing import Union

import inspect
import os
import fnmatch
import sys
import traceback

from akit.compat import import_by_name
from akit.exceptions import AKitSemanticError

from akit.testing.testplus.testref import TestRef

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

def collect_test_references(root, included_files, filter_package, filter_module, filter_testname, test_prefix):
    """
        Finds the test references based on the expression provided and the excludes
        for this class.  The `find_test_references` method is intended to be called
        multiple times, once with each include expression provided by the users.

        :param expression: An include expression to process and collect references for.
    """

    test_references = {}

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
            mod = None
            if modname in sys.modules:
                mod = sys.modules[modname]
            else:
                mod = import_by_name(modname)

            # Go through all of the members of the
            candidate_function_coll = inspect.getmembers(mod, inspect.isfunction)
            for function_name, function_obj in candidate_function_coll:
                cand_module_name = function_obj.__module__
                # We only want to include the classes that are from the target module
                if cand_module_name != modname:
                    continue

                if function_name.startswith(test_prefix):
                    if filter_testname is not None:
                        # If we have a testname expression only add a reference to the test function
                        # if the function_name matches the filter expression
                        if fnmatch.fnmatch(function_name, filter_testname):
                            tref = TestRef(function_obj)
                            test_references[tref.test_name] = tref
                    else:
                        tref = TestRef(function_obj)
                        test_references[tref.test_name] = tref

        except ImportError:
            errmsg = traceback.format_exc()
            print(errmsg)
            import_errors[ifile] = (modname, ifile, errmsg)

    import_errors.update(import_errors)

    for modname, ifile, errmsg in import_errors.values():
        logger.error("TestCase: Import error filename=%r" % ifile)

    return test_references, import_errors

