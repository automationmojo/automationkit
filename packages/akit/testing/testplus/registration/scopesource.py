
from typing import Callable, Union

from akit.testing.testplus.resourcelifespan import ResourceLifespan

from akit.testing.testplus.scopecoupling import ScopeCoupling
from akit.testing.testplus.registration.sourcebase import SourceBase

class ScopeSource(SourceBase):

    def __init__(self, source_func: Callable, query_func: Union[Callable, None], scope_type: ScopeCoupling, constraints: dict):
        SourceBase.__init__(self, source_func, query_func, scope_type, constraints)
        self._source_func = source_func
        return
