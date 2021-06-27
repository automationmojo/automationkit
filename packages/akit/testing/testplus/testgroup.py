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


from akit.testing.testplus.registration.resourceregistry import resource_registry

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

    def __init__(self, name, package=None):
        self._name = name
        self._package = package
        self._children = {}
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

    @property
    def package(self):
        return self._package

    def get_resource_table(self):
        scope_name = "{}.{}".format(self._package, self._name) 
        rtable = resource_registry.lookup_resource_table_by_scope(scope_name)
        return rtable

    def __contains__(self, key):
        has_item = key in self._children
        return has_item

    def __getitem__(self, key):
        item = self._children[key]
        return item

    def __setitem__(self, key, value):
        self._children[key] = value
        return
