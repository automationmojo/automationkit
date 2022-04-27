"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ConfigurationManagement1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ConfigurationManagement1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ConfigurationManagement:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AttributeValuesUpdate": { "data_type": "string", "default": None, "allowed_list": None},
        "ConfigurationUpdate": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentConfigurationVersion": { "data_type": "ui4", "default": None, "allowed_list": None},
        "InconsistentStatus": { "data_type": "boolean", "default": None, "allowed_list": None},
        "SupportedDataModelsUpdate": { "data_type": "string", "default": None, "allowed_list": None},
        "SupportedParametersUpdate": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_CreateInstance(self, MultiInstanceName, ChildrenInitialization, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateInstance action.

            :returns: "InstanceIdentifier", "Status"
        """
        arguments = {
            "MultiInstanceName": MultiInstanceName,
            "ChildrenInitialization": ChildrenInitialization,
        }

        out_params = self.call_action("CreateInstance", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("InstanceIdentifier", "Status",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteInstance(self, InstanceIdentifier, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteInstance action.

            :returns: "Status"
        """
        arguments = {
            "InstanceIdentifier": InstanceIdentifier,
        }

        out_params = self.call_action("DeleteInstance", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Status",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAttributeValuesUpdate(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAttributeValuesUpdate action.

            :returns: "StateVariableValue"
        """
        arguments = { }

        out_params = self.call_action("GetAttributeValuesUpdate", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAttributes(self, Parameters, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAttributes action.

            :returns: "NodeAttributeValueList"
        """
        arguments = {
            "Parameters": Parameters,
        }

        out_params = self.call_action("GetAttributes", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NodeAttributeValueList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetConfigurationUpdate(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetConfigurationUpdate action.

            :returns: "StateVariableValue"
        """
        arguments = { }

        out_params = self.call_action("GetConfigurationUpdate", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCurrentConfigurationVersion(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCurrentConfigurationVersion action.

            :returns: "StateVariableValue"
        """
        arguments = { }

        out_params = self.call_action("GetCurrentConfigurationVersion", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetInconsistentStatus(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetInconsistentStatus action.

            :returns: "StateVariableValue"
        """
        arguments = { }

        out_params = self.call_action("GetInconsistentStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetInstances(self, StartingNode, SearchDepth, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetInstances action.

            :returns: "Result"
        """
        arguments = {
            "StartingNode": StartingNode,
            "SearchDepth": SearchDepth,
        }

        out_params = self.call_action("GetInstances", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSelectedValues(self, StartingNode, Filter, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSelectedValues action.

            :returns: "ParameterValueList"
        """
        arguments = {
            "StartingNode": StartingNode,
            "Filter": Filter,
        }

        out_params = self.call_action("GetSelectedValues", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ParameterValueList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSupportedDataModels(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSupportedDataModels action.

            :returns: "SupportedDataModels"
        """
        arguments = { }

        out_params = self.call_action("GetSupportedDataModels", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedDataModels",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSupportedDataModelsUpdate(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSupportedDataModelsUpdate action.

            :returns: "StateVariableValue"
        """
        arguments = { }

        out_params = self.call_action("GetSupportedDataModelsUpdate", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSupportedParameters(self, StartingNode, SearchDepth, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSupportedParameters action.

            :returns: "Result"
        """
        arguments = {
            "StartingNode": StartingNode,
            "SearchDepth": SearchDepth,
        }

        out_params = self.call_action("GetSupportedParameters", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSupportedParametersUpdate(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSupportedParametersUpdate action.

            :returns: "StateVariableValue"
        """
        arguments = { }

        out_params = self.call_action("GetSupportedParametersUpdate", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetValues(self, Parameters, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetValues action.

            :returns: "ParameterValueList"
        """
        arguments = {
            "Parameters": Parameters,
        }

        out_params = self.call_action("GetValues", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ParameterValueList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetAttributes(self, NodeAttributeValueList, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAttributes action.

            :returns: "Status"
        """
        arguments = {
            "NodeAttributeValueList": NodeAttributeValueList,
        }

        out_params = self.call_action("SetAttributes", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Status",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetValues(self, ParameterValueList, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetValues action.

            :returns: "Status"
        """
        arguments = {
            "ParameterValueList": ParameterValueList,
        }

        out_params = self.call_action("SetValues", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Status",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
