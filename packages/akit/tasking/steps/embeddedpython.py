"""
.. module:: shellscript
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A module that provides the EmbeddedPython step class which implements
               the execution of inline python based steps in a workpacket.

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

from akit.xformatting import indent_lines

from akit.tasking.steps.stepbase import StepBase

class EmbeddedPython(StepBase):
    """
        A task class that is used to setup the running of an embedded python script
        in the context of the automation worker.
    """

    def __init__(self, ordinal, label, step_info, logger):
        super(EmbeddedPython, self).__init__(ordinal, label, step_info, logger)
        self._lines = step_info["lines"]
        return

    @property
    def lines(self):
        return self._lines

    def execute(self, parameters):

        self._logger.info("STEP: %s - %d" % (self._label, self._ordinal))

        locals().update(parameters)

        script_content = os.linesep.join(self._lines)
        script_content = indent_lines(script_content, level=2)

        # Execute the inline python script in the context of the current
        # globals and locals.
        exec(script_content, globals(), locals())

        return
