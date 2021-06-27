
from typing import Callable, Type

import inspect

class ResourceBase:

    def __init__(self, source_func: Callable):
        self._source_func = source_func
        return

    @property
    def module_name(self) -> str:
        return self._source_func.__module__


    @property
    def source_function(self) -> Callable:
        return self._source_func

    @property
    def source_signature(self) -> inspect.Signature:
        return inspect.signature(self._source_func)

    @property
    def source_id(self) -> str:
        source = self._source_func
        idstr = "{}#{}!{}".format(source.__module__, source.__name__, self._constraints)
        return idstr
