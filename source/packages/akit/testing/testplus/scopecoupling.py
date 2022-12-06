"""
.. module:: scopecoupling
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ScopeCoupling` class and associated reflection methods.
        The :class:`ScopeCoupling` derived classes can be used to provide setup and teardown of test
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

from typing import Dict

import inspect
import weakref

from akit.coupling.basecoupling import BaseCoupling
from akit.environment.context import ContextUser

class ScopeCoupling(BaseCoupling):
    """
        The :class:`ScopeCoupling` object is the base object class that is used for scope declaration. :class:`ScopeCoupling`
        derived objects are used to create a hierarchy of scopes that are representative of the scopes of execution
        that are represented by the runtime environment.  These scopes of execution are used to establish the runtime
        contexts that task and test instantiations can be run inside of.  The scopes of a runtime environment are
        typically hierarchical in nature starting with the root object of a tree and build more complexed
        environments as they the hierarchy is ascended.

        The code of the :class:`ScopeCoupling` is divided into class level code and instance level code.  The hierarchy
        of the :class:`ScopeCoupling` derived objects are used by the :class:`akit.testing.unittest.testsequencer.Sequencer`
        object to determine the grouping and order of the tests or tasks to be run.  The class level code of the
        :class:`ScopeCoupling` is run by the :class:`akit.sequencer.Sequencer` object based on the class hierarchy to
        establish the order that scopes are entered and exited as the automation sequence is executed by the
        :class:`akit.testing.unittest.testsequencer.Sequencer` object.  The :class:`ScopeCoupling` class level code, is executed
        before any object that inherits from a :class:`ScopeCoupling` derived object is instantiated, so the state for the
        scope has been establish.

        The :class:`ScopeCoupling` instance level code is utilized to inter-operate with the state of the scope and also
        provides scope specific functionality.

        ..notes :
            A scope represents a predefined state that is reached by the execution of code.  The state represents a
            requirement that is needed to be met in order for a task to be able to run.

            Scopes have a name that is like a file system path /configuration

            Scopes can contain state and they are deposited into the context in a leaf just like other nodes.

    """

    TEMPLATE_SCOPES_PREFIX = "/scopes/%s"

    pathname = None

    descendants = {}
    test_references = {}

    def __init__(self):
        """
            The default contructor for an :class:`ScopeCoupling`.
        """
        if self.pathname is None:
            scope_type = type(self)
            scope_leaf = (scope_type.__module__ + "." + scope_type.__name__).replace(".", "/")
            self.pathname = self.TEMPLATE_SCOPES_PREFIX % scope_leaf

        # Create a weak reference to this scope in the global context and create a finalizer that
        # will remove the weak reference when the scope object is destroyed
        wref = weakref.ref(self)
        weakref.finalize(self, scope_finalize, self.context, self.pathname)

        self.context.insert(self.pathname, wref)
        return

    @classmethod
    def attach_to_environment(cls, constraints: Dict={}):
        """
            This API is called so that the ScopeCoupling can process configuration information.  The :class:`ScopeCoupling`
            will verify that it has a valid environment and configuration to run in.

            :raises :class:`akit.exceptions.AKitMissingConfigError`, :class:`akit.exceptions.AKitInvalidConfigError`:
        """
        return

    def scope_enter(self):
        """
            This API is called by the sequencer when a scope of state is being entered by an automation
            run.  The derived `ScopeCoupling` implementation should initialize the scope they are designed
            to manage and if initialization fails, they should raise a :class:`akit.exceptions.AKitScopeEntryError`
            error.

            :raises :class:`akit.exceptions.AKitScopeEntryError`:
        """
        return

    def scope_exit(self):
        """
            This API is called by the sequencer when an automation run is exiting a scope.  The derived
            ScopeCoupling implementation should use this opportunity to tear down the scope that it is
            managing.
        """
        return

class ScopeAperture:
    def __init__(self, scope_type):
        self._scope_type = scope_type
        return

    def __enter__(self):
        self._scope_type.scope_enter()
        return

    def __exit__(self, err_inst, err_type, err_tb):
        self._scope_type.scope_exit() 
        return False

class IteratorScopeCoupling(ContextUser):
    """
        The :class:`IteratorScopeCoupling` object is the base object class that is used for interator scope declaration.
        :class:`IteratorScopeCoupling` derived objects are used to insert a state iteration context into a test scope.
    """

    @classmethod
    def iteration_initialize(cls):
        """
            This API is overridden by derived iterator scope couplings and is called by the sequencer at the start
            of the use of a scope before the scope is entered for the first time.  It provides a hook for the
            iteration scope to setup the iteration state for the iteration scope.
        """
        return

    @classmethod
    def iteration_advance(cls, iterctx): # pylint: disable=unused-argument
        """
            The 'iteration_advance' API is overridden by derived iterator scope couplings and is called by the
            sequencer after the scope exits.  This class level hook method is used by the sequencer to advance
            the scope to the next iteration state.  The 'iteration_advance' API will return a 'True' result
            when the advancement of the iteration state was successful and the scope can be re-entered for
            execution.  The 'iteration_advance' API will return a 'False' when the advancement of the iteration
            state has reached the end of its iteration cycle and the scope should not be re-entered.
        """
        return

def inherits_from_scope_coupling(cls) -> bool:
    """
        Helper function that is used to determine if a type is an :class:`ScopeCoupling` subclass, but not
        the ScopeCoupling type itself.
    """
    is_scopemi = False
    if inspect.isclass(cls) and cls is not ScopeCoupling and issubclass(cls, ScopeCoupling):
        is_scopemi = True
    return is_scopemi

def is_iteration_scope_coupling(cls) -> bool:
    """
        Helper function that is used to determine if a type is an :class:`IteratorScopeCoupling` subclass, but not
        the :class:`IteratorScopeCoupling` type itself.
    """
    is_iterscopemi = False
    if inspect.isclass(cls) and cls is not ScopeCoupling and issubclass(cls, ScopeCoupling) and \
        hasattr(cls, "iteration_initialize") and hasattr(cls, "iteration_advance"):
        is_iterscopemi = True
    return is_iterscopemi

def scope_finalize(context, pathname):
    """
        Callback method used to finalize scope object and ensure they are unpublished from the
        global context.

        :param context: A reference to the context object.
        :param pathname: A string lookup path to the object in the context.
    """
    context.remove(pathname)
    return
