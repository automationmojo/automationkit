"""
.. module:: decorations
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A set of standardized decorations that are utilized to declare integrations and scopes.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


from typing import Callable, Literal, Optional, TypeVar

import inspect

from akit.testing.testplus.factoryregistry import FACTORY_KEY_FORMAT, factory_registry


_ResourceScope = Literal["session", "package", "module", "class", "function"]

_IntegrationFactory = TypeVar("_IntegrationFactory", bound=Callable[..., object])
_ScopeFactory = TypeVar("_ScopeFactory", bound=Callable[..., object])


class IntegrationReference:
    def __init__(self, identifier: str, factory: _IntegrationFactory):
        self._identifier = identifier
        self._factory = factory
        return

    @property
    def factory(self) -> _IntegrationFactory:
        return self._factory

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def module_name(self) -> str:
        return self._factory.__module__

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self._factory)

    @property
    def key(self) -> str:
        idstr = FACTORY_KEY_FORMAT.format(self.module_name, self._identifier)
        return

def integration(ifactory: _IntegrationFactory, *, identifier: Optional[str] = None) -> _IntegrationFactory:
    if identifier is None:
        identifier = ifactory.__name__

    iref = IntegrationReference(identifier, ifactory)
    factory_registry.register_integration(iref)

    return ifactory


class ScopeReference:
    def __init__(self, identifier: str, factory: _ScopeFactory, scope: _ResourceScope):
        self._identifier = identifier
        self._factory = factory
        self._scope = scope
        return

    @property
    def factory(self) -> _ScopeFactory:
        return self._factory

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def module_name(self) -> str:
        return self._factory.__module__

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self._factory)

    @property
    def key(self) -> str:
        idstr = FACTORY_KEY_FORMAT.format(self.module_name, self._identifier, self._scope)
        return

def scope(sfactory: _ScopeFactory, scope: _ResourceScope = "function", *, identifier: Optional[str] = None) -> _ScopeFactory:
    if identifier is None:
        identifier = sfactory.__name__

    sref = ScopeReference(identifier, sfactory, scope)
    factory_registry.register_scope(sref)

    return sfactory




