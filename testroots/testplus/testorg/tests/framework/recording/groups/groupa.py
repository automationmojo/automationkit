
from typing import Generator

from akit.exceptions import AKitSkipError

from akit.testing import testplus

@testplus.resource()
def raises_skip() -> Generator[int, None, None]:
    raise AKitSkipError("Intentional failure.")

testplus.originate_parameter(raises_skip, identifier="skip")

def test_skip_a(skip):
    print("blah_a")
    return

def test_skip_b(skip):
    print("blah_b")
    return
