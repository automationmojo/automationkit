"""
.. module:: jobcontext
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the JobContext step class which implements
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

import datetime
import os
import uuid

from akit.tasking.steps.stepbase import StepBase
from akit.xtime import format_time_with_fractional

class JobContext(StepBase):

    def __init__(self, ordinal, label, step_info, logger):
        super(JobContext, self).__init__(ordinal, label, step_info, logger)
        return

    def execute(self, parameters):

        # AKIT_RUNID
        run_id = str(uuid.uuid4())
        os.environ["AKIT_RUNID"] = run_id
        parameters["runid"] = run_id

        # AKIT_STARTTIME
        job_start = datetime.datetime.now()
        job_start_str = format_time_with_fractional(job_start.timestamp())
        os.environ["AKIT_STARTTIME"] = job_start_str
        parameters["starttime"] = job_start_str

        from akit.environment.variables import VARIABLES

        if VARIABLES.AKIT_RUNID != run_id:
            VARIABLES.AKIT_RUNID = run_id

        if VARIABLES.AKIT_STARTTIME != job_start_str:
            VARIABLES.AKIT_STARTTIME = job_start_str

        return

