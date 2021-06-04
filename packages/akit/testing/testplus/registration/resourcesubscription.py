
from typing import Callable, Type

import inspect

from akit.testing.testplus.resourcelifespan import ResourceLifespan

class ResourceSubscription:

    def __init__(self, identifier: str, subscriber: Callable, source: Callable, constraints: dict):
        self._identifier = identifier
        self._source = source
        self._subscriber = subscriber
        self._constraints = constraints
        return

    @property
    def constraints(self) -> dict:
        return self._constraints

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def source_module_name(self) -> str:
        return self._source.__module__

    @property
    def source_function(self) -> Callable:
        return self._source

    @property
    def source_signature(self) -> inspect.Signature:
        return inspect.signature(self._source)
    
    @property
    def subscriber_function(self) -> Callable:
        return self._subscriber

    @property
    def subscriber_signature(self) -> inspect.Signature:
        return inspect.signature(self._subscriber)

    @property
    def key(self) -> str:
        source = self._source
        idstr = "{}#{}!{}".format(source.__module__, source.__name__, self._constraints)
        return idstr
