"""
.. module:: execution
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the function which implemented the execution workflow
               of an individual workpacket.

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

from akit.compat import import_by_name

from akit.exceptions import AKitConfigurationError

def execute_workpacket(environment: dict, parameters: dict, steps: list, logger):

    # Publish the environment variables so they will take effect in the current
    # process and any sub-processes lauched from this process
    for key, val in environment.items():
        os.environ[key] = val

    for step_info in steps:
        label = step_info["label"]
        ttype = step_info["ttype"]

        task_module_name, task_module_class = ttype.split("@")
        task_module = import_by_name(task_module_name)

        if hasattr(task_module, task_module_class):
            task_class = getattr(task_module, task_module_class)

            task_instance = task_class(step_info, logger)

            task_instance.execute(parameters)

        else:
            error_msg = "The specified task module %r does not contain a class %r" % (
                task_module_name, task_module_class)
            raise AKitConfigurationError(error_msg)


    return
