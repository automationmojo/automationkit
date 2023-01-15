"""
.. module:: taskbase
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the base task object that other tasks derive
               from.

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

from typing import Optional

from akit.exceptions import AKitNotOverloadedError

class TaskBase:

    def __init__(self, ordinal: str, label: str, task_info: dict, logger):
        self._ordinal = ordinal
        self._label = label
        self._task_info = task_info
        self._logger = logger

        self._onfailure = None
        if "onfailure" in task_info:
            self._onfailure = task_info["onfailure"]

        self._onsuccess = None
        if "onsuccess" in task_info:
            self._onsuccess = task_info["onsuccess"]

        return

    @property
    def label(self) -> str:
        return self._label

    @property
    def onfailure(self) -> str:
        return self._onfailure

    @property
    def onsuccess(self) -> str:
        return self._onsuccess

    @property
    def ordinal(self) -> str:
        return self._ordinal

    @property
    def task_info(self) -> dict:
        return self._task_info

    def execute(self, parameters: Optional[dict]=None, topology: Optional[dict]=None, **kwargs) -> int:
        raise AKitNotOverloadedError("TaskBase->execute must be overloaded by derived classes.") from None