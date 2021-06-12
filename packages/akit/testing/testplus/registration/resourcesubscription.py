
from typing import Callable, Optional, Union

import inspect

from akit.testing.testplus.resourcelifespan import ResourceLifespan

class ResourceSubscription:

    def __init__(self, identifier: str, subscriber: Callable, source: Callable, constraints: Optional[dict]=None):
        self._identifier = identifier
        self._source = source
        self._subscriber = subscriber
        self._constraints = constraints
        return

    @property
    def constraints(self) -> Union[dict, None]:
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
    def source_key(self) -> str:
        source = self._source
        idstr = "{}#{}".format(source.__module__, source.__name__)
        return idstr

    @property
    def subscriber_key(self) -> str:
        subscriber = self._subscriber
        idstr = "{}#{}".format(subscriber.__module__, subscriber.__name__)
        return idstr
