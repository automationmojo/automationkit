"""
.. module:: scope
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ScopeMixIn` class and associated reflection methods.
        The :class:`ScopeMixIn` derived classes can be used to provide setup and teardown of test
        automation scopes of execution for groups of tests.

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

from akit.environment.context import ContextUser

class BaseMixIn(ContextUser):
    """
        The :class:`BaseMixIn` object serves as a base type to detect mixin based
        resources.
    """