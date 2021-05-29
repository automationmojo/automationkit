
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
    
    def register_integration_source(self, source: IntegrationSource):

        key = source.key
        
        if key not in self._integration_source:
            self._integration_source[key] = source

        return

    def register_resource_source(self, source: ResourceSource):

        key = source.key
        
        if key not in self._resource_source:
            self._resource_source[key] = source

        return

    def register_scope_source(self, source: ScopeSource):

        key = source.key
        
        if key not in self._scope_source:
            self._scope_source[key] = source

        return

    def register_subscription(self, subscription: ResourceSubscription):
        key = subscription.key
        
        if key not in self._subscriptions:
            self._subscriptions[key] = subscription

        return

resource_registry = ResourceRegistry()

