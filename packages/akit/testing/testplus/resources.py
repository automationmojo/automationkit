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


from typing import Callable, Dict, Generator, Optional, TypeVar, Union

import enum
import inspect
import os

from akit.compat import NoneType

from akit.mixins.base import BaseMixIn
from akit.mixins.integration import IntegrationMixIn
from akit.mixins.scope import ScopeMixIn

from akit.exceptions import AKitSemanticError

from akit.testing.testplus.registration.resourceregistry import RESOURCE_KEY_FORMAT, resource_registry

from akit.testing.testplus.resourcelifespan import ResourceLifespan
from akit.testing.testplus.registration.integrationsource import IntegrationSource
from akit.testing.testplus.registration.resourcesource import ResourceSource
from akit.testing.testplus.registration.resourcesubscription import ResourceSubscription
from akit.testing.testplus.registration.scopesource import ScopeSource

_IntegrationSubscriberType = TypeVar("_IntegrationSubscriberType", bound=Callable[..., object])


def integration(*, constraints: Optional[dict]=None):
    """
        The `integration` decorator is used to declare a function as the source
        of an integration resource.
    """
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints

        signature = inspect.signature(source_function)
        integration_context = signature.return_annotation

        resource_type = None

        if integration_context._name == "Generator":
            ra_yield_type, ra_send_type, ra_return_type = integration_context.__args__
            if ra_yield_type is not NoneType:
                resource_type = ra_return_type
            elif ra_return_type is not NoneType:
                resource_type = ra_return_type
        elif issubclass(integration_context, IntegrationMixIn):
            resource_type = integration_context
        else:
            raise AKitSemanticError("You must pass a IntegrationMixIn derived object.")
        
        if resource_type is not None:

            if issubclass(resource_type, IntegrationMixIn):
                raise AKitSemanticError("The 'integration' decorator can only be used on resources that inherit from the 'IntegrationMixIn'.")

            isource = IntegrationSource(source_function, resource_type)
            resource_registry.register_integration_source(isource)
        else:
            errmsg_lines = [
                "Unable to determine the resource type of the function which the 'integration' decorator was applied too.",
                "FUNCTION: {}".format(signature)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitSemanticError(errmsg)

        return source_function
    return decorator

def param(source, *, identifier: Optional[None], constraints: Optional[dict]=None):
    def decorator(subscriber: Callable) -> Callable:
        nonlocal source
        nonlocal identifier
        nonlocal constraints

        if identifier is None:
            identifier = source.__name__

        subscription = ResourceSubscription(identifier, subscriber, source, constraints)
        resource_registry.register_subscription(subscription)

        return subscriber
    return decorator

def resource(*, life_span: ResourceLifespan=ResourceLifespan.Session, constraints: Optional[dict]=None):
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints
        nonlocal life_span

        signature = inspect.signature(source_function)
        integration_context = signature.return_annotation

        resource_type = None

        if integration_context._name == "Generator":
            ra_yield_type, ra_send_type, ra_return_type = integration_context.__args__
            if ra_yield_type is not NoneType:
                resource_type = ra_return_type
            elif ra_return_type is not NoneType:
                resource_type = ra_return_type
        elif issubclass(integration_context, IntegrationMixIn):
            resource_type = integration_context
        else:
            raise AKitSemanticError("You must pass a IntegrationMixIn derived object.")
        
        if resource_type is not None:

            sref = ResourceSource(source_function, resource_type, life_span, constraints)
            resource_registry.register_resource_source(sref)
        else:
            errmsg_lines = [
                "Unable to determine the resource type of the function which the 'resource' decorator was applied too.",
                "FUNCTION: {}".format(signature)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitSemanticError(errmsg)

        return source_function
    return decorator

def scope(*, life_span: ResourceLifespan=ResourceLifespan.Session, constraints: Optional[dict]=None):
    """
        The `scope` decorator is used to declare a function as the source
        of an scope resource.
    """
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints
        nonlocal life_span

        signature = inspect.signature(source_function)
        integration_context = signature.return_annotation

        resource_type = None

        if integration_context._name == "Generator":
            ra_yield_type, ra_send_type, ra_return_type = integration_context.__args__
            if ra_yield_type is not NoneType:
                resource_type = ra_return_type
            elif ra_return_type is not NoneType:
                resource_type = ra_return_type
        elif issubclass(integration_context, IntegrationMixIn):
            resource_type = integration_context
        else:
            raise AKitSemanticError("You must pass a IntegrationMixIn derived object.")
        
        if resource_type is not None:

            if issubclass(resource_type, ScopeMixIn):
                raise AKitSemanticError("The 'scope' decorator can only be used on resources that inherit from the 'ScopeMixin'.")

            ssource = ScopeSource(source_function, resource_type, life_span, constraints)
            resource_registry.register_scope_source(ssource)
        else:
            errmsg_lines = [
                "Unable to determine the resource type of the function which the 'scope' decorator was applied too.",
                "FUNCTION: {}".format(signature)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitSemanticError(errmsg)

        return source_function
    return decorator
