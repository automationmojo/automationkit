
"""
.. module:: taskchain
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`TaskChain` class which serves as a base for chains of tasks.

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

from akit.tasking.tasklink import TaskLink

class TaskChain(TaskLink):
    """
        The :class:`TaskChain` object serves as the base link in a chain of tasks.
    """

    def __init__(self, name):
        self._chain = []
        super(TaskChain, self).__init__(self, self._chain, name)
        return
