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
from akit.workflow.execution import execute_workflow

logger = getAutomatonKitLogger()

def run_workflow_entrypoint(workflow_file: str, workflow_info: dict):
    """
        This is the entry point for the execution of workpackets.  It provides a the execution
        context for the execution of the orchestration steps in the workpacket.

        environment:
            AKIT_BUILD_BRANCH: somebranch
            AKIT_BUILD_NAME: somebuild-2.1.456
            AKIT_JOBTYPE: unknown

        parameters:
            branch: somebranch
            build: somebuild-2.1.456
            landscape: $HOME/akit/config/landscape.yaml

        tasklist:
            - label: Print OS Name
              tasktype: akit.workflow.tasks.embeddedpython@EmbeddedPython
              script:
                  - import os
                  - print(os.name)

            - label: List Directories
              tasktype: akit.workflow.tasks.shellscript@BashScript
              script:
                  - ls -al

    """
    # We must exit with a result code, initialize it to 0 here
    result_code = 0

    if "environment" not in workflow_info:
        error_msg = "The work packet file must have an 'workpacket->environment section. file=%s" % workpacket_file
        raise SyntaxError(error_msg)

    if "parameters" not in workflow_info:
        error_msg = "The work packet file must have an 'workpacket->parameters section. file=%s" % workpacket_file
        raise SyntaxError(error_msg)

    if "workflow" not in workflow_info:
        error_msg = "The work packet file must have an 'workpacket->workflow section. file=%s" % workpacket_file
        raise SyntaxError(error_msg)

    environment = workflow_info["environment"]
    del workflow_info["environment"]

    parameters = workflow_info["parameters"]
    del workflow_info["parameters"]

    workflow = workflow_info["workflow"]
    del workflow_info["workflow"]

    execute_workflow(logger, environment=environment, parameters=parameters, workflow=workflow, **workflow_info)

    sys.exit(result_code)

    return
