"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class HVAC_FanOperatingMode1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'HVAC_FanOperatingMode1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:HVAC_FanOperatingMode:1'

    SERVICE_DEFAULT_VARIABLES = {
        "FanStatus": { "data_type": "string", "default": "On", "allowed_list": "['On', 'Off']"},
        "Mode": { "data_type": "string", "default": "Auto", "allowed_list": "['Auto', 'ContinuousOn', 'PeriodicOn']"},
        "Name": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetFanStatus(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFanStatus action.

            :returns: "CurrentStatus"
        """
        arguments = { }

        out_params = self.call_action("GetFanStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMode(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMode action.

            :returns: "CurrentMode"
        """
        arguments = { }

        out_params = self.call_action("GetMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetName(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetName action.

            :returns: "CurrentName"
        """
        arguments = { }

        out_params = self.call_action("GetName", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentName",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetMode(self, NewMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetMode action.
        """
        arguments = {
            "NewMode": NewMode,
        }

        self.call_action("SetMode", arguments=arguments, aspects=aspects)

        return

    def action_SetName(self, NewName, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetName action.
        """
        arguments = {
            "NewName": NewName,
        }

        self.call_action("SetName", arguments=arguments, aspects=aspects)

        return
