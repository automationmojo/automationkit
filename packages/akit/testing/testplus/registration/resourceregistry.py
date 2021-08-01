
from typing import Dict, List, Union

import inspect
import os

from akit.exceptions import AKitSemanticError
from akit.mixins.integration import IntegrationMixIn
from akit.mixins.scope import ScopeMixIn

from akit.testing.testplus.registration.integrationsource import IntegrationSource
from akit.testing.testplus.registration.parameterorigin import ParameterOrigin
from akit.testing.testplus.registration.resourcesource import ResourceSource
from akit.testing.testplus.registration.scopesource import ScopeSource
from akit.testing.testplus.registration.parameterorigin import ParameterOrigin
from akit.testing.testplus.registration.parametersubscription import ParameterSubscription
from akit.testing.testplus.testref import TestRef

RESOURCE_KEY_FORMAT = "{}@{}:{}"

class ResourceScope:
    def __init__(self, name=None, package=None, is_test_scope=False):
        self._name = name
        self._package = package
        self._children = {}
        self._parameters = {}
        self._is_test_scope = is_test_scope
        return

    @property
    def children(self):
        return self._children

    @property
    def parameters(self):
        return self._parameters

    def add_descendent_parameter(self, assigned_scope, parameter_object):

        if self._package is not None:
            err_msg = "The 'add_descendent' API can only be called on the root package."
            raise AKitSemanticError(err_msg)

        if self._package is None and assigned_scope == "<session>":
            identifier = parameter_object.identifier
            self._parameters[identifier] =  parameter_object
        else:
            is_test_scope = False
            if assigned_scope.find("#") > -1:
                is_test_scope = True
                assigned_scope = assigned_scope.replace("#", ".")
            to_walk_list = assigned_scope.split(".")
            path_stack = []

            self._add_descendent_parameter(parameter_object, to_walk_list, path_stack, is_test_scope)

        return

    def has_descendent_parameter(self, assigned_scope: str, identifier: str):
        rtnval = False

        if self._package is None and assigned_scope == "<session>":
            if identifier in self._parameters:
                rtnval = True
        else:
            assigned_scope = assigned_scope.replace("#", ".")
            to_walk_list = assigned_scope.split(".")

            rtnval = self._has_descendent_parameter(to_walk_list, identifier)

        return rtnval

    def lookup_scope(self, scope_name):

        scope_found = None
        if self._package is None and scope_name == "<session>":
            scope_found = self
        else:
            scope_name = scope_name.replace("#", ".")
            to_walk_list = scope_name.split(".")

            if len(to_walk_list) > 0:
                scope_found = self._lookup_scope(to_walk_list)

        return scope_found

    def _add_descendent_parameter(self, parameter_object, to_walk_list: List[str], path_stack: List[str], is_test_scope):

        curr_leaf = to_walk_list.pop(0)
        curr_scope = None

        if curr_leaf in self._children:
            curr_scope = self._children[curr_leaf]
        else:
            curr_package = curr_leaf
            if len(path_stack) > 0:
                curr_package = "{}.{}".format(".".join(path_stack), curr_package)

            set_test_scope = False
            if len(to_walk_list) == 0:
                set_test_scope = is_test_scope

            curr_scope = ResourceScope(curr_leaf, curr_package, set_test_scope)
            self._children[curr_leaf] = curr_scope

        if len(to_walk_list) > 0:
            path_stack.append(curr_leaf)
            curr_scope._add_descendent_parameter(parameter_object, to_walk_list, path_stack, is_test_scope)
            path_stack.pop()
        else:
            identifier = parameter_object.identifier
            curr_scope._parameters[identifier] = parameter_object

        return

    def _has_descendent_parameter(self, to_walk_list: List[str], identifier: str):
        rtnval = False

        if len(to_walk_list) == 0:
            if identifier in self._parameters:
                rtnval = True
        else:
            child_name = to_walk_list[0]
            if child_name in self._children:
                scope = self._children[child_name]
                desc_to_walk_list = to_walk_list[1:]
                rtnval = scope._has_descendent_parameter(desc_to_walk_list, identifier)

        return rtnval

    def _has_descendent_parameter(self, to_walk_list: List[str], identifier: str):
        rtnval = False

        if len(to_walk_list) == 0:
            if identifier in self._parameters:
                rtnval = True
        else:
            child_name = to_walk_list[0]
            if child_name in self._children:
                scope = self._children[child_name]
                desc_to_walk_list = to_walk_list[1:]
                rtnval = scope._has_descendent_parameter(desc_to_walk_list, identifier)

        return rtnval

    def _lookup_scope(self, to_walk_list):
        scope_found = None

        child_name = to_walk_list.pop(0)
        if child_name in self._children:
            child_scope = self._children[child_name]
            if len(to_walk_list) > 0:
                scope_found = child_scope._lookup_scope(to_walk_list)
            else:
                scope_found = child_scope

        return scope_found

class ResourceRegistry:
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

            # The integration source tables are how integration sources are registered
            # they help to lookup any factory functions that generate a given type of
            # resource.
            self._integration_source = {}
            self._resource_source = {}
            self._scope_source = {}

            # The subscriptions table is utilized to map the subscriber functions to the
            # factory functions that they subscribe to either via a direct 'param' declaration
            # or via the registration of a well-known name.
            self._subscription_table = {}

            # The wellknown resource table is used to store subscription templates
            # that assign a parameter name to a source function for a given scope.
            # Resources declared as wellknown resources are later linked dynamically to
            # the test methods that are consuming them based on closest scope and if a
            # parameter has already been linked for a given subscriber. 
            self._wellknown_integration_table = {}
            self._wellknown_scope_table = {}
            self._wellknown_resource_table = {}

            # The unknown parameter table gets populated with the names of subscribe functions
            # that have unknown paramters and the list of parameters names the could not be
            # resolved to a parameter source function.
            self._unknown_parameters = {}

            # The identifier subscription table contains a list of identifiers that are used by tests and
            # the associated contexts in which they were used.
            self._identifier_subscription_table = {}

            # The identifier assignment table is used to keep a list of scopes associated with a
            # test run and the variable names that are assigned to a given scope.
            self._scope_tree = ResourceScope()
        return

    @property
    def identifier_subscription_table(self):
        return self._identifier_subscription_table

    @property
    def identifier_scope_table(self):
        return self._scope_identifier_table

    @property
    def unknown_parameters(self):
        return self._unknown_parameters

    def lookup_resource_scope(self, scope_name):
        resource_scope = self._scope_tree.lookup_scope(scope_name)
        return resource_scope

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

        wellknown_table_list = []
        if identifier in self._wellknown_integration_table:
            wellknown_table_list.append(self._wellknown_integration_table)
        else:
            if identifier in self._wellknown_scope_table:
                wellknown_table_list.append(self._wellknown_scope_table)
            if identifier in self._wellknown_resource_table:
                wellknown_table_list.append(self._wellknown_resource_table)

        longest_match_skey = None
        longest_match_candidate_table = None
        for wellknown_table in wellknown_table_list:
            candidate_table = wellknown_table[identifier]

            for skey in candidate_table.keys():
                if query_scope.startswith(skey):
                    if longest_match_skey is not None:
                        if len(skey) > len(longest_match_skey):
                            longest_match_skey = skey
                            longest_match_candidate_table = candidate_table
                    else:
                        longest_match_skey = skey
                        longest_match_candidate_table = candidate_table
                elif skey == "<session>":
                    if longest_match_skey is None:
                       longest_match_skey = skey
                       longest_match_candidate_table = candidate_table

        if longest_match_skey is not None:
            subscription = longest_match_candidate_table[longest_match_skey]

        return subscription

    def lookup_subscriptions(self, subscriber):
        subscriptions = self._subscription_table.get(subscriber, {})
        return subscriptions

    def perform_parameter_resolution(self, test_references: Dict[str, TestRef]):

        self._unknown_parameters = {}
        self._identifier_subscription_table = {}

        integration_table = {}
        scope_table = {}

        # Go through all of the integration sources and perform parameter resolution
        # on any parameters that are feeding the integration sources.
        for source_info in self._integration_source.values():
            missing_params = []
            subscriber_func = source_info.source_function
            self._resolve_subscriber_parameters(subscriber_func, missing_params)

            if subscriber_func in self._subscription_table:
                source_info.subscriptions = self._subscription_table[subscriber_func]

            if len(missing_params) > 0:
                self._unknown_parameters[source_info.source_id] = missing_params

        # Go through all of the scope sources and perform parameter resolution
        # on any parameters that are feeding the scope sources.
        for source_info in self._scope_source.values():
            missing_params = []
            subscriber_func = source_info.source_function
            self._resolve_subscriber_parameters(subscriber_func, missing_params)

            if subscriber_func in self._subscription_table:
                source_info.subscriptions = self._subscription_table[subscriber_func]

            if len(missing_params) > 0:
                self._unknown_parameters[source_info.source_id] = missing_params

        # Go through all of the resource sources and perform parameter resolution
        # on any parameters that are feeding the scope sources.
        for source_info in self._resource_source.values():
            missing_params = []
            subscriber_func = source_info.source_function
            self._resolve_subscriber_parameters(subscriber_func, missing_params)

            if subscriber_func in self._subscription_table:
                source_info.subscriptions = self._subscription_table[subscriber_func]

            if len(missing_params) > 0:
                self._unknown_parameters[source_info.source_id] = missing_params

        # Go through all of the Test References and perform parameter resolution on
        # all the parameters.  Also make sure that the scope tree is filled out all
        # the way up to the test leaf.
        for _, test_ref in test_references.items():
            missing_params= []

            subscriber_func = test_ref.test_function
            self._resolve_subscriber_parameters(subscriber_func, missing_params)

            if subscriber_func in self._subscription_table:
                test_ref.subscriptions = self._subscription_table[subscriber_func]

            if len(missing_params) > 0:
                self._unknown_parameters[test_ref.test_name] = missing_params

            test_scope_name = test_ref.test_name
            if self._scope_tree.lookup_scope(test_scope_name) is None:
                for _, param_obj in test_ref.subscriptions.items():
                    self._scope_tree.add_descendent_parameter(test_scope_name, param_obj)


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

    def register_subscription(self, subscription: ParameterSubscription):

        subscriber = subscription.subscriber_function

        params = None
        if subscriber not in self._subscription_table:
            params = {}
            self._subscription_table[subscriber] = params
        else:
            params = self._subscription_table[subscriber]

        param_name = subscription.identifier
        if param_name in params:
            errmsg = "The parameter {} has already been declared for function {}.".format(
                param_name, subscriber.__name__)
            raise AKitSemanticError(errmsg)

        params[param_name] = subscription

        return

    def register_parameter_origin(self, identifier: str, origin: ParameterOrigin):
        """
            The :method:`register_parameter_origin` is used to register an alias as a wellknown parameter
            so that subscriber functions can consume the parameter as an input parameter.
        """
        candidate_table = None
        wellknown_table = None

        # Perform some rules checking to ensure that test framework consumers are not doing things
        # that could have hidden and unwanted effects.  Things like using the same alias when its
        # not necessary.
        param_type = origin.source_resource_type
        if issubclass(param_type, IntegrationMixIn):
            # If we are registering a integration mixin with a specific identifier name, then it should not
            # be found in the scope or resource tables.  We don't allow integration aliases to be
            # overloaded.
            if identifier in self._wellknown_scope_table:
                errmsg = "The parameter identifier '{}' cannot be used as both a integration identifier and scope identifier."
                raise AKitSemanticError(errmsg)
            if identifier in self._wellknown_resource_table:
                errmsg = "The parameter identifier '{}' cannot be used as both a integration identifier and resource identifier."
                raise AKitSemanticError(errmsg)
            wellknown_table = self._wellknown_integration_table

        elif issubclass(param_type, ScopeMixIn):
            # If we are registering a scope mixin with a specific identifier name, then it should not
            # be found in the integration tables.  We don't allow integration aliases to be overloaded.
            if identifier in self._wellknown_integration_table:
                errmsg = "The parameter identifier '{}' cannot be used as both a integration identifier and scope identifier."
                raise AKitSemanticError(errmsg)
            wellknown_table = self._wellknown_scope_table

        else:
            # If we are registering a resource with a specific identifier name, then it should not
            # be found in the integration tables.  We don't allow integration aliases to be overloaded.
            if identifier in self._wellknown_integration_table:
                errmsg = "The parameter identifier '{}' cannot be used as both a integration identifier and resource identifier."
                raise AKitSemanticError(errmsg)
            wellknown_table = self._wellknown_resource_table

        if identifier not in wellknown_table:
            candidate_table = {}
            wellknown_table[identifier] = candidate_table
        else:
            candidate_table = wellknown_table[identifier]

        assigned_scope = origin.assigned_scope

        if assigned_scope in candidate_table:
            errmsg = "A parameter identified as '{}' has already been assigned to scope '{}'.".format(identifier, assigned_scope)
            raise AKitSemanticError(errmsg)

        if self._scope_tree.has_descendent_parameter(assigned_scope, identifier):
            errmsg = "A wellknown variable identified as '{}' has already been assigned to scope '{}'.".format(identifier, assigned_scope)
            raise AKitSemanticError(errmsg)

        # Add the parameter origin to the identifiers_for_scope table for this scope so we
        # can lookup identifiers by scope
        self._scope_tree.add_descendent_parameter(assigned_scope, origin)

        # Add the parameter origin to the candidate scope table associated with the identifier to
        # help us resolve the correct scope for any given parameter being consumed by a subscriber
        candidate_table[assigned_scope] = origin

        return

    def _collect_integrations_and_scopes_for_subscriber(self, subscriber_func, integration_table, scope_table, usage_ledger):
        """
            Look at the subscriptions for the subscriber function provide in order to find the :class:`IntegrationMixIn`
            and :class:`ScopeMixIn` types that need to be involved in the startup of the test framework and
            test environment.
        """
        params = self._subscription_table[subscriber_func]
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
        if subscriber_function in self._subscription_table:
            params = self._subscription_table[subscriber_function]
        else:
            params = {}
            self._subscription_table[subscriber_function] = params

        subscriber_arg_spec = inspect.getfullargspec(subscriber_function)
        subscriber_args_list = subscriber_arg_spec.args
        if len(subscriber_args_list) > 0:

            for nxt_arg in subscriber_args_list:
                if nxt_arg not in params:
                    # If we don't find a parameter in the subscription
                    # parameters then we need to look in the well-known
                    # parameters and create a subscription for any
                    # well-known parameters.
                    param_origin = self.lookup_wellknown_parameter(nxt_arg, subscriber_module_name)
                    if param_origin is not None:
                        subscription = param_origin.create_subscription(subscriber_function)
                        params[nxt_arg] = subscription
                    else:
                        missing_params.append(nxt_arg)
                else:
                    subobj = params[nxt_arg]
                    if isinstance(subobj, ParameterOrigin):
                        # If all we have is a ParameterOrigin, then we need to try and convert that
                        # to an actual resource in some scope.
                        pass
                    elif subobj.assigned_scope is None:
                        sub_template = self.lookup_wellknown_parameter(nxt_arg, subscriber_module_name)

                if nxt_arg in params:
                    subscription = params[nxt_arg]

                    reference_list = None
                    if nxt_arg not in self._identifier_subscription_table:
                        reference_list = set()
                        self._identifier_subscription_table[nxt_arg] = reference_list
                    else:
                        reference_list = self._identifier_subscription_table[nxt_arg]

                    reference_list.add(subscription)

        return

resource_registry = ResourceRegistry()

