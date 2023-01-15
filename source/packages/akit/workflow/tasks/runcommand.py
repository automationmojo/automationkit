"""
.. module:: runcommand
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the RunCommand task class which implements
               the execution of a singular command based tasks in a workpacket.

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

import os
import stat
import subprocess

from akit.paths import get_temporary_file
from akit.xformatting import indent_lines

from akit.workflow.tasks.taskbase import TaskBase

class RunCommand(TaskBase):

    def __init__(self, ordinal: str, label: str, task_info: dict, logger):
        super(RunCommand, self).__init__(ordinal, label, task_info, logger)
        self._command = task_info["command"]
        return

    @property
    def command(self) -> str:
        return self._command

    def execute(self, parameters: Optional[dict]=None, topology: Optional[dict]=None, **kwargs) -> int:

        self._logger.info("STEP: %s - %s" % (self._label, self._ordinal))

        self._logger.info("Running Command: %s" % self._command)

        proc = subprocess.Popen([self._command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        exit_code = proc.wait()

        stdout = stdout.decode()
        stderr = stderr.decode()

        log_msg_lines = [
            "RESULT CODE: %d" % exit_code,
            "STDOUT:",
            indent_lines(stdout, level=1),
            "STDERR:",
            indent_lines(stderr, level=1),
        ]

        log_msg = os.linesep.join(log_msg_lines)
        if exit_code == 0:
            self._logger.info(log_msg)
        else:
            self._logger.error(log_msg)

        return exit_code