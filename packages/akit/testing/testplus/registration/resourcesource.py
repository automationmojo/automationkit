from typing import Callable, Type

import inspect

from akit.testing.testplus.resourcelifespan import ResourceLifespan
from akit.testing.testplus.registration.sourcebase import SourceBase

class ResourceSource(SourceBase):
    def __init__(self, source_func: Callable, resource_type: Type):
        SourceBase.__init__(source_func, resource_type)
        self._resource_type = resource_type
        return

    @property
    def resource_type(self) -> Type:
        return self._resource_type
