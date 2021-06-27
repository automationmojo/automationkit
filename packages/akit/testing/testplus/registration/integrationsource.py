
from typing import Callable

import inspect

from akit.mixins.integration import IntegrationMixIn
from akit.testing.testplus.registration.sourcebase import SourceBase

class IntegrationSource(SourceBase):
    def __init__(self, source_func: Callable, integration: IntegrationMixIn):
        SourceBase.__init__(source_func, integration)
        self._integration = integration
        return
