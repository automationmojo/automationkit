"""
.. module:: testpack
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is contains the :class:`TestPack` class which is utilized as the collection point
               which associates a set of tests with their execution scopes.

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

import inspect

from akit.mixins.scope import ScopeMixIn, inherits_from_scope_mixin

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

class TestPack(ScopeMixIn):
    """
              --------------
              |  TestPack  |
        -------------------------
        |  Scope A  |  Scope B  |
        -------------------------
        |         Scope C       |
        -------------------------

        Pack:
            * Single instance
            * Collect or Group tests
            * Associates scopes of execution with the tests
            * Allows for the customization of the Setup and TearDown of scopes

        Scopes:
            * Collect Resources utilized in a Scope of Execution for a group of tests
            * Setup and TearDown of scope
    """

    name = ""           # TestPack Friendly Name
    description = ""    # TestPack Description

    # Includes and excludes can be added to a TestPack in order to help the test framework reduce
    # the amount of resources that need to be expended in order to scan for the tests that are linked
    # to a TestPack
    searchin = None

    context = None # The scopes associated with a testpack, scopes
    test_references = None

    def acclimate(self, testlandscape): # pylint: disable=no-self-use, unused-argument
        """
            API called by the test framework in order to acclimate the :class:`TestPack` to the :class:`TestLandscape`.
            When this method is called on a :class:`TestPack` it can analyze the testlandscape and configure
            internal state that can be used to determine which tests are applicable to the given test
            landscape.
        """
        return

    def expectations(self): # pylint: disable=no-self-use
        """
            Method that can be implemented by derived classes or updated dynamically to reflect the
            expected torun and skipped test counts for a given testlandscape.  The test framework will call the 'acclimate'
            method prior to calling this method in order to let the 'TestPack' analyze the testlandscape
            and determine which tests are applicable to the test

            (torun, skipped)
        """
        return

    def scopes_enter(self): # pylint: disable=no-self-use
        """
            Called to enter the scopes to setup for running the :class:`TestPack`.
        """

        rev_mro = list(TestPack.mro())
        rev_mro.reverse()

        for nxt_cls in rev_mro:
            if inherits_from_scope_mixin(nxt_cls):
                nxt_cls.scope_enter()
                if not hasattr(nxt_cls, "scope_enter_count"):
                    nxt_cls.scope_enter_count = 1
                else:
                    nxt_cls.scope_enter_count += 1 # pylint: disable=no-member

        return

    def scopes_exit(self): # pylint: disable=no-self-use
        """
            Called to exit the scopes to cleanup after running the :class:`TestPack`.
        """

        norm_mro = list(TestPack.mro())

        for nxt_cls in norm_mro:
            if inherits_from_scope_mixin(nxt_cls):
                nxt_cls.scope_exit()
                if hasattr(nxt_cls, "scope_enter_count"):
                    nxt_cls.scope_enter_count -= 1 # pylint: disable=no-member
                else:
                    logger.error("ERROR: Every scope should have a 'scope_enter_count' class variable.")

        return


class DefaultTestPack(TestPack):
    """
        The :class:`DefaultTestPack` is utilized to provide a package container for collections of tests
        that either share a common collection of foundation scopes or do not explicitly mixin a parent class
        that is a subclass of :class:`ScopeMixIn`.
    """
    pathname = ""

def inherits_from_testpack(cls) -> bool:
    """
        Helper method that detects if an objects type inherits from :class:`TestPack` but ensures
        that the object is not a :class:`TestPack` type from this file.
    """
    istp = False
    if inspect.isclass(cls) and cls is not TestPack and issubclass(cls, TestPack):
        istp = True
    return istp

def testpack_compare(tpack):
    """
        Used to provide a key for comparing :class:`TestPack` objects.
    """
    return tpack.weight
