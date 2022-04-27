"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class CloudProxy1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'CloudProxy1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:CloudProxy:1'

    SERVICE_DEFAULT_VARIABLES = {
        "DeviceList": { "data_type": "string", "default": None, "allowed_list": None},
        "ProxyList": { "data_type": "string", "default": None, "allowed_list": None},
        "UCSList": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "CloudProxyUpdate": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddProxyDevice(self, DeviceId, UserAtCloud, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddProxyDevice action.

            :returns: "DeviceJID"
        """
        arguments = {
            "DeviceId": DeviceId,
            "UserAtCloud": UserAtCloud,
        }

        out_params = self.call_action("AddProxyDevice", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DeviceJID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AddUCSAccount(self, UserAtCloud, Port, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddUCSAccount action.

            :returns: "UCSJID", "Password"
        """
        arguments = {
            "UserAtCloud": UserAtCloud,
            "Port": Port,
        }

        out_params = self.call_action("AddUCSAccount", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("UCSJID", "Password",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteProxyDevice(self, DeviceJID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteProxyDevice action.
        """
        arguments = {
            "DeviceJID": DeviceJID,
        }

        self.call_action("DeleteProxyDevice", arguments=arguments, aspects=aspects)

        return

    def action_DeleteUCSAccount(self, BareJID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteUCSAccount action.
        """
        arguments = {
            "BareJID": BareJID,
        }

        self.call_action("DeleteUCSAccount", arguments=arguments, aspects=aspects)

        return

    def action_GetDeviceList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDeviceList action.

            :returns: "DeviceList"
        """
        arguments = { }

        out_params = self.call_action("GetDeviceList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DeviceList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetProxyList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetProxyList action.

            :returns: "ProxyList"
        """
        arguments = { }

        out_params = self.call_action("GetProxyList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ProxyList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUCSList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUCSList action.

            :returns: "UCSList"
        """
        arguments = { }

        out_params = self.call_action("GetUCSList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("UCSList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
