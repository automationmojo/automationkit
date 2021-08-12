
from typing import Callable

from akit.testing.testplus.resourcelifespan import ResourceLifespan

from akit.testing.testplus.scopemixin import ScopeMixIn
from akit.testing.testplus.registration.sourcebase import SourceBase

class ScopeSource(SourceBase):

    def __init__(self, source_func: Callable, scope_type: ScopeMixIn, constraints: dict):
        SourceBase.__init__(self, source_func, scope_type, constraints)
        self._source_func = source_func
        return
