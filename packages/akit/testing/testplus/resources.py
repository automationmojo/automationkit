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


def register_wellknown_parameter(source, *, identifier: Optional[None], life_span: ResourceLifespan=ResourceLifespan.Session, assigned_scope: Optional[str]=None, constraints: Optional[dict]=None):

    if identifier is None:
        identifier = source.__name__

    if life_span == ResourceLifespan.Package:
            if source is None:
                package_scope = source.__module__

    elif assigned_scope is not None:
        errmsg = "The 'assigned_scope' parameter should only be used if the resource lifespan is 'ResourceLifespan.Package'."
        raise AKitSemanticError(errmsg)

    source_info = resource_registry.lookup_resource_source(source)
    if assigned_scope is not None:
        if isinstance(source_info, IntegrationSource):
            errmsg = "The 'assigned_scope' parameter should not be specified unless the source of the resource is of type 'scope' or 'resource'."
            raise AKitSemanticError(errmsg)
        elif life_span != ResourceLifespan.Package:
            errmsg = "The 'assigned_scope' parameter should not be specified unless 'life_span' is ResourceLifespan.Package."
            raise AKitSemanticError(errmsg)
    elif life_span != ResourceLifespan.Test:
        caller_frame = inspect.stack()[1]
        calling_module = inspect.getmodule(caller_frame[0])
        assigned_scope = calling_module.__name__

    subscription = ResourceSubscription(identifier, None, source, life_span, assigned_scope, constraints)
    resource_registry.register_wellknown_parameter(identifier, assigned_scope, subscription)

    return

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

        if integration_context == inspect._empty:
            errmsg = "Parameters factories or 'integration' functions must have an annotated return type."
            raise AKitSemanticError(errmsg)
        elif integration_context._name == "Generator":
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

def param(source, *, identifier: Optional[None], life_span: ResourceLifespan=ResourceLifespan.Session, assigned_scope: Optional[str]=None, constraints: Optional[dict]=None):
    def decorator(subscriber: Callable) -> Callable:
        nonlocal source
        nonlocal identifier
        nonlocal life_span
        nonlocal assigned_scope
        nonlocal constraints

        if identifier is None:
            identifier = source.__name__

        if life_span == ResourceLifespan.Package:
                if source is None:
                    package_scope = source.__module__

        elif assigned_scope is not None:
            errmsg = "The 'assigned_scope' parameter should only be used if the resource lifespan is 'ResourceLifespan.Package'."
            raise AKitSemanticError(errmsg)

        source_info = resource_registry.lookup_resource_source(source)
        if assigned_scope is not None:
            if isinstance(source_info, IntegrationSource):
                errmsg = "The 'assigned_scope' parameter should not be specified unless the source of the resource is of type 'scope' or 'resource'."
                raise AKitSemanticError(errmsg)
            elif life_span != ResourceLifespan.Package:
                errmsg = "The 'assigned_scope' parameter should not be specified unless 'life_span' is ResourceLifespan.Package."
                raise AKitSemanticError(errmsg)

        subscription = ResourceSubscription(identifier, subscriber, source, life_span, assigned_scope, constraints)
        resource_registry.register_subscription(subscription)

        return subscriber
    return decorator

def resource(*, constraints: Optional[dict]=None):
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints

        signature = inspect.signature(source_function)
        resource_context = signature.return_annotation

        resource_type = None

        if resource_context == inspect._empty:
            errmsg = "Parameters factories or 'resource' functions must have an annotated return type."
            raise AKitSemanticError(errmsg)
        elif hasattr(resource_context, "_name") and resource_context._name == "Generator":
            ra_yield_type, ra_send_type, ra_return_type = resource_context.__args__
            if ra_yield_type is not NoneType:
                resource_type = ra_return_type
            elif ra_return_type is not NoneType:
                resource_type = ra_return_type
        elif issubclass(resource_context, IntegrationMixIn):
            resource_type = resource_context
        else:
            raise AKitSemanticError("You must pass a IntegrationMixIn derived object.")
        
        if resource_type is not None:

            sref = ResourceSource(source_function, resource_type, constraints)
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

def scope(*, constraints: Optional[dict]=None):
    """
        The `scope` decorator is used to declare a function as the source
        of an scope resource.
    """
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints

        signature = inspect.signature(source_function)
        scope_context = signature.return_annotation

        resource_type = None

        if scope_context == inspect._empty:
            errmsg = "Parameters factories or 'scope' functions must have an annotated return type."
            raise AKitSemanticError(errmsg)
        elif scope_context._name == "Generator":
            ra_yield_type, ra_send_type, ra_return_type = scope_context.__args__
            if ra_yield_type is not NoneType:
                resource_type = ra_return_type
            elif ra_return_type is not NoneType:
                resource_type = ra_return_type
        elif issubclass(scope_context, ScopeMixIn):
            resource_type = scope_context
        else:
            raise AKitSemanticError("You must pass a IntegrationMixIn derived object.")
        
        if resource_type is not None:

            if issubclass(resource_type, ScopeMixIn):
                raise AKitSemanticError("The 'scope' decorator can only be used on resources that inherit from the 'ScopeMixin'.")

            ssource = ScopeSource(source_function, resource_type, constraints)
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

