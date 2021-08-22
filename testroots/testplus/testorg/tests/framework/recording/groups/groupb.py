
from typing import Generator

from akit.exceptions import AKitError

from akit.testing import testplus

@testplus.resource()
def raises_error() -> Generator[int, None, None]:
    raise AKitError("Intentional failure.")

testplus.originate_parameter(raises_error, identifier="err")

def test_error_a(err):
    print("blah_a")
    return

def test_error_b(err):
    print("blah_b")
    return
