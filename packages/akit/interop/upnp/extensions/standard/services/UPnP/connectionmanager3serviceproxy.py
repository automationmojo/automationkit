"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ConnectionManager3ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ConnectionManager3' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ConnectionManager:3'

    SERVICE_DEFAULT_VARIABLES = {
        "ClockUpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "FeatureList": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "CurrentConnectionIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "DeviceClockInfoUpdates": { "data_type": "string", "default": None, "allowed_list": None},
        "SinkProtocolInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "SourceProtocolInfo": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_ConnectionComplete(self, ConnectionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ConnectionComplete action.
        """
        arguments = {
            "ConnectionID": ConnectionID,
        }

        self.call_action("ConnectionComplete", arguments=arguments, aspects=aspects)

        return

    def action_GetCurrentConnectionIDs(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCurrentConnectionIDs action.

            :returns: "ConnectionIDs"
        """
        arguments = { }

        out_params = self.call_action("GetCurrentConnectionIDs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectionIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCurrentConnectionInfo(self, ConnectionID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCurrentConnectionInfo action.

            :returns: "RcsID", "AVTransportID", "ProtocolInfo", "PeerConnectionManager", "PeerConnectionID", "Direction", "Status"
        """
        arguments = {
            "ConnectionID": ConnectionID,
        }

        out_params = self.call_action("GetCurrentConnectionInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RcsID", "AVTransportID", "ProtocolInfo", "PeerConnectionManager", "PeerConnectionID", "Direction", "Status",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFeatureList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFeatureList action.

            :returns: "FeatureList"
        """
        arguments = { }

        out_params = self.call_action("GetFeatureList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FeatureList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetProtocolInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetProtocolInfo action.

            :returns: "Source", "Sink"
        """
        arguments = { }

        out_params = self.call_action("GetProtocolInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Source", "Sink",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRendererItemInfo(self, ItemInfoFilter, ItemMetadataList, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRendererItemInfo action.

            :returns: "ItemRenderingInfoList"
        """
        arguments = {
            "ItemInfoFilter": ItemInfoFilter,
            "ItemMetadataList": ItemMetadataList,
        }

        out_params = self.call_action("GetRendererItemInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ItemRenderingInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_PrepareForConnection(self, RemoteProtocolInfo, PeerConnectionManager, PeerConnectionID, Direction, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the PrepareForConnection action.

            :returns: "ConnectionID", "AVTransportID", "RcsID"
        """
        arguments = {
            "RemoteProtocolInfo": RemoteProtocolInfo,
            "PeerConnectionManager": PeerConnectionManager,
            "PeerConnectionID": PeerConnectionID,
            "Direction": Direction,
        }

        out_params = self.call_action("PrepareForConnection", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectionID", "AVTransportID", "RcsID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
