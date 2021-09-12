"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANCommonInterfaceConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANCommonInterfaceConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_GetActiveConnection(self, NewActiveConnectionIndex, extract_returns=True):
        """
            Calls the GetActiveConnection action.

            :returns: "NewActiveConnDeviceContainer", "NewActiveConnectionServiceID"
        """
        arguments = {
            "NewActiveConnectionIndex": NewActiveConnectionIndex,
        }

        out_params = self._proxy_call_action("GetActiveConnection", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewActiveConnDeviceContainer", "NewActiveConnectionServiceID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCommonLinkProperties(self, extract_returns=True):
        """
            Calls the GetCommonLinkProperties action.

            :returns: "NewWANAccessType", "NewLayer1UpstreamMaxBitRate", "NewLayer1DownstreamMaxBitRate", "NewPhysicalLinkStatus"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetCommonLinkProperties", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewWANAccessType", "NewLayer1UpstreamMaxBitRate", "NewLayer1DownstreamMaxBitRate", "NewPhysicalLinkStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetEnabledForInternet(self, extract_returns=True):
        """
            Calls the GetEnabledForInternet action.

            :returns: "NewEnabledForInternet"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetEnabledForInternet", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewEnabledForInternet",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMaximumActiveConnections(self, extract_returns=True):
        """
            Calls the GetMaximumActiveConnections action.

            :returns: "NewMaximumActiveConnections"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetMaximumActiveConnections", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewMaximumActiveConnections",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalBytesReceived(self, extract_returns=True):
        """
            Calls the GetTotalBytesReceived action.

            :returns: "NewTotalBytesReceived"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetTotalBytesReceived", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalBytesReceived",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalBytesSent(self, extract_returns=True):
        """
            Calls the GetTotalBytesSent action.

            :returns: "NewTotalBytesSent"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetTotalBytesSent", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalBytesSent",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalPacketsReceived(self, extract_returns=True):
        """
            Calls the GetTotalPacketsReceived action.

            :returns: "NewTotalPacketsReceived"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetTotalPacketsReceived", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalPacketsReceived",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalPacketsSent(self, extract_returns=True):
        """
            Calls the GetTotalPacketsSent action.

            :returns: "NewTotalPacketsSent"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetTotalPacketsSent", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalPacketsSent",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetWANAccessProvider(self, extract_returns=True):
        """
            Calls the GetWANAccessProvider action.

            :returns: "NewWANAccessProvider"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetWANAccessProvider", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewWANAccessProvider",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetEnabledForInternet(self, NewEnabledForInternet):
        """
            Calls the SetEnabledForInternet action.
        """
        arguments = {
            "NewEnabledForInternet": NewEnabledForInternet,
        }

        self._proxy_call_action("SetEnabledForInternet", arguments=arguments)

        return
