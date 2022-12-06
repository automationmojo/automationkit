"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RADASync2ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RADASync2' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RADASync:2'

    SERVICE_DEFAULT_VARIABLES = {
        "SystemInfo": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_AddRemoteDevices(self, DeviceList, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddRemoteDevices action.
        """
        arguments = {
            "DeviceList": DeviceList,
            "ID": ID,
        }

        self.call_action("AddRemoteDevices", arguments=arguments, aspects=aspects)

        return

    def action_GetLocalNetworkAddressInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLocalNetworkAddressInfo action.

            :returns: "LocalNetworkAddress"
        """
        arguments = { }

        out_params = self.call_action("GetLocalNetworkAddressInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("LocalNetworkAddress",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_HeartbeatUpdate(self, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the HeartbeatUpdate action.
        """
        arguments = {
            "ID": ID,
        }

        self.call_action("HeartbeatUpdate", arguments=arguments, aspects=aspects)

        return

    def action_RemoveRemoteDevices(self, DeviceList, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveRemoteDevices action.
        """
        arguments = {
            "DeviceList": DeviceList,
            "ID": ID,
        }

        self.call_action("RemoveRemoteDevices", arguments=arguments, aspects=aspects)

        return

    def action_SetDDDLocation(self, DDDLocation, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDDDLocation action.
        """
        arguments = {
            "DDDLocation": DDDLocation,
            "ID": ID,
        }

        self.call_action("SetDDDLocation", arguments=arguments, aspects=aspects)

        return
