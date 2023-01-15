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

from typing import Optional

import os
import stat
import subprocess

from akit.paths import get_temporary_file
from akit.xformatting import indent_script

from akit.workflow.tasks.taskbase import TaskBase

class ShellScript(TaskBase):

    def __init__(self, ordinal: str, label: str, task_info: dict, logger):
        super(ShellScript, self).__init__(ordinal, label, task_info, logger)
        self._script = task_info["script"]
        return

    @property
    def script(self) -> str:
        return self._script

    def execute(self, parameters: Optional[dict]=None, topology: Optional[dict]=None, **kwargs) -> int:

        self._logger.info("STEP: %s - %s" % (self._label, self._ordinal))

        script_content = os.linesep.join(self._script)

        tempfile = get_temporary_file(prefix="step-%d" % self._ordinal, suffix=".sh")

        self._logger.info("Running Script: %s" % tempfile)

        with open(tempfile, 'w') as tf:
            tf.write(script_content)

        os.chmod(tempfile, stat.S_IEXEC)

        proc = subprocess.Popen([tempfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        exit_code = proc.wait()

        log_msg_script = [
            "RESULT CODE: %d" % exit_code,
            "STDOUT:",
            indent_script(stdout.read(), level=1),
            "STDERR:",
            indent_script(stderr.read(), level=1),
        ]

        log_msg = os.linesep.join(log_msg_script)
        if exit_code == 0:
            self._logger.info(log_msg)
        else:
            self._logger.error(log_msg)

        return exit_code