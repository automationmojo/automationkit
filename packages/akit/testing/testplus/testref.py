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

from types import FunctionType

class TestRef:
    """
        The :class:`TestRef` objects are used to refer to a reference to a test.  We use :class:`TestRef` instances
        to reference the tests that are going to be run so we can control the lifespan of test case instances
        and control our memory consumption during test runs with large collections of test cases.

        The :class:`TestRef` object allows us to delay the creation of test runtime instance data and state until it is
        necessary to instantiate it and allows us to cleanup the runtime instance and state as soon as it is no longer
        being used.
    """

    def __init__(self, testfunc: FunctionType):
        """
            Initializes the test reference object.

            :param testcontainer: The class of the test object that is being created.
            :param testmeth: The method on the test container
        """
        self._test_function = testfunc
        return

    @property
    def test_function(self):
        """
            The test function 
        """
        return self._test_function

    @property
    def test_name(self) -> str:
        """
            The fully qualified name of the test that is referenced.
        """
        tf = self._test_function
        test_name = "%s#%s" % (tf.__module__, tf.__name__)
        return test_name

    def __str__(self):
        return self.test_name
