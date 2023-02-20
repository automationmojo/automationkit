__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

TIMEDELTA_RENEWAL_WINDOW = 120

from akit.aspects import AspectsUPnP

UPNP_CALL_COMPLETION_TIMEOUT = 30
UPNP_CALL_COMPLETION_INTERVAL = 5

UPNP_CALL_INACTIVITY_TIMEOUT = 30
UPNP_CALL_INACTIVITY_INTERVAL = 1

DEFAULT_UPNP_CALL_ASPECTS = AspectsUPnP(
    completion_timeout=UPNP_CALL_COMPLETION_TIMEOUT,
    completion_interval=UPNP_CALL_COMPLETION_INTERVAL,
    inactivity_timeout=UPNP_CALL_INACTIVITY_TIMEOUT,
    inactivity_interval=UPNP_CALL_INACTIVITY_INTERVAL)