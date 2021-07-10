
from typing import Callable

from akit.mixins.integration import IntegrationMixIn
from akit.testing.testplus.registration.sourcebase import SourceBase

class IntegrationSource(SourceBase):

    def __init__(self, source_func: Callable, integration_type: IntegrationMixIn, constraints: dict):
        SourceBase.__init__(self, source_func, integration_type, constraints)
        return
