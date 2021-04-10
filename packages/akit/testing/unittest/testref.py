"""
.. module:: testref
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the base :class:`TestRef` type used to reference to
        tests that will be included into an a test execution graph.

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

from akit.testing.unittest.testcontainer import TestContainer
class TestRef:
    """
        The :class:`TestRef` objects are used to refer to a reference to a test.  We use :class:`TestRef` instances
        to reference the tests that are going to be run so we can control the lifespan of test case instances
        and control our memory consumption during test runs with large collections of test cases.

        The :class:`TestRef` object allows us to delay the creation of test runtime instance data and state until it is
        necessary to instantiate it and allows us to cleanup the runtime instance and state as soon as it is no longer
        being used.
    """

    def __init__(self, testcontainer: TestContainer, testmeth: str):
        """
            Initializes the test reference object.

            :param testcontainer: The class of the test object that is being created.
            :param testmeth: The method on the test container
        """
        self.testcontainer = testcontainer
        self.testmeth = testmeth
        self.testpack = None
        return

    @property
    def test_name(self) -> str:
        """
            The fully qualified name of the test that is referenced.
        """
        tc = self.testcontainer
        test_name = "%s@%s#%s" % (tc.__module__, tc.__name__, self.testmeth.__name__)
        return test_name

    def create_instance(self, recorder):
        """
            Method used to create and initialize an instance of the :class:`TestContainer` object and method that
            is referred to by this :class:`TestRef` object.
        """
        testinst = self.testcontainer(self.testmeth, recorder)
        return testinst

    def __str__(self):
        return self.test_name
