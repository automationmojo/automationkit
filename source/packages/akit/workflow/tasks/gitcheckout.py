"""
.. module:: gitcheckout
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

from typing import Optional

from akit.workflow.tasks.taskbase import TaskBase

class GitCheckout(TaskBase):

    def __init__(self, ordinal: str, label: str, task_info: dict, logger):
        super(GitCheckout, self).__init__(ordinal, label, task_info, logger)
        return

    def execute(self, parameters: Optional[dict]=None, topology: Optional[dict]=None, **kwargs) -> int:

        self._logger.info("STEP: %s - %s" % (self._label, self._ordinal))

        exit_code = 0
        return exit_code