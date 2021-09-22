"""
"""

import akit.environment.activate # pylint: disable=unused-import

from akit.testing.unittest.testpack import TestPack
from akit.testing.unittest.testcontainer import PositiveTestContainer

from testorg.scopes.examplescopes import ExampleScopeAACoupling, ExampleScopeABCoupling, ExampleScopeBCoupling


class TestPackageAA(TestPack, ExampleScopeAACoupling):
    """
    """

class TestPackageAB(TestPack, ExampleScopeABCoupling):
    """
    """

class TestPackB(TestPack, ExampleScopeBCoupling):
    """
    """

class TestExampleAA(PositiveTestContainer, TestPackageAA):

    def test_hello_world_aa(self):
        print("Hello World, AA")
        return

class TestExampleAB(PositiveTestContainer, TestPackageAB):

    def test_hello_world_ab(self):
        print("Hello World, AB")
        return

class TestExampleB(PositiveTestContainer, TestPackB):

    def test_hello_world_b(self):
        print("Hello World, B")
        return

    def test_failure_b(self):
        """
            Test that raises an intentional failure.
        """
        raise AssertionError("Intentional failure")
        pass



if __name__ == "__main__":
    from akit.testing.unittest.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
