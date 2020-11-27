"""
.. module:: variables
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`VARIABLES` object which is used store the environment variables.

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

import os
import sys

environ = os.environ

LOG_LEVEL_NAMES = [
    "NOTSET",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "QUIET"
]

class VARIABLES:
    AKIT_BRANCH = "unknown"
    if "AKIT_BRANCH" in environ:
        AKIT_BRANCH = environ["AKIT_BRANCH"]

    AKIT_BUILD = "unknown"
    if "AKIT_BUILD" in environ:
        AKIT_BUILD = environ["AKIT_BUILD"]

    AKIT_CONSOLE_LOG_LEVEL = None
    if "AKIT_CONSOLE_LOG_LEVEL" in environ:
        AKIT_CONSOLE_LOG_LEVEL = environ["AKIT_CONSOLE_LOG_LEVEL"].upper()

    AKIT_FILE_LOG_LEVEL = None
    if "AKIT_FILE_LOG_LEVEL" in environ:
        AKIT_FILE_LOG_LEVEL = environ["AKIT_FILE_LOG_LEVEL"].upper()

    AKIT_FLAVOR = "unknown"
    if "AKIT_FLAVOR" in environ:
        AKIT_FLAVOR = environ["AKIT_FLAVOR"]

    AKIT_JOBTYPE = "unknown"
    if "AKIT_JOBTYPE" in environ:
        AKIT_JOBTYPE = environ["AKIT_JOBTYPE"]

    AKIT_LANDSCAPE_MODULE = None
    if "AKIT_LANDSCAPE_MODULE" in environ:
        AKIT_LANDSCAPE_MODULE = environ["AKIT_LANDSCAPE_MODULE"]

    AKIT_STARTTIME = None
    if "AKIT_STARTTIME" in environ:
        AKIT_STARTTIME = environ["AKIT_STARTTIME"]

    AKIT_USER_CONFIGURATION = "~/akit/config/userconfig.json"
    if "AKIT_USER_CONFIGURATION" in environ:
        AKIT_USER_CONFIGURATION = environ["AKIT_USER_CONFIGURATION"]

def extend_path(dir_to_add):
    """
        Extends the PYTHONPATH in the current python process and also modifies
        'PYTHONPATH' so the child processes will also see inherit the extension
        of 'PYTHONPATH'.
    """
    found = False

    for nxt_item in sys.path:
        nxt_item = nxt_item.rstrip(os.sep)
        dir_to_add = dir_to_add.rstrip(os.sep)
        if nxt_item == dir_to_add:
            found = True
            break

    if not found:
        sys.path.insert(0, dir_to_add)
        os.environ["PYTHONPATH"] = dir_to_add + os.pathsep + os.environ["PYTHONPATH"]

    return