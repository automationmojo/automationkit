"""
.. module:: shellscript
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the EmbeddedPython task class which implements
               the execution of inline python based tasks in a workpacket.

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

from typing import List, Optional

import os

from akit.xformatting import indent_lines

from akit.workflow.tasks.taskbase import TaskBase

class EmbeddedPython(TaskBase):
    """
        A task class that is used to setup the running of an embedded python script
        in the context of the automation worker.
    """

    def __init__(self, ordinal: str, label: str, task_info: dict, logger):
        super(EmbeddedPython, self).__init__(ordinal, label, task_info, logger)
        self._script = task_info["script"]
        return

    @property
    def script(self) -> List[str]:
        return self._script

    def execute(self, parameters: Optional[dict]=None, topology: Optional[dict]=None, **kwargs) -> int:

        self._logger.info("STEP: %s - %s" % (self._label, self._ordinal))

        locals().update({"parameters": parameters, "topology": topology})
        locals().update(kwargs)

        script_content = os.linesep.join(self._script)
        script_content = indent_lines(script_content, level=3)

        exit_status = 0

        try:
            # Execute the inline python script in the context of the current
            # globals and locals.
            exec(script_content, globals(), locals())
        except:
            exit_status = 1

        return exit_status
