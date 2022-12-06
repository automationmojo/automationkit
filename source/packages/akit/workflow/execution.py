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

from akit.compat import import_by_name

from akit.exceptions import AKitConfigurationError

def execute_workflow(logger, *, environment: dict, parameters: dict, tasklist: list, **kwargs):

    # Publish the environment variables so they will take effect in the current
    # process and any sub-processes lauched from this process
    for key, val in environment.items():
        os.environ[key] = val

    result_code = 0

    task_ordinal = 1
    for task_info in tasklist:
        task_label = task_info["label"]
        tasktype = task_info["tasktype"]

        task_module_name, task_module_class = tasktype.split("@")
        task_module = import_by_name(task_module_name)

        failure_section = None

        if hasattr(task_module, task_module_class):
            task_class = getattr(task_module, task_module_class)

            task_instance = task_class(task_ordinal, task_label, task_info, logger)

            if failure_section is not None:
                section = task_instance.section
                if failure_section == section:
                    failure_section = None
                else:
                    # Skip ahead until we file the failure section
                    continue

            task_result = task_instance.execute(parameters=parameters, **kwargs)
            if task_result != 0:
                result_code = 1
                if task_instance.onfailure is not None:
                    failure_section = task_instance.onfailure

        else:
            error_msg = "The specified task module %r does not contain a class %r" % (
                task_module_name, task_module_class)
            raise AKitConfigurationError(error_msg) from None

    return result_code
