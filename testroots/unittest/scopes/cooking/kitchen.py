
from akit.mixins.scope import ScopeMixIn

class KitchenScope(ScopeMixIn):

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

