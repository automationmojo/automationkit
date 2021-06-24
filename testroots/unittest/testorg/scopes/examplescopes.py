
from akit.mixins.scope import ScopeMixIn

class ExampleScopeAMixIn(ScopeMixIn):

    @classmethod
    def scope_enter(cls):
        print("Enter A")
        return

    @classmethod
    def scope_exit(cls):
        print("Exit A")
        return

    def shout_out(self):
        print("Im scope ExampleScopeAMixIn")
        return


class ExampleScopeAAMixIn(ExampleScopeAMixIn):

    @classmethod
    def scope_enter(cls):
        print("Enter AA")
        return

    @classmethod
    def scope_exit(cls):
        print("Exit AA")
        return


class ExampleScopeABMixIn(ExampleScopeAMixIn):

    @classmethod
    def scope_enter(cls):
        print("Enter AB")
        return

    @classmethod
    def scope_exit(cls):
        print("Exit AB")
        return


class ExampleScopeBMixIn(ScopeMixIn):

    @classmethod
    def scope_enter(cls):
        print("Enter B")
        return

    @classmethod
    def scope_exit(cls):
        print("Exit B")
        return

    def shout_out(self):
        print("Im scope ExampleScopeBMixIn")
        return

    def only_in_B(self):
        print("Only works in B")
        return
