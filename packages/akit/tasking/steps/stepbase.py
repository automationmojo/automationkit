"""
.. module:: shellscript
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the ShellScript task class which implements
               the execution of shell based tasks in a workpacket.

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

from akit.exceptions import AKitNotOverloadedError

class StepBase:

    def __init__(self, ordinal, label, step_info, logger):
        self._ordinal = ordinal
        self._label = label
        self._step_info = step_info
        self._logger = logger
        return

    @property
    def label(self):
        return self._label

    @property
    def ordinal(self):
        return self._ordinal

    @property
    def step_info(self):
        return self._step_info

    def execute(self, parameters):
        raise AKitNotOverloadedError("StepBase->execute must be overloaded by derived classes.") from None