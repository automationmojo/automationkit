"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class HVAC_FanOperatingMode1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'HVAC_FanOperatingMode1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:HVAC_FanOperatingMode:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_GetFanStatus(self, extract_returns=True):
        """
            Calls the GetFanStatus action.

            :returns: "CurrentStatus"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetFanStatus", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMode(self, extract_returns=True):
        """
            Calls the GetMode action.

            :returns: "CurrentMode"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetMode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetName(self, extract_returns=True):
        """
            Calls the GetName action.

            :returns: "CurrentName"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetName", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentName",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetMode(self, NewMode):
        """
            Calls the SetMode action.
        """
        arguments = {
            "NewMode": NewMode,
        }

        self._proxy_call_action("SetMode", arguments=arguments)

        return

    def action_SetName(self, NewName):
        """
            Calls the SetName action.
        """
        arguments = {
            "NewName": NewName,
        }

        self._proxy_call_action("SetName", arguments=arguments)

        return
