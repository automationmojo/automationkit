
from typing import Dict, List, Union

import inspect

from akit.exceptions import AKitSemanticError

from akit.testing.testplus.registration.integrationsource import IntegrationSource
from akit.testing.testplus.registration.resourcesource import ResourceSource
from akit.testing.testplus.registration.scopesource import ScopeSource
from akit.testing.testplus.registration.resourcesubscription import ResourceSubscription
from akit.testing.testplus.testref import TestRef

RESOURCE_KEY_FORMAT = "{}@{}:{}"

class ResourceRegistry():
    _instance = None
    _initialized = False

    def __new__(cls):
        """
            Constructs new instances of the FactoryRegistry object.

            1. During environment startup, the resource decorators are executed
               and the source functions are registered and available for consumption
               via a query interface or by executing code

               Also, during starup, the calls to register wellknown parameters are made
               as well as the 'param' decorators are executed in order to establish the
               parameter lookup tables to identify the parameters that are available to
               be passed to functions for code.

            2. At the start of the discovery and collection phase of test execution, the
               'perform_consolidation' API is called and we go through and remove any
               resource declarations that do not have a subscription or are not registered
               as a well-known parameter.  We can also accept a 'Set' of expected parameter
               which we can use to further reduce the information cache to only include
               sources that are being consumed by the executing code.

            3. After we know all of the test references, we can walk through all of the test
               references, create subscriptions for any parameters that are not currently assigned
               to the tests based on the scope of the test and based on the closest well-known
               parameter in the scope hierarchy of the tests.
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

            # There are two tables that are used to manage parameter subscription.
            
            # The self._subscription table handles direct subsciptions, where a 'param'
            # decorator was used to directly link a resource source function with a
            # subscriber function
            self._subscriptions_table = {}

            # The self._wellknown_resource_table is used to store subscription templates
            # that assign a parameter name to a source function for a given scope.
            # Resources declared as wellknown resources are later linked dynamically to
            # the test methods that are consuming them based on closest scope and if a
            # parameter has already been linked for a given subscriber. 
            self._wellknown_resource_table = {}

        return

    def lookup_resource_table_by_scope(self, scope_name):

        resource_table = {}

        for identifier, scope_table in self._wellknown_resource_table.items():
            if scope_name in scope_table:
                resource_table[identifier] = scope_table[scope_name]

        return resource_table

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

        if identifier in self._wellknown_resource_table:
            candidate_table = self._wellknown_resource_table[identifier]

            longest_match_skey = None
            for skey in candidate_table.keys():
                if query_scope.startswith(skey):
                    if longest_match_skey is not None:
                        if len(skey) > len(longest_match_skey):
                            longest_match_skey = skey
                    else:
                        longest_match_skey = skey

            if longest_match_skey is not None:
                subscription = candidate_table[longest_match_skey]

        return subscription

    def lookup_subscrptions(self, subscriber):
        subscriptions = self._subscriptions_table.get(subscriber, {})
        return subscriptions

    def perform_consolidation(self, test_references: Dict[str, TestRef]):

        unknown_parameters = {}

        identifier_table = {}

        for _, test_ref in test_references.items():
            subscriber_func = test_ref.test_function

            params = None
            if subscriber_func in self._subscriptions_table:
                params = self._subscriptions_table[subscriber_func]
            else:
                params = {}
                self._subscriptions_table[subscriber_func] = params

            subscriber_arg_spec = inspect.getfullargspec(subscriber_func)
            subscriber_args_list = subscriber_arg_spec.args
            if len(subscriber_args_list) > 0:
                test_missing_params = []

                for nxt_arg in subscriber_args_list:
                    if nxt_arg not in params:
                        # If we don't find a parameter in the subscription
                        # parameters then we need to look in the well-known
                        # parameters and create a subscription for any
                        # well-known parameters.
                        test_module_name = test_ref.test_module_name
                        sub_template = self.lookup_wellknown_parameter(nxt_arg, test_module_name)
                        if sub_template is not None:
                            subscription = sub_template.clone_subscription(subscriber_func)
                            params[nxt_arg] = subscription
                        else:
                            test_missing_params.append(nxt_arg)
                
                if len(test_missing_params) > 0:
                    unknown_parameters[test_ref.test_name] = test_missing_params

        return

    def register_integration_source(self, source: IntegrationSource):
        """
            This method is called by the 'integration' decorator in order to register a
            factory function that generates an 'IntegrationMixIn' object. 
        """
        source_func = source.source_function

        if source_func not in self._integration_source:
            self._integration_source[source_func] = source

        return

    def register_resource_source(self, source: ResourceSource):
        """
            This method is called by the 'resource' decorator in order to register a
            factory function that generate an arbitrary parameter resources.
        """
        source_func = source.source_function
        
        if source_func not in self._resource_source:
            self._resource_source[source_func] = source

        return

    def register_scope_source(self, source: ScopeSource):
        """
            This method is called by the 'scope' decorator in order to register a factory
            function that generates an 'ScopeMixIn' object. 
        """
        source_func = source.source_function

        if source_func not in self._scope_source:
            self._scope_source[source_func] = source

        return

    def register_subscription(self, subscription: ResourceSubscription):

        subscriber = subscription.subscriber_function

        params = None
        if subscriber not in self._subscriptions_table:
            params = {}
            self._subscriptions_table[subscriber] = params
        else:
            params = self._subscriptions_table[subscriber]

        param_name = subscription.identifier
        if param_name in params:
            errmsg = "The parameter {} has already been declared for function {}.".format(
                param_name, subscriber.__name__)
            raise AKitSemanticError(errmsg)

        params[param_name] = subscription

        return

    def register_wellknown_parameter(self, identifier, assigned_scope, subscription: ResourceSubscription):

        candidate_table = None
        if identifier not in self._wellknown_resource_table:
            candidate_table = {}
            self._wellknown_resource_table[identifier] = candidate_table
        else:
            candidate_table = self._wellknown_resource_table[identifier]

        if assigned_scope in candidate_table:
            errmsg = "A wellknown variable '{}' has already been assigned to scope '{}'.".format(identifier, assigned_scope)
            raise AKitSemanticError(errmsg)

        candidate_table[assigned_scope] = subscription

        return


resource_registry = ResourceRegistry()

