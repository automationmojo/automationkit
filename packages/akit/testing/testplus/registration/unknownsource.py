from typing import Callable, Type

from akit.testing.testplus.registration.sourcebase import SourceBase

class UnknownSource(SourceBase):
    """
        The :class:`UnknownSource` object is used when a parameter is declared for a
        test method of other resource function that cannot be resolved to a source
        function.  The :class:`UnknownSource` enables the test parameters to be queried
        by acting as a placeholder.
    """
    def __init__(self, source_func: Callable, resource_type: Type, constraints: dict):
        SourceBase.__init__(self, source_func, resource_type, constraints)
        return
