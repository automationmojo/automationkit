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


from typing import Callable, Dict, Optional, TypeVar, Union

import enum
import inspect

from akit.mixins.base import BaseMixIn
from akit.mixins.integration import IntegrationMixIn
from akit.mixins.scope import ScopeMixIn

from akit.exceptions import AKitSemanticError

from akit.testing.testplus.resourceregistry import RESOURCE_KEY_FORMAT, resource_registry

class ResourceLifespan(str, enum.Enum):
    Session = "session"
    Package = "package"
    Test = "test"

_ScopeSubscriberType = TypeVar("_ScopeSubscriberType", bound=Callable[..., object])

class ScopeFunction:
    def __init__(self, identifier: str, scope_function: Callable, life_span: ResourceLifespan):
        self._identifier = identifier
        self._life_span = life_span
        self._scope_function = scope_function
        return

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def life_span(self) -> ResourceLifespan:
        return self._life_span

    @property
    def module_name(self) -> str:
        return self._scope_function.__module__

    @property
    def scope_function(self) -> Callable:
        return self._scope_function

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self._scope_function)

    @property
    def key(self) -> str:
        idstr = RESOURCE_KEY_FORMAT.format(self.module_name, self._identifier, self._scope_function)
        return idstr

class ScopeSubscription:
    def __init__(self, identifier: str, subscriber: _ScopeSubscriberType, scope: ScopeMixIn, life_span: ResourceLifespan):
        self._identifier = identifier
        self._life_span = life_span
        self._scope = scope
        self._subscriber = subscriber
        return

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def life_span(self) -> ResourceLifespan:
        return self._life_span

    @property
    def module_name(self) -> str:
        return self._subscriber.__module__

    @property
    def scope(self) -> ScopeMixIn:
        return self._scope

    @property
    def subscriber(self) -> _ScopeSubscriberType:
        return self._subscriber

    @property
    def subscriber_signature(self) -> inspect.Signature:
        return inspect.signature(self._subscriber)

    @property
    def key(self) -> str:
        idstr = RESOURCE_KEY_FORMAT.format(self.module_name, self._identifier, self._scope)
        return idstr

def scope_function(*, identifier: Optional[str] = None, life_span: ResourceLifespan=ResourceLifespan.Session, constraints: Dict = None):
    def decorator(scope_function: Callable) -> Callable:
        nonlocal identifier

        if callable(scope_function):
            identifier = scope_function.__name__
        else:
            raise AKitSemanticError("You must pass a Callable object.")
        
        sref = ScopeFunction(identifier, scope_function, life_span)
        resource_registry.register_scope_function(sref)

        return scope_function
    return decorator

def scope(scope_context: ScopeMixIn, *, identifier: Optional[str] = None, life_span: ResourceLifespan=ResourceLifespan.Session, constraints: Dict = None):
    def decorator(subscriber: _ScopeSubscriberType) -> _ScopeSubscriberType:
        nonlocal identifier
        nonlocal scope_context

        if issubclass(scope_context, ScopeMixIn):
            if identifier is None:
                if hasattr(scope_context, 'identifier'):
                    identifier = scope_context.identifier
                else:
                    identifier = scope_context.__name__ 
        else:
            raise AKitSemanticError("You must pass a ScopeMixIn derived object.")
        
        sref = ScopeSubscription(identifier, subscriber, scope_context, life_span)
        resource_registry.register_scope_subscription(sref)

        return subscriber
    return decorator

from akit.mixins.upnpcoordinatorintegration import UpnpCoordinatorIntegration

class AutomationPod(UpnpCoordinatorIntegration):
    """
    """
    identifier = "apod"

@scope(AutomationPod, constraints={})
@scope_function()
def hthroom(apod):
    return

def test_method(hthroom):
    return
