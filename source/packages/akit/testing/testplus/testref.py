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

from typing import Any, Dict, List, OrderedDict, Optional, Sequence

from types import FunctionType

import collections
import inspect
import sys

from akit.testing.testplus.markers import MetaFilter

class TestRef:
    """
        The :class:`TestRef` objects are used to refer to a reference to a test.  We use :class:`TestRef` instances
        to reference the tests that are going to be run so we can control the lifespan of test case instances
        and control our memory consumption during test runs with large collections of test cases.

        The :class:`TestRef` object allows us to delay the creation of test runtime instance data and state until it is
        necessary to instantiate it and allows us to cleanup the runtime instance and state as soon as it is no longer
        being used.
    """

    def __init__(self, testfunc: FunctionType, monikers: List[str]=[], pivots: OrderedDict[str, Any]=collections.OrderedDict()):
        """
            Initializes the test reference object.

            :param testcontainer: The class of the test object that is being created.
            :param testmeth: The method on the test container
        """
        self._test_function = testfunc
        self._monikers = monikers
        self._pivots = pivots
        self._subscriptions = None
        self._finalized = False
        return

    @property
    def finalized(self) -> bool:
        return self._finalized

    @property
    def monikers(self) -> List[str]:
        return self._monikers

    @property
    def pivots(self) -> OrderedDict[str, Any]:
        return self._pivots

    @property
    def scope_name(self) -> str:
        return self.test_name

    @property
    def subscriptions(self):
        return self._subscriptions

    @subscriptions.setter
    def subscriptions(self, val):
        self._subscriptions = val
        return

    @property
    def test_base_name(self) -> str:
        tbname = self._test_function.__name__
        return tbname

    @property
    def test_function(self) -> FunctionType:
        """
            The test function 
        """
        return self._test_function

    @property
    def test_function_parameters(self):
        signature = inspect.signature(self._test_function)
        return signature.parameters

    @property
    def test_module_name(self) -> str:
        return self._test_function.__module__

    @property
    def test_name(self) -> str:
        """
            The fully qualified name of the test that is referenced.
        """
        tf = self._test_function
        test_name = "%s#%s" % (tf.__module__, tf.__name__)
        return test_name

    def finalize(self):
        self._finalized = True
        return

    def is_member_of_metaset(self, metafilters: Sequence[MetaFilter]):
        """
            Indicates if a test belongs to a set that is associated with a collection of metafilters.
        """
        include = True

        for mfilter in metafilters:
            if not mfilter.should_include(self._metadata):
                include = False

        return include

    def resolve_metadata(self, parent_metadata: Optional[Dict[str, str]]=None):

        reference_metadata = self._reference_metadata()

        if parent_metadata is not None:
            if reference_metadata is not None:
                self._metadata = {}
                self._metadata.update(parent_metadata)
                self._metadata.update(reference_metadata)
            else:
                self._metadata = parent_metadata
        else:
            self._metadata = reference_metadata

        return

    def _reference_metadata(self):
        """
            Looks up the metadata if any on the module associated with this group.
        """
        
        refmd = None
        if hasattr(self._test_function, "_metadata_"):
            refmd = self._test_function._metadata_

        return refmd

    def __str__(self):
        return self.test_name
