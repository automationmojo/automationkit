
import random

import akit.testing.testplus as testplus


@testplus.resource()
def random_integer() -> int:
    return random.randint(0, 10)

def test_dolby50_a(apod, ht_room, websrv):
    return

@testplus.param(random_integer, identifier="rint")
def test_dolby50_b(apod, ht_room, websrv, rint):
    return
