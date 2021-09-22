
from akit.testing.unittest.scopecoupling import ScopeCoupling

class ExampleScopeACoupling(ScopeCoupling):

    @classmethod
    def scope_enter(cls):
        print("Enter A")
        return

    @classmethod
    def scope_exit(cls):
        print("Exit A")
        return

    def shout_out(self):
        print("Im scope ExampleScopeACoupling")
        return


class ExampleScopeAACoupling(ExampleScopeACoupling):

    @classmethod
    def scope_enter(cls):
        print("Enter AA")
        return

    @classmethod
    def scope_exit(cls):
        print("Exit AA")
        return


class ExampleScopeABCoupling(ExampleScopeACoupling):

    @classmethod
    def scope_enter(cls):
        print("Enter AB")
        return

    @classmethod
    def scope_exit(cls):
        print("Exit AB")
        return


class ExampleScopeBCoupling(ScopeCoupling):

    @classmethod
    def scope_enter(cls):
        print("Enter B")
        return

    @classmethod
    def scope_exit(cls):
        print("Exit B")
        return

    def shout_out(self):
        print("Im scope ExampleScopeBCoupling")
        return

    def only_in_B(self):
        print("Only works in B")
        return
