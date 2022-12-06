"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANIPConnection1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANIPConnection1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANIPConnection:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AutoDisconnectTime": { "data_type": "ui4", "default": None, "allowed_list": None},
        "ConnectionStatus": { "data_type": "string", "default": None, "allowed_list": "['Unconfigured', 'Connected', 'Disconnected']"},
        "ConnectionType": { "data_type": "string", "default": None, "allowed_list": None},
        "ExternalIPAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "ExternalPort": { "data_type": "ui2", "default": None, "allowed_list": None},
        "IdleDisconnectTime": { "data_type": "ui4", "default": None, "allowed_list": None},
        "InternalClient": { "data_type": "string", "default": None, "allowed_list": None},
        "InternalPort": { "data_type": "ui2", "default": None, "allowed_list": None},
        "LastConnectionError": { "data_type": "string", "default": None, "allowed_list": "['ERROR_NONE']"},
        "NATEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "PortMappingDescription": { "data_type": "string", "default": None, "allowed_list": None},
        "PortMappingEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "PortMappingLeaseDuration": { "data_type": "ui4", "default": None, "allowed_list": None},
        "PortMappingNumberOfEntries": { "data_type": "ui2", "default": None, "allowed_list": None},
        "PortMappingProtocol": { "data_type": "string", "default": None, "allowed_list": "['TCP', 'UDP']"},
        "PossibleConnectionTypes": { "data_type": "string", "default": None, "allowed_list": "['Unconfigured', 'IP_Routed', 'IP_Bridged']"},
        "RSIPAvailable": { "data_type": "boolean", "default": None, "allowed_list": None},
        "RemoteHost": { "data_type": "string", "default": None, "allowed_list": None},
        "Uptime": { "data_type": "ui4", "default": None, "allowed_list": None},
        "WarnDisconnectDelay": { "data_type": "ui4", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_AddPortMapping(self, NewRemoteHost, NewExternalPort, NewProtocol, NewInternalPort, NewInternalClient, NewEnabled, NewPortMappingDescription, NewLeaseDuration, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddPortMapping action.
        """
        arguments = {
            "NewRemoteHost": NewRemoteHost,
            "NewExternalPort": NewExternalPort,
            "NewProtocol": NewProtocol,
            "NewInternalPort": NewInternalPort,
            "NewInternalClient": NewInternalClient,
            "NewEnabled": NewEnabled,
            "NewPortMappingDescription": NewPortMappingDescription,
            "NewLeaseDuration": NewLeaseDuration,
        }

        self.call_action("AddPortMapping", arguments=arguments, aspects=aspects)

        return

    def action_DeletePortMapping(self, NewRemoteHost, NewExternalPort, NewProtocol, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeletePortMapping action.
        """
        arguments = {
            "NewRemoteHost": NewRemoteHost,
            "NewExternalPort": NewExternalPort,
            "NewProtocol": NewProtocol,
        }

        self.call_action("DeletePortMapping", arguments=arguments, aspects=aspects)

        return

    def action_ForceTermination(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ForceTermination action.
        """
        arguments = { }

        self.call_action("ForceTermination", arguments=arguments, aspects=aspects)

        return

    def action_GetAutoDisconnectTime(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAutoDisconnectTime action.

            :returns: "NewAutoDisconnectTime"
        """
        arguments = { }

        out_params = self.call_action("GetAutoDisconnectTime", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAutoDisconnectTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetConnectionTypeInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetConnectionTypeInfo action.

            :returns: "NewConnectionType", "NewPossibleConnectionTypes"
        """
        arguments = { }

        out_params = self.call_action("GetConnectionTypeInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewConnectionType", "NewPossibleConnectionTypes",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetExternalIPAddress(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetExternalIPAddress action.

            :returns: "NewExternalIPAddress"
        """
        arguments = { }

        out_params = self.call_action("GetExternalIPAddress", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewExternalIPAddress",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetGenericPortMappingEntry(self, NewPortMappingIndex, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetGenericPortMappingEntry action.

            :returns: "NewRemoteHost", "NewExternalPort", "NewProtocol", "NewInternalPort", "NewInternalClient", "NewEnabled", "NewPortMappingDescription", "NewLeaseDuration"
        """
        arguments = {
            "NewPortMappingIndex": NewPortMappingIndex,
        }

        out_params = self.call_action("GetGenericPortMappingEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewRemoteHost", "NewExternalPort", "NewProtocol", "NewInternalPort", "NewInternalClient", "NewEnabled", "NewPortMappingDescription", "NewLeaseDuration",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetIdleDisconnectTime(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetIdleDisconnectTime action.

            :returns: "NewIdleDisconnectTime"
        """
        arguments = { }

        out_params = self.call_action("GetIdleDisconnectTime", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewIdleDisconnectTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetNATRSIPStatus(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetNATRSIPStatus action.

            :returns: "NewRSIPAvailable", "NewNATEnabled"
        """
        arguments = { }

        out_params = self.call_action("GetNATRSIPStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewRSIPAvailable", "NewNATEnabled",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSpecificPortMappingEntry(self, NewRemoteHost, NewExternalPort, NewProtocol, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSpecificPortMappingEntry action.

            :returns: "NewInternalPort", "NewInternalClient", "NewEnabled", "NewPortMappingDescription", "NewLeaseDuration"
        """
        arguments = {
            "NewRemoteHost": NewRemoteHost,
            "NewExternalPort": NewExternalPort,
            "NewProtocol": NewProtocol,
        }

        out_params = self.call_action("GetSpecificPortMappingEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewInternalPort", "NewInternalClient", "NewEnabled", "NewPortMappingDescription", "NewLeaseDuration",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetStatusInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetStatusInfo action.

            :returns: "NewConnectionStatus", "NewLastConnectionError", "NewUptime"
        """
        arguments = { }

        out_params = self.call_action("GetStatusInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewConnectionStatus", "NewLastConnectionError", "NewUptime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetWarnDisconnectDelay(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetWarnDisconnectDelay action.

            :returns: "NewWarnDisconnectDelay"
        """
        arguments = { }

        out_params = self.call_action("GetWarnDisconnectDelay", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewWarnDisconnectDelay",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RequestConnection(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RequestConnection action.
        """
        arguments = { }

        self.call_action("RequestConnection", arguments=arguments, aspects=aspects)

        return

    def action_RequestTermination(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RequestTermination action.
        """
        arguments = { }

        self.call_action("RequestTermination", arguments=arguments, aspects=aspects)

        return

    def action_SetAutoDisconnectTime(self, NewAutoDisconnectTime, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAutoDisconnectTime action.
        """
        arguments = {
            "NewAutoDisconnectTime": NewAutoDisconnectTime,
        }

        self.call_action("SetAutoDisconnectTime", arguments=arguments, aspects=aspects)

        return

    def action_SetConnectionType(self, NewConnectionType, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetConnectionType action.
        """
        arguments = {
            "NewConnectionType": NewConnectionType,
        }

        self.call_action("SetConnectionType", arguments=arguments, aspects=aspects)

        return

    def action_SetIdleDisconnectTime(self, NewIdleDisconnectTime, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetIdleDisconnectTime action.
        """
        arguments = {
            "NewIdleDisconnectTime": NewIdleDisconnectTime,
        }

        self.call_action("SetIdleDisconnectTime", arguments=arguments, aspects=aspects)

        return

    def action_SetWarnDisconnectDelay(self, NewWarnDisconnectDelay, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetWarnDisconnectDelay action.
        """
        arguments = {
            "NewWarnDisconnectDelay": NewWarnDisconnectDelay,
        }

        self.call_action("SetWarnDisconnectDelay", arguments=arguments, aspects=aspects)

        return
