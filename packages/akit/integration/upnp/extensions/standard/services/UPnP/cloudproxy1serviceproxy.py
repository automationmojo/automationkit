"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class CloudProxy1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'CloudProxy1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:CloudProxy:1'

    SERVICE_EVENT_VARIABLES = {
        "CloudProxyUpdate": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddProxyDevice(self, DeviceId, UserAtCloud, extract_returns=True):
        """
            Calls the AddProxyDevice action.

            :returns: "DeviceJID"
        """
        arguments = {
            "DeviceId": DeviceId,
            "UserAtCloud": UserAtCloud,
        }

        out_params = self._proxy_call_action("AddProxyDevice", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DeviceJID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AddUCSAccount(self, UserAtCloud, Port, extract_returns=True):
        """
            Calls the AddUCSAccount action.

            :returns: "UCSJID", "Password"
        """
        arguments = {
            "UserAtCloud": UserAtCloud,
            "Port": Port,
        }

        out_params = self._proxy_call_action("AddUCSAccount", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("UCSJID", "Password",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteProxyDevice(self, DeviceJID):
        """
            Calls the DeleteProxyDevice action.
        """
        arguments = {
            "DeviceJID": DeviceJID,
        }

        self._proxy_call_action("DeleteProxyDevice", arguments=arguments)

        return

    def action_DeleteUCSAccount(self, BareJID):
        """
            Calls the DeleteUCSAccount action.
        """
        arguments = {
            "BareJID": BareJID,
        }

        self._proxy_call_action("DeleteUCSAccount", arguments=arguments)

        return

    def action_GetDeviceList(self, extract_returns=True):
        """
            Calls the GetDeviceList action.

            :returns: "DeviceList"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetDeviceList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DeviceList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetProxyList(self, extract_returns=True):
        """
            Calls the GetProxyList action.

            :returns: "ProxyList"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetProxyList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ProxyList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUCSList(self, extract_returns=True):
        """
            Calls the GetUCSList action.

            :returns: "UCSList"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetUCSList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("UCSList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
