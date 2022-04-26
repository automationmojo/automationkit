
from typing import NamedTuple

class FastPingResult(NamedTuple):
    pings_sent: int
    pings_received: int
    ping_loss_rate: int
