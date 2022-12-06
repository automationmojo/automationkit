"""
.. module:: createenvironment
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the CreateEnvironment task class which implements
               the execution of environment creation commands.

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
import subprocess

from akit.xformatting import indent_lines

from akit.workflow.tasks.taskbase import TaskBase

class CreateEnvironment(TaskBase):
    """
        A task class that is used to create environment variables that persist and
        are consumable over the entire workflow.
    """

    def __init__(self, ordinal, label, task_info, logger):
        super(CreateEnvironment, self).__init__(ordinal, label, task_info, logger)
        self._variables = task_info["variables"]
        return

    @property
    def variables(self):
        return self._variables

    def execute(self, parameters: Optional[dict]=None, topology: Optional[dict]=None, **kwargs) -> int:

        status_code = 0

        for var_info in self._variables:
            var_name = var_info["name"]
            var_command = var_info["command"]

            proc = subprocess.Popen([var_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = proc.communicate()
            exit_code = proc.wait()

            if exit_code == 0:
                var_val = stdout
                os.environ[var_name] = var_val
            else:
                errmsg_lines = [
                    "Error creating environment variable '{}' with:".format(var_name),
                    "COMMAND: {}".format(var_command),
                    "STDERR: {}".format(stderr)
                ]
                errmsg = os.linesep.join(errmsg_lines)
                self._logger.error(errmsg)

        return status_code
