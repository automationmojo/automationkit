"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANPPPConnection1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANPPPConnection1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANPPPConnection:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_AddPortMapping(self, NewRemoteHost, NewExternalPort, NewProtocol, NewInternalPort, NewInternalClient, NewEnabled, NewPortMappingDescription, NewLeaseDuration):
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

        self._proxy_call_action("AddPortMapping", arguments=arguments)

        return

    def action_ConfigureConnection(self, NewUserName, NewPassword):
        """
            Calls the ConfigureConnection action.
        """
        arguments = {
            "NewUserName": NewUserName,
            "NewPassword": NewPassword,
        }

        self._proxy_call_action("ConfigureConnection", arguments=arguments)

        return

    def action_DeletePortMapping(self, NewRemoteHost, NewExternalPort, NewProtocol):
        """
            Calls the DeletePortMapping action.
        """
        arguments = {
            "NewRemoteHost": NewRemoteHost,
            "NewExternalPort": NewExternalPort,
            "NewProtocol": NewProtocol,
        }

        self._proxy_call_action("DeletePortMapping", arguments=arguments)

        return

    def action_ForceTermination(self):
        """
            Calls the ForceTermination action.
        """
        arguments = { }


        self._proxy_call_action("ForceTermination", arguments=arguments)

        return

    def action_GetAutoDisconnectTime(self, extract_returns=True):
        """
            Calls the GetAutoDisconnectTime action.

            :returns: "NewAutoDisconnectTime"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetAutoDisconnectTime", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAutoDisconnectTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetConnectionTypeInfo(self, extract_returns=True):
        """
            Calls the GetConnectionTypeInfo action.

            :returns: "NewConnectionType", "NewPossibleConnectionTypes"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetConnectionTypeInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewConnectionType", "NewPossibleConnectionTypes",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetExternalIPAddress(self, extract_returns=True):
        """
            Calls the GetExternalIPAddress action.

            :returns: "NewExternalIPAddress"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetExternalIPAddress", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewExternalIPAddress",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetGenericPortMappingEntry(self, NewPortMappingIndex, extract_returns=True):
        """
            Calls the GetGenericPortMappingEntry action.

            :returns: "NewRemoteHost", "NewExternalPort", "NewProtocol", "NewInternalPort", "NewInternalClient", "NewEnabled", "NewPortMappingDescription", "NewLeaseDuration"
        """
        arguments = {
            "NewPortMappingIndex": NewPortMappingIndex,
        }

        out_params = self._proxy_call_action("GetGenericPortMappingEntry", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewRemoteHost", "NewExternalPort", "NewProtocol", "NewInternalPort", "NewInternalClient", "NewEnabled", "NewPortMappingDescription", "NewLeaseDuration",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetIdleDisconnectTime(self, extract_returns=True):
        """
            Calls the GetIdleDisconnectTime action.

            :returns: "NewIdleDisconnectTime"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetIdleDisconnectTime", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewIdleDisconnectTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLinkLayerMaxBitRates(self, extract_returns=True):
        """
            Calls the GetLinkLayerMaxBitRates action.

            :returns: "NewUpstreamMaxBitRate", "NewDownstreamMaxBitRate"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetLinkLayerMaxBitRates", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamMaxBitRate", "NewDownstreamMaxBitRate",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetNATRSIPStatus(self, extract_returns=True):
        """
            Calls the GetNATRSIPStatus action.

            :returns: "NewRSIPAvailable", "NewNATEnabled"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetNATRSIPStatus", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewRSIPAvailable", "NewNATEnabled",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPPPAuthenticationProtocol(self, extract_returns=True):
        """
            Calls the GetPPPAuthenticationProtocol action.

            :returns: "NewPPPAuthenticationProtocol"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetPPPAuthenticationProtocol", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPPPAuthenticationProtocol",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPPPCompressionProtocol(self, extract_returns=True):
        """
            Calls the GetPPPCompressionProtocol action.

            :returns: "NewPPPCompressionProtocol"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetPPPCompressionProtocol", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPPPCompressionProtocol",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPPPEncryptionProtocol(self, extract_returns=True):
        """
            Calls the GetPPPEncryptionProtocol action.

            :returns: "NewPPPEncryptionProtocol"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetPPPEncryptionProtocol", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPPPEncryptionProtocol",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPassword(self, extract_returns=True):
        """
            Calls the GetPassword action.

            :returns: "NewPassword"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetPassword", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPassword",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSpecificPortMappingEntry(self, NewRemoteHost, NewExternalPort, NewProtocol, extract_returns=True):
        """
            Calls the GetSpecificPortMappingEntry action.

            :returns: "NewInternalPort", "NewInternalClient", "NewEnabled", "NewPortMappingDescription", "NewLeaseDuration"
        """
        arguments = {
            "NewRemoteHost": NewRemoteHost,
            "NewExternalPort": NewExternalPort,
            "NewProtocol": NewProtocol,
        }

        out_params = self._proxy_call_action("GetSpecificPortMappingEntry", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewInternalPort", "NewInternalClient", "NewEnabled", "NewPortMappingDescription", "NewLeaseDuration",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetStatusInfo(self, extract_returns=True):
        """
            Calls the GetStatusInfo action.

            :returns: "NewConnectionStatus", "NewLastConnectionError", "NewUptime"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetStatusInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewConnectionStatus", "NewLastConnectionError", "NewUptime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUserName(self, extract_returns=True):
        """
            Calls the GetUserName action.

            :returns: "NewUserName"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetUserName", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUserName",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetWarnDisconnectDelay(self, extract_returns=True):
        """
            Calls the GetWarnDisconnectDelay action.

            :returns: "NewWarnDisconnectDelay"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetWarnDisconnectDelay", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewWarnDisconnectDelay",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RequestConnection(self):
        """
            Calls the RequestConnection action.
        """
        arguments = { }


        self._proxy_call_action("RequestConnection", arguments=arguments)

        return

    def action_RequestTermination(self):
        """
            Calls the RequestTermination action.
        """
        arguments = { }


        self._proxy_call_action("RequestTermination", arguments=arguments)

        return

    def action_SetAutoDisconnectTime(self, NewAutoDisconnectTime):
        """
            Calls the SetAutoDisconnectTime action.
        """
        arguments = {
            "NewAutoDisconnectTime": NewAutoDisconnectTime,
        }

        self._proxy_call_action("SetAutoDisconnectTime", arguments=arguments)

        return

    def action_SetConnectionType(self, NewConnectionType):
        """
            Calls the SetConnectionType action.
        """
        arguments = {
            "NewConnectionType": NewConnectionType,
        }

        self._proxy_call_action("SetConnectionType", arguments=arguments)

        return

    def action_SetIdleDisconnectTime(self, NewIdleDisconnectTime):
        """
            Calls the SetIdleDisconnectTime action.
        """
        arguments = {
            "NewIdleDisconnectTime": NewIdleDisconnectTime,
        }

        self._proxy_call_action("SetIdleDisconnectTime", arguments=arguments)

        return

    def action_SetWarnDisconnectDelay(self, NewWarnDisconnectDelay):
        """
            Calls the SetWarnDisconnectDelay action.
        """
        arguments = {
            "NewWarnDisconnectDelay": NewWarnDisconnectDelay,
        }

        self._proxy_call_action("SetWarnDisconnectDelay", arguments=arguments)

        return
