
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

            self._scope_functions = {}
            self._scope_subscriptions = {}

        return

    def register_scope_function(self, scope_function: "ScopeFunction"):
        key = scope_function.key
        
        if key not in self._scope_subscriptions:
            self._scope_functions[key] = scope_function

        return

    def register_scope_subscription(self, subscription: "ScopeSubscription"):
        key = subscription.key
        
        if key not in self._scope_subscriptions:
            self._scope_subscriptions[key] = subscription

        return

resource_registry = ResourceRegistry()
