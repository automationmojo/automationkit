

from akit.xlogging.foundations import getAutomatonKitLogger

from .resources import (
    integration,
    resource,
    scope
)

from .parameters import (
    originate_parameter,
    param
)

logger = getAutomatonKitLogger()

__all__ = [
    originate_parameter,
    integration,
    logger,
    param,
    resource,
    scope
]
