
from typing import Callable

import inspect

from akit.testing.testplus.resourcelifespan import ResourceLifespan

from akit.mixins.scope import ScopeMixIn

class ScopeSource:
    def __init__(self, source_func: Callable, scope_type: ScopeMixIn, constraints: dict):
        self._scope_type = scope_type
        self._source_func = source_func
        self._constraints = constraints
        return

    @property
    def constraints(self) -> dict:
        return self._constraints

    @property
    def module_name(self) -> str:
        return self._source.__module__

    @property
    def source_function(self) -> Callable:
        return self._source_func

    @property
    def scope_type(self) -> ScopeMixIn:
        return self._scope_type

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self._source)

    @property
    def key(self) -> str:
        source = self._source
        idstr = "{}#{}!{}".format(source.__module__, source.__name__, self._constraints)
        return idstr

