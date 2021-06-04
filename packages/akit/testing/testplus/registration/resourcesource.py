from typing import Callable, Type

import inspect

from akit.testing.testplus.resourcelifespan import ResourceLifespan

class ResourceSource:
    def __init__(self, source: Callable, resource_type: Type, life_span: ResourceLifespan, constraints: dict):
        self._life_span = life_span
        self._resource_type = resource_type
        self._source = source
        self._constraints = constraints
        return

    @property
    def constraints(self) -> dict:
        return self._constraints

    @property
    def life_span(self) -> ResourceLifespan:
        return self._life_span

    @property
    def module_name(self) -> str:
        return self._source.__module__

    @property
    def resource_type(self) -> Type:
        return self._resource_type

    @property
    def source(self) -> Callable:
        return self._source

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self._source)

    @property
    def key(self) -> str:
        source = self._source
        idstr = "{}#{}!{}".format(source.__module__, source.__name__, self._constraints)
        return idstr
