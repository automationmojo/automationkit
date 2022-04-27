"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RemoteUIClient1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RemoteUIClient1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RemoteUIClient:1'

    SERVICE_DEFAULT_VARIABLES = {
        "CompatibleUIsUpdateIDEvent": { "data_type": "i4", "default": None, "allowed_list": None},
        "CurrentConnections": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentConnectionsEvent": { "data_type": "string", "default": None, "allowed_list": None},
        "DeviceProfile": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_AddUIListing(self, InputUIList, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddUIListing action.

            :returns: "TimeToLive"
        """
        arguments = {
            "InputUIList": InputUIList,
        }

        out_params = self.call_action("AddUIListing", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TimeToLive",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Connect(self, RequestedConnections, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Connect action.

            :returns: "CurrentConnectionsList"
        """
        arguments = {
            "RequestedConnections": RequestedConnections,
        }

        out_params = self.call_action("Connect", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentConnectionsList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Disconnect(self, RequestedDisconnects, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Disconnect action.

            :returns: "CurrentConnectionsList"
        """
        arguments = {
            "RequestedDisconnects": RequestedDisconnects,
        }

        out_params = self.call_action("Disconnect", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentConnectionsList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DisplayMessage(self, MessageType, Message, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DisplayMessage action.
        """
        arguments = {
            "MessageType": MessageType,
            "Message": Message,
        }

        self.call_action("DisplayMessage", arguments=arguments, aspects=aspects)

        return

    def action_GetCurrentConnections(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCurrentConnections action.

            :returns: "CurrentConnectionsList"
        """
        arguments = { }

        out_params = self.call_action("GetCurrentConnections", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentConnectionsList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDeviceProfile(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDeviceProfile action.

            :returns: "StaticDeviceInfo"
        """
        arguments = { }

        out_params = self.call_action("GetDeviceProfile", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StaticDeviceInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUIListing(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUIListing action.

            :returns: "CompatibleUIList"
        """
        arguments = { }

        out_params = self.call_action("GetUIListing", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CompatibleUIList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ProcessInput(self, InputDataType, InputData, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ProcessInput action.
        """
        arguments = {
            "InputDataType": InputDataType,
            "InputData": InputData,
        }

        self.call_action("ProcessInput", arguments=arguments, aspects=aspects)

        return

    def action_RemoveUIListing(self, RemoveUIList, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveUIListing action.
        """
        arguments = {
            "RemoveUIList": RemoveUIList,
        }

        self.call_action("RemoveUIListing", arguments=arguments, aspects=aspects)

        return
