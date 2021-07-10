from typing import Callable, Type

from akit.testing.testplus.resourcelifespan import ResourceLifespan
from akit.testing.testplus.registration.sourcebase import SourceBase

class ResourceSource(SourceBase):

    def __init__(self, source_func: Callable, resource_type: Type, constraints: dict):
        SourceBase.__init__(self, source_func, resource_type, constraints)
        return
