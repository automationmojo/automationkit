
"""
.. module:: taskbase
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`TaskBase` object which is used as the base.

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

class TaskBase:

    required_scopes = None

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._scope = None
        return

    @classmethod
    def do(cls, scope, *args, **kwargs):
        return

    @classmethod
    def begin(cls, scope, *args, **kwargs):
        return

    def enter(self):
        self._scope.enter()
        return

    def exit(self):
        self._scope.exit()
        return
