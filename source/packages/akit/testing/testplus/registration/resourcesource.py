from typing import Callable, Union, Type

from akit.testing.testplus.resourcelifespan import ResourceLifespan
from akit.testing.testplus.registration.sourcebase import SourceBase

class ResourceSource(SourceBase):

    def __init__(self, source_func: Callable, query_func: Union[Callable, None], resource_type: Type, constraints: dict):
        SourceBase.__init__(self, source_func, query_func, resource_type, constraints)
        return
