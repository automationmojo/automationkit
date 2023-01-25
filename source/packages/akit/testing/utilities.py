"""
.. module:: utilities
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing utility functions utilized by the objects in the testing module.

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

from typing import Union

import fnmatch
import json
import os

from akit.exceptions import AKitConfigurationError
from akit.paths import collect_python_modules

def catalog_tree(rootdir: str, ignore_dirs=[]):
    """
        Adds json catalog files to a file system tree to help provide directory
        services to javascript in html files.
    """
    for dirpath, dirnames, filenames in os.walk(rootdir, topdown=True):
        dir_base_name = os.path.basename(dirpath)
        if dir_base_name not in ignore_dirs:

            for igdir in ignore_dirs:
                if igdir in dirnames:
                    dirnames.remove(igdir)

            catalog = {
                "files": filenames,
                "folders": dirnames
            }

            catalogfile = os.path.join(dirpath, "catalog.json")
            with open(catalogfile, 'w') as cf:
                json.dump(catalog, cf, indent=4)

    return

def create_testpack_key(testpack_cls):
    mtpkey = testpack_cls.__module__ + "@" + testpack_cls.__name__
    return mtpkey

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

    root_pkg = os.path.basename(root)

    included_file_candidates = set()

    if package is None:
        # If package is None, then we had a single item expression, this means
        # we can look for a single file, or a directory with lots of files.
        filenames = os.listdir(root)
        for fname in filenames:
            pkg_name = "{}.{}".format(root_pkg, fname)
            if pkg_name.startswith(module) or fnmatch.fnmatch(pkg_name, module):
                ffull = os.path.join(root, fname)
                if os.path.isfile(ffull):
                    fbase, fext = os.path.splitext(fname)
                    if fext == ".py" and fbase != "__init__":
                        included_file_candidates.add(ffull)
                elif os.path.isdir(ffull):
                    module_list = collect_python_modules(ffull)
                    for mod in module_list:
                        included_file_candidates.add(mod)
    else:
        pkgpathpfx = package.replace(".", "/")
        fullpathpfx = pkgpathpfx + "/" + module
        for dirpath, _, filenames in os.walk(root):
            dirleaf = root_pkg + "/" + dirpath[len(root):].lstrip(os.sep)
            dirleaf = dirleaf.rstrip("/")

            if dirleaf.startswith(fullpathpfx) or fnmatch.fnmatch(dirleaf, fullpathpfx):
                collected_modules = collect_python_modules(dirpath)
                for cm in collected_modules:
                    included_file_candidates.add(cm)
            elif dirleaf.startswith(pkgpathpfx) or fnmatch.fnmatch(dirleaf, pkgpathpfx):
                for fname in filenames:
                    fbase, fext = os.path.splitext(fname)
                    if fext == ".py" and fbase != "__init__" and \
                        fbase.startswith(module) and fnmatch.fnmatch(fbase, module):
                        ffull = os.path.join(dirpath, fname)
                        included_file_candidates.add(ffull)

    included_files = []
    excluded_files = []

    while len(included_file_candidates) > 0:
        candidate_file = included_file_candidates.pop()

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

def find_testmodule_root(module) -> str:
    """
        Finds the root directory that is associated with a given test module.
    """
    mod_dir = os.path.dirname(module.__file__)
    while True:
        pkg_dir_file = os.path.join(mod_dir, "__testroot__.py")
        if not os.path.exists(pkg_dir_file):
            if mod_dir == "/":
                errmsg = "TestPlus test files must exist inside a test root directory marked with a __testroot__.py file."
                raise AKitConfigurationError(errmsg)
            mod_dir = os.path.dirname(mod_dir)
        else:
            break

    return mod_dir

def find_testmodule_fullname(module, testroot=None) -> str:
    """
        Finds the root directory that is associated with a given test module and
        then uses the leaf path to a module to develop a full module name.
    """

    if testroot is None:
        testroot = find_testmodule_root(module)

    mod_filebase, _ = os.path.splitext(os.path.abspath(module.__file__))
    testroot_parent = os.path.dirname(testroot)
    testmodule_fullname = mod_filebase[len(testroot_parent):].strip("/").replace("/", ".")

    return testmodule_fullname





