
from typing import Callable

import inspect

from akit.mixins.integration import IntegrationMixIn

class IntegrationSource:
    def __init__(self, source_func: Callable, integration: IntegrationMixIn):
        self._integration = integration
        self._source_func = source_func
        return

    @property
    def module_name(self) -> str:
        return self._source.__module__

    @property
    def integration(self) -> IntegrationMixIn:
        return self._integration

    @property
    def source_funcion(self) -> Callable:
        return self._source_func

    @property
    def source_signature(self) -> inspect.Signature:
        return inspect.signature(self._source_func)

    @property
    def key(self) -> str:
        idstr = "{}#{}".format(self.module_name, self._source_func.__name__)
        return idstr

