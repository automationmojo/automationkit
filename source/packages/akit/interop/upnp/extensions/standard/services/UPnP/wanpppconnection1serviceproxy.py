"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANPPPConnection1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANPPPConnection1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANPPPConnection:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AutoDisconnectTime": { "data_type": "ui4", "default": None, "allowed_list": None},
        "ConnectionStatus": { "data_type": "string", "default": None, "allowed_list": "['Unconfigured', 'Connected', 'Disconnected']"},
        "ConnectionType": { "data_type": "string", "default": None, "allowed_list": None},
        "DownstreamMaxBitRate": { "data_type": "ui4", "default": None, "allowed_list": None},
        "ExternalIPAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "ExternalPort": { "data_type": "ui2", "default": None, "allowed_list": None},
        "IdleDisconnectTime": { "data_type": "ui4", "default": None, "allowed_list": None},
        "InternalClient": { "data_type": "string", "default": None, "allowed_list": None},
        "InternalPort": { "data_type": "ui2", "default": None, "allowed_list": None},
        "LastConnectionError": { "data_type": "string", "default": None, "allowed_list": "['ERROR_NONE']"},
        "NATEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "PPPAuthenticationProtocol": { "data_type": "string", "default": None, "allowed_list": None},
        "PPPCompressionProtocol": { "data_type": "string", "default": None, "allowed_list": None},
        "PPPEncryptionProtocol": { "data_type": "string", "default": None, "allowed_list": None},
        "Password": { "data_type": "string", "default": None, "allowed_list": None},
        "PortMappingDescription": { "data_type": "string", "default": None, "allowed_list": None},
        "PortMappingEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "PortMappingLeaseDuration": { "data_type": "ui4", "default": None, "allowed_list": None},
        "PortMappingNumberOfEntries": { "data_type": "ui2", "default": None, "allowed_list": None},
        "PortMappingProtocol": { "data_type": "string", "default": None, "allowed_list": "['TCP', 'UDP']"},
        "PossibleConnectionTypes": { "data_type": "string", "default": None, "allowed_list": "['Unconfigured', 'IP_Routed', 'DHCP_Spoofed', 'PPPoE_Bridged', 'PPTP_Relay', 'L2TP_Relay', 'PPPoE_Relay']"},
        "RSIPAvailable": { "data_type": "boolean", "default": None, "allowed_list": None},
        "RemoteHost": { "data_type": "string", "default": None, "allowed_list": None},
        "UpstreamMaxBitRate": { "data_type": "ui4", "default": None, "allowed_list": None},
        "Uptime": { "data_type": "ui4", "default": None, "allowed_list": None},
        "UserName": { "data_type": "string", "default": None, "allowed_list": None},
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

    def action_ConfigureConnection(self, NewUserName, NewPassword, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ConfigureConnection action.
        """
        arguments = {
            "NewUserName": NewUserName,
            "NewPassword": NewPassword,
        }

        self.call_action("ConfigureConnection", arguments=arguments, aspects=aspects)

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

    def action_GetLinkLayerMaxBitRates(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLinkLayerMaxBitRates action.

            :returns: "NewUpstreamMaxBitRate", "NewDownstreamMaxBitRate"
        """
        arguments = { }

        out_params = self.call_action("GetLinkLayerMaxBitRates", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamMaxBitRate", "NewDownstreamMaxBitRate",)]
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

    def action_GetPPPAuthenticationProtocol(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPPPAuthenticationProtocol action.

            :returns: "NewPPPAuthenticationProtocol"
        """
        arguments = { }

        out_params = self.call_action("GetPPPAuthenticationProtocol", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPPPAuthenticationProtocol",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPPPCompressionProtocol(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPPPCompressionProtocol action.

            :returns: "NewPPPCompressionProtocol"
        """
        arguments = { }

        out_params = self.call_action("GetPPPCompressionProtocol", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPPPCompressionProtocol",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPPPEncryptionProtocol(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPPPEncryptionProtocol action.

            :returns: "NewPPPEncryptionProtocol"
        """
        arguments = { }

        out_params = self.call_action("GetPPPEncryptionProtocol", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPPPEncryptionProtocol",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPassword(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPassword action.

            :returns: "NewPassword"
        """
        arguments = { }

        out_params = self.call_action("GetPassword", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPassword",)]
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

    def action_GetUserName(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUserName action.

            :returns: "NewUserName"
        """
        arguments = { }

        out_params = self.call_action("GetUserName", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUserName",)]
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
