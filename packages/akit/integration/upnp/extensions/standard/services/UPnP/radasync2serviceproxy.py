"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RADASync2ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RADASync2' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RADASync:2'

    SERVICE_EVENT_VARIABLES = {}

    def action_AddRemoteDevices(self, DeviceList, ID):
        """
            Calls the AddRemoteDevices action.
        """
        arguments = {
            "DeviceList": DeviceList,
            "ID": ID,
        }

        self._proxy_call_action("AddRemoteDevices", arguments=arguments)

        return

    def action_GetLocalNetworkAddressInfo(self, extract_returns=True):
        """
            Calls the GetLocalNetworkAddressInfo action.

            :returns: "LocalNetworkAddress"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetLocalNetworkAddressInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("LocalNetworkAddress",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_HeartbeatUpdate(self, ID):
        """
            Calls the HeartbeatUpdate action.
        """
        arguments = {
            "ID": ID,
        }

        self._proxy_call_action("HeartbeatUpdate", arguments=arguments)

        return

    def action_RemoveRemoteDevices(self, DeviceList, ID):
        """
            Calls the RemoveRemoteDevices action.
        """
        arguments = {
            "DeviceList": DeviceList,
            "ID": ID,
        }

        self._proxy_call_action("RemoveRemoteDevices", arguments=arguments)

        return

    def action_SetDDDLocation(self, DDDLocation, ID):
        """
            Calls the SetDDDLocation action.
        """
        arguments = {
            "DDDLocation": DDDLocation,
            "ID": ID,
        }

        self._proxy_call_action("SetDDDLocation", arguments=arguments)

        return
