
from akit.exceptions import AKitSkipError

def test_raises_exception():
    raise TimeoutError("Test timeout error.")
    return

def test_raises_assertion():
    assert False, "Test assert failure."
    return

def test_raises_skip():
    raise AKitSkipError(reason="Test skip.", bug="SWPBL-12345")
    return
