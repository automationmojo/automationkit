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

import json
import os

def find_testmodule_root(module) -> str:
    """
        Finds the root directory that is associated with a given test module.
    """
    mod_dir = os.path.dirname(module.__file__)
    while True:
        pkg_dir_file = os.path.join(mod_dir, "__init__.py")
        if os.path.exists(pkg_dir_file):
            mod_dir = os.path.dirname(mod_dir)
        else:
            break

    return mod_dir

def find_testmodule_fullname(module, root_path=None) -> str:
    """
        Finds the root directory that is associated with a given test module and
        then uses the leaf path to a module to develop a full module name.
    """

    if root_path is None:
        root_path = find_testmodule_root(module)

    mod_filebase, _ = os.path.splitext(os.path.abspath(module.__file__))
    testmodule_fullname = mod_filebase[len(root_path):].strip("/").replace("/", ".")

    return testmodule_fullname

def catalog_tree(rootdir: str):
    """
        Adds json catalog files to a file system tree to help provide directory
        services to javascript in html files.
    """
    for dirpath, dirnames, filenames in os.walk(rootdir, topdown=True):
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