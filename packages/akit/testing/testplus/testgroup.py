"""
.. module:: testnode
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`TestNode` class which is utilized as the collection point
               which associates a set of tests with their descendant execution scopes.

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

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

class TestGroup:
    """
              -------------
              |  Group A  |
        ---------------------------
        |  Group AA  |  Scope AB  |
        -------------------------------
        |         Scope AAA/ABA       |
        -------------------------------
    """

    def __init__(self, name, children):
        self._name = name
        self._children = children
        return

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        return False

    @property
    def children(self):
        return self._children

    @property
    def name(self):
        return self._name

