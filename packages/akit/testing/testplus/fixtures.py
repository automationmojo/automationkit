
from typing import Any, Callable, Iterable, Literal, Optional, TypeVar, Union

_FixtureScope = Literal["session", "package", "module", "class", "function"]

_FixtureFunction = TypeVar("_FixtureFunction", bound=Callable[..., object])

class FixtureReference:
    def __init__(self, fixture_function):
        self._fixture_function = fixture_function
        return

def fixture(fobj: _FixtureFunction, scope: _FixtureScope = "function",
        *,
        params: Optional[Iterable[object]] = None,_FixtureScope,
        autouse: bool = False,
        ids: Optional[
            Union[
                Iterable[Union[None, str, float, int, bool]],
                Callable[[Any], Optional[object]],
            ]
        ] = None,
        name: Optional[str] = None,):

    return fobj
