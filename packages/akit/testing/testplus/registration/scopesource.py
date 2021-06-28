
from typing import Callable

import inspect

from akit.testing.testplus.resourcelifespan import ResourceLifespan

from akit.mixins.scope import ScopeMixIn
from akit.testing.testplus.registration.sourcebase import SourceBase

class ScopeSource(SourceBase):

    def __init__(self, source_func: Callable, scope_type: ScopeMixIn):
        SourceBase.__init__(self, source_func, scope_type)
        self._source_func = source_func
        return
