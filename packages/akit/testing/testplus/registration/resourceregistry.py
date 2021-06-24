
from typing import Union

from akit.exceptions import AKitSemanticError
from akit.testing.testplus.registration.integrationsource import IntegrationSource
from akit.testing.testplus.registration.resourcesource import ResourceSource
from akit.testing.testplus.registration.scopesource import ScopeSource
from akit.testing.testplus.registration.resourcesubscription import ResourceSubscription

RESOURCE_KEY_FORMAT = "{}@{}:{}"

class ResourceRegistry():
    _instance = None
    _initialized = False

    def __new__(cls):
        """
            Constructs new instances of the FactoryRegistry object.
        """
        if cls._instance is None:
            cls._instance = super(ResourceRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
            Initializes the SubscriptionRegistry object the first time this singleton is created.
        """
        thisType = type(self)

        if not thisType._initialized:
            thisType._initialized = True

            self._integration_source = {}
            self._resource_source = {}
            self._scope_source = {}
            self._subscriptions = {}
            self._wellknowns = {}

        return

    def lookup_resource_source(self, source_func):
        source = None

        if source_func in self._integration_source:
            source = self._integration_source[source_func]
        elif source_func in self._scope_source:
            source = self._scope_source[source_func]
        elif source_func in self._resource_source:
            source = self._resource_source[source_func]

        return source

    def lookup_wellknown_parameter(self, identifier, query_scope):

        subscription = None

        if identifier in self._wellknowns:
            candidate_table = self._wellknowns[identifier]

            longest_match_skey = None
            for skey, sitem in candidate_table.keys():
                if query_scope.startswith(skey):
                    if longest_match_skey is not None:
                        if len(skey) > len(longest_match_skey):
                            longest_match_skey = skey
                    else:
                        longest_match_skey = skey

            if longest_match_skey is not None:
                subscription = candidate_table[longest_match_skey]

        return subscription

    def lookup_subscriptions(self, subscriber):
        subscriptions = self._subscriptions.get(subscriber, {})
        return subscriptions

    def register_integration_source(self, source: IntegrationSource):

        source_func = source.source_function

        if source_func not in self._integration_source:
            self._integration_source[source_func] = source

        return

    def register_resource_source(self, source: ResourceSource):

        source_func = source.source_function
        
        if source_func not in self._resource_source:
            self._resource_source[source_func] = source

        return

    def register_scope_source(self, source: ScopeSource):

        source_func = source.source_function

        if source_func not in self._scope_source:
            self._scope_source[source_func] = source

        return

    def register_subscription(self, subscription: ResourceSubscription):

        subscriber = subscription.subscriber_function

        params = None
        if subscriber not in self._subscriptions:
            params = {}
            self._subscriptions[subscriber] = params
        else:
            params = self._subscriptions[subscriber]

        param_name = subscription.identifier
        if param_name in params:
            errmsg = "The parameter {} has already been declared for function {}.".format(
                param_name, subscriber.__name__)
            raise AKitSemanticError(errmsg)

        params[param_name] = subscription

        return

    def register_wellknown_parameter(self, identifier, assigned_scope, subscription: ResourceSubscription):

        candidate_table = None
        if identifier not in self._wellknowns:
            candidate_table = {}
            self._wellknowns[identifier] = candidate_table
        else:
            candidate_table = self._wellknowns[identifier]

        if assigned_scope in candidate_table:
            errmsg = "A wellknown variable '{}' has already been assigned to scope '{}'.".format(identifier, assigned_scope)
            raise AKitSemanticError(errmsg)

        candidate_table[assigned_scope] = subscription

        return


resource_registry = ResourceRegistry()

