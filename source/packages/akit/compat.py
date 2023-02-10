"""
.. module:: compat
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains functions that are utilized to provide compatibility across different
               operating system platforms and python version.

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

import traceback

import sys
import importlib

from types import ModuleType

NoneType = type(None)

is_python3 = sys.version_info[0] == 3
is_python_pre_3_5 = (is_python3 and sys.version_info[1] < 5)

def import_by_name(modulename: str) -> ModuleType:
    """
        Imports a module by name.
    """

    mod = None
    if modulename in sys.modules:
        mod = sys.modules[modulename]
    else:
        mod = importlib.import_module(modulename)

    return mod

def import_file(name: str, loc: str, by_file_only=False) -> ModuleType:
    """
        Import module from a file. Used to load models from a directory.

        :param unicode name: Name of module to load.
        :param (unicode / Path) loc: Path to the file.

        returns: The loaded module.
    """
    mod = None
    if name in sys.modules:
        mod = sys.modules[name]

    if mod is None:
        if is_python_pre_3_5:
            import imp # pylint: disable=import-outside-toplevel

            mod = imp.load_source(name, loc)
        else:

            while True:
                if not by_file_only:
                    # First try to import the module by name only
                    try:
                        mod = importlib.import_module(name)
                        break
                    except ImportError:
                        errmsg = traceback.format_exc()
                        pass

                spec = importlib.util.spec_from_file_location(name, str(loc))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                sys.modules[name] = mod
                break

    return mod

def bytes_cast(val: Union[str, bytes]) -> bytes:
    """
        Ensures that the 'val' parameter is a bytes object.

        :param val: A str or bytes value that needs to be converted to bytes.
        :param val: str or bytes

        :returns: The input value converted to a bytes
    """
    if isinstance(val, str):
        val = val.encode('utf-8')
    return val

def str_cast(val: Union[str, bytes]) -> str:
    """
        Ensures that the 'val' parameter is a str object.

        :param val: A str or bytes value that needs to be converted to str.
        :param val: str or bytes

        :returns: The input value converted to a str
    """
    if isinstance(val, bytes):
        val = val.decode('utf-8')
    return val
