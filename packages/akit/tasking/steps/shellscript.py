"""
.. module:: shellscript
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the ShellScript step class which implements
               the execution of shell based steps in a workpacket.

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
import stat
import subprocess

from akit.paths import get_temporary_file
from akit.xformatting import indent_lines

from akit.tasking.steps.stepbase import StepBase

class ShellScript(StepBase):

    def __init__(self, ordinal, label, step_info, logger):
        super(ShellScript, self).__init__(ordinal, label, step_info, logger)
        self._lines = step_info["lines"]
        return

    @property
    def lines(self):
        return self._lines

    def execute(self, parameters):

        self._logger.info("STEP: %s - %d" % (self._label, self._ordinal))

        script_content = os.linesep.join(self._lines)

        tempfile = get_temporary_file(prefix="step-%d" % self._ordinal, suffix=".sh")

        self._logger.info("Running Script: %s" % tempfile)

        with open(tempfile, 'w') as tf:
            tf.write(script_content)

        os.chmod('somefile', stat.S_IEXEC)

        proc = subprocess.Popen([tempfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        exit_code = proc.wait()

        log_msg_lines = [
            "RESULT CODE: %d" % exit_code,
            "STDOUT:",
            indent_lines(stdout.read(), level=1),
            "STDERR:",
            indent_lines(stderr.read(), level=1),
        ]

        log_msg = os.linesep.join(log_msg_lines)
        if exit_code == 0:
            self._logger.info(log_msg)
        else:
            self._logger.error(log_msg)

        return