"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ConnectionManager3ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ConnectionManager3' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ConnectionManager:3'

    SERVICE_EVENT_VARIABLES = {
        "CurrentConnectionIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "DeviceClockInfoUpdates": { "data_type": "string", "default": None, "allowed_list": None},
        "SinkProtocolInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "SourceProtocolInfo": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_ConnectionComplete(self, ConnectionID):
        """
            Calls the ConnectionComplete action.
        """
        arguments = {
            "ConnectionID": ConnectionID,
        }

        self._proxy_call_action("ConnectionComplete", arguments=arguments)

        return

    def action_GetCurrentConnectionIDs(self, extract_returns=True):
        """
            Calls the GetCurrentConnectionIDs action.

            :returns: "ConnectionIDs"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetCurrentConnectionIDs", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectionIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCurrentConnectionInfo(self, ConnectionID, extract_returns=True):
        """
            Calls the GetCurrentConnectionInfo action.

            :returns: "RcsID", "AVTransportID", "ProtocolInfo", "PeerConnectionManager", "PeerConnectionID", "Direction", "Status"
        """
        arguments = {
            "ConnectionID": ConnectionID,
        }

        out_params = self._proxy_call_action("GetCurrentConnectionInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RcsID", "AVTransportID", "ProtocolInfo", "PeerConnectionManager", "PeerConnectionID", "Direction", "Status",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFeatureList(self, extract_returns=True):
        """
            Calls the GetFeatureList action.

            :returns: "FeatureList"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetFeatureList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FeatureList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetProtocolInfo(self, extract_returns=True):
        """
            Calls the GetProtocolInfo action.

            :returns: "Source", "Sink"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetProtocolInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Source", "Sink",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRendererItemInfo(self, ItemInfoFilter, ItemMetadataList, extract_returns=True):
        """
            Calls the GetRendererItemInfo action.

            :returns: "ItemRenderingInfoList"
        """
        arguments = {
            "ItemInfoFilter": ItemInfoFilter,
            "ItemMetadataList": ItemMetadataList,
        }

        out_params = self._proxy_call_action("GetRendererItemInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ItemRenderingInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_PrepareForConnection(self, RemoteProtocolInfo, PeerConnectionManager, PeerConnectionID, Direction, extract_returns=True):
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

        out_params = self._proxy_call_action("PrepareForConnection", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectionID", "AVTransportID", "RcsID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
