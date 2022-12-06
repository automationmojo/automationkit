
import random

import akit.testing.testplus as testplus


@testplus.resource()
def random_integer(apod) -> int:
    yield random.randint(0, 10)

def test_dolby50_a(apod, ht_room, websrv):
    print("Ran test 'test_dolby50_a'")
    return

@testplus.param(random_integer, identifier="rint")
def test_dolby50_b(apod, ht_room, websrv, rint):
    print("Ran test 'test_dolby50_b'")
    return
