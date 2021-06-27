
from typing import Callable, Optional, Union

import inspect
from akit.testing.testplus.registration.sourcebase import SourceBase

from akit.testing.testplus.resourcelifespan import ResourceLifespan

class ResourceSubscription:

    def __init__(self, identifier: str, subscriber: Callable, source: SourceBase, life_span: ResourceLifespan, assigned_scope: str, constraints: Optional[dict]):
        self._identifier = identifier
        self._source = source
        self._subscriber = subscriber
        self._life_span = life_span
        self._assigned_scope = assigned_scope
        self._constraints = constraints
        return

    @property
    def assigned_scope() -> str:
        return self._assigned_scope

    @property
    def constraints(self) -> Union[dict, None]:
        return self._constraints

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def life_span(self) -> ResourceLifespan:
        return self._life_span

    @property
    def source_function(self) -> Callable:
        return self._source.source_function

    @property
    def source_id(self) -> str:
        idstr = self._source.source_id
        return idstr

    @property
    def source_module_name(self) -> str:
        return self._source.module_name

    @property
    def source_signature(self) -> inspect.Signature:
        return self._source.source_signature
    
    @property
    def subscriber_function(self) -> Callable:
        return self._subscriber

    @property
    def subscriber_signature(self) -> inspect.Signature:
        return inspect.signature(self._subscriber)

    @property
    def subscriber_key(self) -> str:
        subscriber = self._subscriber
        idstr = "{}#{}".format(subscriber.__module__, subscriber.__name__)
        return idstr
