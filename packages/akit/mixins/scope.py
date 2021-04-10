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

import inspect
import weakref

from akit.environment.context import ContextUser

class ScopeMixIn(ContextUser):
    """
        The :class:`ScopeMixIn` object is the base object class that is used for scope declaration. :class:`ScopeMixIn`
        derived objects are used to create a hierarchy of scopes that are representative of the scopes of execution
        that are represented by the runtime environment.  These scopes of execution are used to establish the runtime
        contexts that task and test instantiations can be run inside of.  The scopes of a runtime environment are
        typically hierarchical in nature starting with the root object of a tree and build more complexed
        environments as they the hierarchy is ascended.

        The code of the :class:`ScopeMixIn` is divided into class level code and instance level code.  The hierarchy
        of the :class:`ScopeMixIn` derived objects are used by the :class:`akit.testing.unittest.testsequencer.Sequencer`
        object to determine the grouping and order of the tests or tasks to be run.  The class level code of the
        :class:`ScopeMixIn` is run by the :class:`akit.sequencer.Sequencer` object based on the class hierarchy to
        establish the order that scopes are entered and exited as the automation sequence is executed by the
        :class:`akit.testing.unittest.testsequencer.Sequencer` object.  The :class:`ScopeMixIn` class level code, is executed
        before any object that inherits from a :class:`ScopeMixIn` derived object is instantiated, so the state for the
        scope has been establish.

        The :class:`ScopeMixIn` instance level code is utilized to inter-operate with the state of the scope and also
        provides scope specific functionality.

        ..notes :
            A scope represents a predefined state that is reached by the execution of code.  The state represents a
            requirement that is needed to be met in order for a task to be able to run.

            Scopes have a name that is like a file system path /environment/configuration

            Scopes can contain state and they are deposited into the context in a leaf just like other nodes.

    """

    TEMPLATE_SCOPES_PREFIX = "/scopes/%s"

    pathname = None

    descendants = {}
    test_references = {}

    def __init__(self):
        """
            The default contructor for an :class:`ScopeMixIn`.
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
    def scope_enter(cls):
        """
            This API is called by the sequencer when a scope of state is being entered by an automation
            run.  The derived `ScopeMixIn` implementation should initialize the scope they are designed
            to manage and if initialization fails, they should raise a :class:`akit.exceptions.AKitScopeEntryError`
            error.

            :raises :class:`akit.exceptions.AKitScopeEntryError`:
        """
        return

    @classmethod
    def scope_exit(cls):
        """
            This API is called by the sequencer when an automation run is exiting a scope.  The derived
            ScopeMixIn implementation should use this opportunity to tear down the scope that it is
            managing.
        """
        return


class IteratorScopeMixIn(ContextUser):
    """
        The :class:`IteratorScopeMixIn` object is the base object class that is used for interator scope declaration.
        :class:`IteratorScopeMixIn` derived objects are used to insert a state iteration context into a test scope.
    """

    @classmethod
    def iteration_initialize(cls):
        """
            This API is overridden by derived iterator scope mixins and is called by the sequencer at the start
            of the use of a scope before the scope is entered for the first time.  It provides a hook for the
            iteration scope to setup the iteration state for the iteration scope.
        """
        return

    @classmethod
    def iteration_advance(cls, iterctx): # pylint: disable=unused-argument
        """
            The 'iteration_advance' API is overridden by derived iterator scope mixins and is called by the
            sequencer after the scope exits.  This class level hook method is used by the sequencer to advance
            the scope to the next iteration state.  The 'iteration_advance' API will return a 'True' result
            when the advancement of the iteration state was successful and the scope can be re-entered for
            execution.  The 'iteration_advance' API will return a 'False' when the advancement of the iteration
            state has reached the end of its iteration cycle and the scope should not be re-entered.
        """
        return

def inherits_from_scope_mixin(cls) -> bool:
    """
        Helper function that is used to determine if a type is an :class:`ScopeMixIn` subclass, but not
        the ScopeMixIn type itself.
    """
    is_scopemi = False
    if inspect.isclass(cls) and cls is not ScopeMixIn and issubclass(cls, ScopeMixIn):
        is_scopemi = True
    return is_scopemi

def is_iteration_scope_mixin(cls) -> bool:
    """
        Helper function that is used to determine if a type is an :class:`IteratorScopeMixIn` subclass, but not
        the :class:`IteratorScopeMixIn` type itself.
    """
    is_iterscopemi = False
    if inspect.isclass(cls) and cls is not ScopeMixIn and issubclass(cls, ScopeMixIn) and \
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
