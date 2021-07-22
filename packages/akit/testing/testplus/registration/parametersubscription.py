
from typing import Callable, Dict, Optional, Type, Union

import inspect

from akit.testing.testplus.registration.sourcebase import SourceBase
from akit.testing.testplus.resourcelifespan import ResourceLifespan

class ParameterSubscription:

    def __init__(self, assigned_scope: str, identifier: str, source: SourceBase, subscriber: Callable, life_span: ResourceLifespan, constraints: Optional[Dict]):
        self._assigned_scope = assigned_scope
        self._identifier = identifier
        self._source = source
        self._subscriber = subscriber
        self._life_span = life_span
        self._constraints = constraints
        return

    @property
    def assigned_scope(self) -> str:
        return self._assigned_scope

    @property
    def constraints(self) -> Union[dict, None]:
        """
            Returns the most applicable constraints assoceated with this resource subscription.  If the
            subscription constraints are set then they will be used.  If the subscription constraints are
            not set and the source constraints are set, then the source constraints will be returned. If
            no constraints are applied to the subscription or the source, 'None' will be returned.
        """
        cval = None
        if self._constraints is not None:
            cval = self._constraints
        elif self._source.constraints is not None:
            cval = self._source.constraints
        return cval

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
    def source_resource_type(self) -> Type:
        return self._source.resource_type

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

    def clone_subscription(self, subscriber):
        subscription = ParameterSubscription(self._identifier, subscriber, self._source, self._life_span, self._assigned_scope, self._constraints)
        return subscription

    def describe_source(self):
        descstr = self.source_id
        cval = self.constraints
        if cval is not None:
            descstr += " constraints={}".format(repr(cval))
        return descstr