
FACTORY_KEY_FORMAT = "{}@{}:{}"

class FactoryRegistry():
    _instance = None
    _initialized = False

    def __new__(cls):
        """
            Constructs new instances of the FactoryRegistry object.
        """
        if cls._instance is None:
            cls._instance = super(FactoryRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
            Initializes the FactoryRegistry object the first time this singleton is created.
        """
        thisType = type(self)

        if not thisType._initialized:
            thisType._initialized = True

            self._integrations = {}
            self._scopes = {}

        return

    def register_integration(self, integration):
        key = integration.key

        if key not in self._integrations:
            self._integrations[key]

        return

    def register_scope(self, scope):
        key = scope.key
        
        if key not in self._scopes:
            self._scopes[key]

        return

factory_registry = FactoryRegistry()
