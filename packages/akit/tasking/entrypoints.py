"""
.. module:: entrypoints
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A set of standaridized entry point functions that provide standardized task orchestration
               of workpacket jobs.

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

from akit.xlogging.foundations import logging_initialize, getAutomatonKitLogger
from akit.tasking.execution import execute_workpacket

logger = getAutomatonKitLogger()

def run_workpacket_entrypoint(workpacket_file: str, workpacket_info: dict):
    """
        This is the entry point for the execution of workpackets.  It provides a the execution
        context for the execution of the orchestration steps in the workpacket.

        environment:
            AKIT_BRANCH: somebranch
            AKIT_BUILD: somebuild-2.1.456
            AKIT_JOBTYPE: unknown
        parameters:
            branch: somebranch
            build: somebuild-2.1.456
            landscape: $HOME/akit/config/landscape.yaml
        steps:
        - label: Print OS Name
            ttype: akit.tasking.tasks.embeddedpython@EmbeddedPython
            lines:
            - import os
            - print(os.name)
        - label: List Directories
            ttype: akit.tasking.tasks.shellscript@BashScript
            lines:
            - ls -al
    """
    # We must exit with a result code, initialize it to 0 here
    result_code = 0

    if "environment" not in workpacket_info:
        error_msg = "The work packet file must have an 'workpacket->environment section. file=%s" % workpacket_file
        raise SyntaxError(error_msg)

    if "parameters" not in workpacket_info:
        error_msg = "The work packet file must have an 'workpacket->parameters section. file=%s" % workpacket_file
        raise SyntaxError(error_msg)

    if "steps" not in workpacket_info:
        error_msg = "The work packet file must have an 'workpacket->steps section. file=%s" % workpacket_file
        raise SyntaxError(error_msg)

    environment = workpacket_info["environment"]
    parameters = workpacket_info["parameters"]
    steps = workpacket_info["steps"]

    execute_workpacket(environment, parameters, steps, logger)

    sys.exit(result_code)

    return
