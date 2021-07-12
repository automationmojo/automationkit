
from typing import Dict, List, Union

import inspect
import os

from akit.exceptions import AKitSemanticError, AKitUnknownParameterError
from akit.mixins.integration import IntegrationMixIn
from akit.mixins.scope import ScopeMixIn

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

            self._unknown_parameters = {}
            self._identifier_table = {}

        return

    @property
    def identifier_table(self):
        return self._identifier_table

    @property
    def unknown_parameters(self):
        return self._unknown_parameters

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

    def perform_parameter_resolution(self, test_references: Dict[str, TestRef]):

        self._unknown_parameters = {}
        self._identifier_table = {}

        integration_table = {}
        scope_table = {}

        # Go through all of the integration sources and perform parameter resolution
        # on any parameters that are feeding the integration sources.
        for source_info in self._integration_source.values():
            missing_params = []
            subscriber_func = source_info.source_function
            self._resolve_subscriber_parameters(subscriber_func, missing_params)

            if subscriber_func in self._subscriptions_table:
                source_info.subscriptions = self._subscriptions_table[subscriber_func]

            if len(missing_params) > 0:
                self._unknown_parameters[source_info.source_name] = missing_params

        # Go through all of the scope sources and perform parameter resolution
        # on any parameters that are feeding the scope sources.
        for source_info in self._scope_source.values():
            missing_params = []
            subscriber_func = source_info.source_function
            self._resolve_subscriber_parameters(subscriber_func, missing_params)

            if subscriber_func in self._subscriptions_table:
                source_info.subscriptions = self._subscriptions_table[subscriber_func]

            if len(missing_params) > 0:
                self._unknown_parameters[source_info.source_name] = missing_params

        # Go through all of the resource sources and perform parameter resolution
        # on any parameters that are feeding the scope sources.
        for source_info in self._resource_source.values():
            missing_params = []
            subscriber_func = source_info.source_function
            self._resolve_subscriber_parameters(subscriber_func, missing_params)

            if subscriber_func in self._subscriptions_table:
                source_info.subscriptions = self._subscriptions_table[subscriber_func]

            if len(missing_params) > 0:
                self._unknown_parameters[source_info.source_name] = missing_params

        # Go through all of the Test References and perform parameter resolution on
        # all the parameters.
        for _, test_ref in test_references.items():
            missing_params= []

            subscriber_func = test_ref.test_function
            self._resolve_subscriber_parameters(subscriber_func, missing_params)

            if subscriber_func in self._subscriptions_table:
                test_ref.subscriptions = self._subscriptions_table[subscriber_func]

            if len(missing_params) > 0:
                self._unknown_parameters[test_ref.test_name] = missing_params

        # Go through all of the test reference functions.  We want to collect a table of
        # all of the integration fixtures and scope fixtures that might be used, for the
        # purpose of letting them participate in the startup of the test framework and
        # test environment.
        for _, test_ref in test_references.items():
            usage_ledger = {}
            subscriber_func = test_ref.test_function
            self._collect_integrations_and_scopes_for_subscriber(subscriber_func, integration_table, scope_table, usage_ledger)

        return integration_table, scope_table, self._unknown_parameters

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

    def _collect_integrations_and_scopes_for_subscriber(self, subscriber_func, integration_table, scope_table, usage_ledger):
        """
            Look at the subscriptions for the subscriber function provide in order to find the :class:`IntegrationMixIn`
            and :class:`ScopeMixIn` types that need to be involved in the startup of the test framework and
            test environment.
        """
        params = self._subscriptions_table[subscriber_func]
        for pname, subscription in params.items():

            usage_key = "{}: {}".format(pname, str(subscription))

            param_resource_type = subscription.source_resource_type
            source_function = subscription.source_function
            if source_function in usage_ledger:
                first_usage = usage_ledger[source_function]
                err_msg_lines = [
                    "Circular dependency detected.  The same source function should not be used twice in the same resource creation stack."
                    "FIRST USAGE: {}".format(first_usage),
                    "SECOND USAGE: {}".format(usage_key)
                ]
                err_msg = os.linesep.join(err_msg_lines)
                raise AKitSemanticError(err_msg)

            usage_ledger[source_function] = usage_key
            if issubclass(param_resource_type, IntegrationMixIn):
                # There should never be more than one fixture with the same well-known or declared name in
                # the same collection of tests.
                integration_table[source_function] = param_resource_type
            elif issubclass(param_resource_type, ScopeMixIn):
                scope_table[source_function] = param_resource_type

            self._collect_integrations_and_scopes_for_subscriber(source_function, integration_table, scope_table, usage_ledger)
            del usage_ledger[source_function]

        return

    def _resolve_subscriber_parameters(self, subscriber_function, missing_params):

        subscriber_module_name = subscriber_function.__module__

        params = None
        if subscriber_function in self._subscriptions_table:
            params = self._subscriptions_table[subscriber_function]
        else:
            params = {}
            self._subscriptions_table[subscriber_function] = params

        subscriber_arg_spec = inspect.getfullargspec(subscriber_function)
        subscriber_args_list = subscriber_arg_spec.args
        if len(subscriber_args_list) > 0:

            for nxt_arg in subscriber_args_list:
                if nxt_arg not in params:
                    # If we don't find a parameter in the subscription
                    # parameters then we need to look in the well-known
                    # parameters and create a subscription for any
                    # well-known parameters.
                    sub_template = self.lookup_wellknown_parameter(nxt_arg, subscriber_module_name)
                    if sub_template is not None:
                        subscription = sub_template.clone_subscription(subscriber_function)
                        params[nxt_arg] = subscription
                    else:
                        missing_params.append(nxt_arg)

                if nxt_arg in params:
                    subscriber = params[nxt_arg]

                    reference_list = None
                    if nxt_arg not in self._identifier_table:
                        reference_list = set()
                        self._identifier_table[nxt_arg] = reference_list
                    else:
                        reference_list = self._identifier_table[nxt_arg]

                    reference_list.add(subscriber)

        return

resource_registry = ResourceRegistry()

