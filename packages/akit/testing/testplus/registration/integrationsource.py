
from typing import Callable

import inspect

from akit.mixins.integration import IntegrationMixIn

class IntegrationSource:
    def __init__(self, source: Callable, integration: IntegrationMixIn):
        self._integration = integration
        self._source = source
        return

    @property
    def module_name(self) -> str:
        return self._source.__module__

    @property
    def integration(self) -> IntegrationMixIn:
        return self._integration

    @property
    def source(self) -> Callable:
        return self._source

    @property
    def source_signature(self) -> inspect.Signature:
        return inspect.signature(self._source)

    @property
    def key(self) -> str:
        idstr = "{}#{}".format(self.module_name, self._source.__name__)
        return idstr

