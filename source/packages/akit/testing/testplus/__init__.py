

from akit.xlogging.foundations import getAutomatonKitLogger

from akit.exceptions import akit_skip

from .markers import (
    mark_categories,
    mark_keywords,
    mark_priority,
    mark_descendent_categories,
    mark_descendent_keywords,
    mark_descendent_priority
)

from .parameters import (
    originate_parameter,
    param
)


from .resources import (
    integration,
    resource,
    scope
)

logger = getAutomatonKitLogger()

skip_test = akit_skip

__all__ = [
    originate_parameter,
    integration,
    logger,
    mark_categories,
    mark_keywords,
    mark_priority,
    mark_descendent_categories,
    mark_descendent_keywords,
    mark_descendent_priority,
    param,
    resource,
    scope,
    skip_test
]
