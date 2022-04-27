"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANCommonInterfaceConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANCommonInterfaceConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1'

    SERVICE_DEFAULT_VARIABLES = {
        "ActiveConnectionDeviceContainer": { "data_type": "string", "default": None, "allowed_list": None},
        "ActiveConnectionServiceID": { "data_type": "string", "default": None, "allowed_list": None},
        "EnabledForInternet": { "data_type": "boolean", "default": None, "allowed_list": None},
        "Layer1DownstreamMaxBitRate": { "data_type": "ui4", "default": None, "allowed_list": None},
        "Layer1UpstreamMaxBitRate": { "data_type": "ui4", "default": None, "allowed_list": None},
        "MaximumActiveConnections": { "data_type": "ui2", "default": None, "allowed_list": None},
        "NumberOfActiveConnections": { "data_type": "ui2", "default": None, "allowed_list": None},
        "PhysicalLinkStatus": { "data_type": "string", "default": None, "allowed_list": "['Up', 'Down']"},
        "TotalBytesReceived": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TotalBytesSent": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TotalPacketsReceived": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TotalPacketsSent": { "data_type": "ui4", "default": None, "allowed_list": None},
        "WANAccessProvider": { "data_type": "string", "default": None, "allowed_list": None},
        "WANAccessType": { "data_type": "string", "default": None, "allowed_list": "['DSL', 'POTS', 'Cable', 'Ethernet']"},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetActiveConnection(self, NewActiveConnectionIndex, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetActiveConnection action.

            :returns: "NewActiveConnDeviceContainer", "NewActiveConnectionServiceID"
        """
        arguments = {
            "NewActiveConnectionIndex": NewActiveConnectionIndex,
        }

        out_params = self.call_action("GetActiveConnection", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewActiveConnDeviceContainer", "NewActiveConnectionServiceID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCommonLinkProperties(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCommonLinkProperties action.

            :returns: "NewWANAccessType", "NewLayer1UpstreamMaxBitRate", "NewLayer1DownstreamMaxBitRate", "NewPhysicalLinkStatus"
        """
        arguments = { }

        out_params = self.call_action("GetCommonLinkProperties", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewWANAccessType", "NewLayer1UpstreamMaxBitRate", "NewLayer1DownstreamMaxBitRate", "NewPhysicalLinkStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetEnabledForInternet(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetEnabledForInternet action.

            :returns: "NewEnabledForInternet"
        """
        arguments = { }

        out_params = self.call_action("GetEnabledForInternet", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewEnabledForInternet",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMaximumActiveConnections(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMaximumActiveConnections action.

            :returns: "NewMaximumActiveConnections"
        """
        arguments = { }

        out_params = self.call_action("GetMaximumActiveConnections", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewMaximumActiveConnections",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalBytesReceived(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTotalBytesReceived action.

            :returns: "NewTotalBytesReceived"
        """
        arguments = { }

        out_params = self.call_action("GetTotalBytesReceived", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalBytesReceived",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalBytesSent(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTotalBytesSent action.

            :returns: "NewTotalBytesSent"
        """
        arguments = { }

        out_params = self.call_action("GetTotalBytesSent", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalBytesSent",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalPacketsReceived(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTotalPacketsReceived action.

            :returns: "NewTotalPacketsReceived"
        """
        arguments = { }

        out_params = self.call_action("GetTotalPacketsReceived", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalPacketsReceived",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalPacketsSent(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTotalPacketsSent action.

            :returns: "NewTotalPacketsSent"
        """
        arguments = { }

        out_params = self.call_action("GetTotalPacketsSent", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalPacketsSent",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetWANAccessProvider(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetWANAccessProvider action.

            :returns: "NewWANAccessProvider"
        """
        arguments = { }

        out_params = self.call_action("GetWANAccessProvider", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewWANAccessProvider",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetEnabledForInternet(self, NewEnabledForInternet, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetEnabledForInternet action.
        """
        arguments = {
            "NewEnabledForInternet": NewEnabledForInternet,
        }

        self.call_action("SetEnabledForInternet", arguments=arguments, aspects=aspects)

        return
