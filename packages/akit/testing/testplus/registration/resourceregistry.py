
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

        return

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

        param_name = subscription.identifier
        if param_name in params:
            errmsg = "The parameter {} has already been declared for function {}.".format(
                param_name, subscriber.__name__)
            raise AKitSemanticError(errmsg)

        params[param_name] = subscription

        return

resource_registry = ResourceRegistry()

