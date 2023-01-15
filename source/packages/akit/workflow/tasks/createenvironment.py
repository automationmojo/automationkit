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

from typing import Dict, Optional

import os
import shlex
import stat
import subprocess

from akit.xformatting import indent_lines

from akit.workflow.tasks.taskbase import TaskBase

class CreateEnvironment(TaskBase):
    """
        A task class that is used to create environment variables that persist and
        are consumable over the entire workflow.
    """

    def __init__(self, ordinal: int, label: str, task_info: dict, logger):
        super(CreateEnvironment, self).__init__(ordinal, label, task_info, logger)
        self._variables = task_info["variables"]
        return

    @property
    def variables(self) -> Dict[str, str]:
        return self._variables

    def execute(self, parameters: Optional[dict]=None, topology: Optional[dict]=None, **kwargs) -> int:

        self._logger.info("STEP: %s - %s" % (self._label, self._ordinal))

        status_code = 0

        for var_info in self._variables:
            var_name = var_info["name"]
            var_command = var_info["command"]

            stdout, stderr, exit_code = None, None, None

            # If "VIRTUAL_ENV" is set then we are running in a virtual environment, setup to run the shell
            # command in the same virtual environment we are currently running in.
            if "VIRTUAL_ENV" in os.environ:
                virtual_env = os.environ["VIRTUAL_ENV"]
                virtual_env_bin = os.path.join(virtual_env, 'bin')
                virtual_env_activate_script = os.path.join(virtual_env_bin, 'activate')
                virtual_env_cmd_script = os.path.join(virtual_env_bin, 'virtual_env_cmd')
                if not os.path.exists(virtual_env_cmd_script):
                    with open(virtual_env_cmd_script, 'w') as vecsf:
                        vecsf.write("#!/usr/bin/env bash\n")
                        vecsf.write("cd {}\n".format(virtual_env_bin))
                        vecsf.write("source {}\n".format(virtual_env_activate_script))
                        vecsf.write("\"$@\"\n")
                    os.chmod(virtual_env_cmd_script, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)

                proc = subprocess.Popen([virtual_env_cmd_script, var_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                exit_code = proc.wait()

            else:
                proc = subprocess.Popen([var_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                stdout, stderr = proc.communicate()
                exit_code = proc.wait()

            if exit_code == 0:
                var_val = stdout.strip()
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
