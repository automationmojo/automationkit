from typing import Callable, Type

import inspect

from akit.testing.testplus.resourcelifespan import ResourceLifespan

class ResourceSource:
    def __init__(self, source_func: Callable, resource_type: Type, constraints: dict):
        self._resource_type = resource_type
        self._source_func = source_func
        self._constraints = constraints
        return

    @property
    def constraints(self) -> dict:
        return self._constraints

    @property
    def module_name(self) -> str:
        return self._source_func.__module__

    @property
    def resource_type(self) -> Type:
        return self._resource_type

    @property
    def source_function(self) -> Callable:
        return self._source_func

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self._source_func)

    @property
    def key(self) -> str:
        source = self._source_func
        idstr = "{}#{}!{}".format(source.__module__, source.__name__, self._constraints)
        return idstr
