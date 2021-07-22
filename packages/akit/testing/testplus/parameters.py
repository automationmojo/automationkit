
from typing import Callable, Dict, Optional

import inspect

from akit.exceptions import AKitSemanticError
from akit.mixins.integration import IntegrationMixIn
from akit.mixins.scope import ScopeMixIn

from akit.testing.testplus.registration.resourceregistry import resource_registry

from akit.testing.testplus.registration.integrationsource import IntegrationSource
from akit.testing.testplus.resourcelifespan import ResourceLifespan
from akit.testing.testplus.registration.parameterorigin import ParameterOrigin
from akit.testing.testplus.registration.parametersubscription import ParameterSubscription

def param(source, *, identifier: Optional[None], constraints: Optional[Dict]=None):
    def decorator(subscriber: Callable) -> Callable:
        nonlocal source
        nonlocal identifier
        nonlocal constraints

        if identifier is None:
            identifier = source.__name__

        life_span = ResourceLifespan.Test

        source_info = resource_registry.lookup_resource_source(source)

        assigned_scope = "{}#{}".format(subscriber.__module__, subscriber.__name__)

        subscription = ParameterSubscription(assigned_scope, identifier, source_info, subscriber, life_span, constraints)
        resource_registry.register_subscription(subscription)

        return subscriber
    return decorator

def originate_parameter(source_func, *, identifier: Optional[None], life_span: ResourceLifespan=None, assigned_scope: Optional[str]=None, constraints: Optional[Dict]=None):

    if source_func is None:
        errmsg = "The 'source_func' parameter cannot be 'None'."
        raise AKitSemanticError(errmsg)

    if life_span == ResourceLifespan.Test:
        errmsg = "The 'life_span' parameter cannot be 'ResourceLifespan.Test'."
        raise AKitSemanticError(errmsg)

    if identifier is None:
        identifier = source_func.__name__

    source_info = resource_registry.lookup_resource_source(source_func)
    if assigned_scope is not None:
        if isinstance(source_info, IntegrationSource):
            errmsg = "The 'assigned_scope' parameter should not be specified unless the source of the resource is of type 'scope' or 'resource'."
            raise AKitSemanticError(errmsg)
    
    caller_frame = inspect.stack()[1]
    calling_module = inspect.getmodule(caller_frame[0])
    
    if life_span is None:
        res_type = source_info.resource_type
        if issubclass(res_type, IntegrationMixIn):
            life_span = ResourceLifespan.Session
        else:
            life_span = ResourceLifespan.Package

    if life_span == ResourceLifespan.Package:
        if assigned_scope is None:
            assigned_scope = calling_module.__name__
    elif life_span == ResourceLifespan.Session:
        assigned_scope = "<session>"

    subscription = ParameterOrigin(assigned_scope, identifier, source_info, life_span, constraints)
    resource_registry.register_parameter_origin(identifier, subscription)

    return

