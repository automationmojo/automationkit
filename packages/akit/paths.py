"""
.. module:: paths
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`TaskBase` object which is used as the base.

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

# pylint: disable=global-statement

from typing import List, Optional

import os
import tempfile

from akit.environment.context import Context
from akit.exceptions import AKitRuntimeError

DIR_RESULTS_DIRECTORY = None

TRANSLATE_TABLE_NORMALIZE_FOR_PATH = str.maketrans(",.:;", "    ")

DEFAULT_PATH_EXPANSIONS = [
    os.path.expanduser,
    os.path.expandvars,
    os.path.abspath
]
def expand_path(path_in, expansions=DEFAULT_PATH_EXPANSIONS):

    path_out = path_in
    for expansion_func in expansions:
        path_out = expansion_func(path_out)

    return path_out

def collect_python_modules(search_dir: str, max_depth=None) -> List[str]:
    """
        Walks a directory tree of python modules and collects the names
        of all of the python module files or .py files.  This method allows
        for python namespaces by not forcing the root folder to contain a
        __init__.py file.

        :params searchdir: The root directory to search when collecting python modules.
    """
    pyfiles = []

    search_dir = os.path.abspath(search_dir)
    search_dir_len = len(search_dir)

    for root, _, files in os.walk(search_dir, topdown=True):

        if max_depth is not None:
            dir_leaf = root[search_dir_len:].strip(os.path.sep)
            depth = 0
            if dir_leaf != '':
                dir_leaf_parts = dir_leaf.split(os.path.sep)
                depth = len(dir_leaf_parts)
                if depth > max_depth:
                    break

        for fname in files:
            fbase, fext = os.path.splitext(fname)
            if fext == '.py' and fbase != "__init__":
                ffull = os.path.join(root, fname)
                pyfiles.append(ffull)

    return pyfiles

def ensure_directory_is_package(package_dir: str, package_title: Optional[str] = None):
    """
        Ensures that a directory is represented to python as a package by checking to see if the
        directory has an __init__.py file and if not it adds one.

        :param package_dir: The direcotry to represent as a package.
        :param package_title: Optional title to be written into the documentation string in the package file.
    """
    package_dir_init = os.path.join(package_dir, "__init__.py")
    if not os.path.exists(package_dir_init):
        with open(package_dir_init, 'w') as initf:
            initf.write('"""\n')
            if package_title is not None:
                initf.write('   %s\n' % package_title)
            initf.write('"""\n')
    return

def get_directory_for_code_container(container: str) -> str:
    """
        Returns the directory for a code container (module or package)

        :param container: The code container you want to get a directory for.

        :returns: The string that represents the parent directory of the code
                  container specified.
    """
    if hasattr(container, '__path__'):
        container_dir = str(container.__path__[0]).rstrip(os.sep)
    elif hasattr(container, '__file__'):
        container_dir = os.path.dirname(container.__file__).rstrip(os.sep)
    else:
        raise AKitRuntimeError("Unable to get parent dir for module") from None

    return container_dir

def get_expanded_path(path: str) -> str:
    """
        Returns a path expanded using expanduser, expandvars and abspath for
        the provided path.

        :param path: A path which you want to expand to a full path, expanding the
                     user, variables and relative path syntax.

        :returns: The expanded path
    """
    exp_path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
    return exp_path

def get_path_for_artifacts(label: str) -> str:
    """
        Returns a path in the form (testresultdir)/artifacts/(label)

        :param label: A label to associate with the collection of artifacts. The label is used for
                      the name of the artifact container folder.

        :returns: A path that is descendant from (testresultdir)/artifacts
    """
    trdir = get_path_for_output()
    afdir = os.path.join(trdir, "artifacts", label)

    if not os.path.exists(afdir):
        os.makedirs(afdir)

    return afdir

def get_path_for_diagnostics(label: str) -> str:
    """
        Returns a path in the form (testresultdir)/diagnostics/(label)

        :param label: A label to associate with the collection of diagnostic captures.
                      The label is used for the name of the diagnostic container folder.

        :returns: A path that is descendant from (testresultdir)/diagnostics
    """
    trdir = get_path_for_output()
    diagdir = os.path.join(trdir, "diagnostics", label)

    if not os.path.exists(diagdir):
        os.makedirs(diagdir)

    return diagdir

def get_path_for_output(create=True) -> str:
    """
        Returns the timestamped path where test results and artifacts are deposited to
    """
    global DIR_RESULTS_DIRECTORY

    if DIR_RESULTS_DIRECTORY is None:
        ctx = Context()
        env = ctx.lookup("/environment")

        DIR_RESULTS_DIRECTORY = os.path.expanduser(os.path.expandvars(os.path.abspath(env["output_directory"])))
        if create and not os.path.exists(DIR_RESULTS_DIRECTORY):
            os.makedirs(DIR_RESULTS_DIRECTORY)

    return DIR_RESULTS_DIRECTORY

def get_temporary_directory() -> str:
    """
        Returns the path of a temporary directory in the output directory.
    """
    temp_dir = os.path.join(get_path_for_output(), "temp")
    return temp_dir

def get_temporary_file(suffix: str = '', prefix: str = '') -> str:
    """
        Returns the path of a temporary file in the output directory.
    """
    tempdir = get_temporary_directory()

    tmpfile = tempfile.mktemp(suffix=suffix, prefix=prefix, dir=tempdir)

    return tmpfile

def normalize_name_for_path(name: str) -> str:
    """
        Normalizes a path string by replacing ",.:;" with space and then removing
        white space.

        :param name: A name as a str which is to be normalized to allow it to be used in a path.

        :returns: The normalized string which can be used in a path.
    """
    norm_name = name.translate(TRANSLATE_TABLE_NORMALIZE_FOR_PATH).replace(" ", "")
    return norm_name
