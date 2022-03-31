
from typing import Callable

from akit.coupling.integrationcoupling import IntegrationCoupling
from akit.testing.testplus.registration.sourcebase import SourceBase

class IntegrationSource(SourceBase):

    def __init__(self, source_func: Callable, integration_type: IntegrationCoupling, constraints: dict):
        SourceBase.__init__(self, source_func, None, integration_type, constraints)
        return
