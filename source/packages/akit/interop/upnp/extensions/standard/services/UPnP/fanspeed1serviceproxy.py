"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class FanSpeed1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'FanSpeed1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:FanSpeed:1'

    SERVICE_DEFAULT_VARIABLES = {
        "DirectionStatus": { "data_type": "boolean", "default": "0", "allowed_list": None},
        "DirectionTarget": { "data_type": "boolean", "default": "0", "allowed_list": None},
        "FanSpeedStatus": { "data_type": "ui1", "default": "0", "allowed_list": None},
        "FanSpeedTarget": { "data_type": "ui1", "default": "0", "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetFanDirection(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFanDirection action.

            :returns: "CurrentDirectionStatus"
        """
        arguments = { }

        out_params = self.call_action("GetFanDirection", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentDirectionStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFanDirectionTarget(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFanDirectionTarget action.

            :returns: "CurrentDirectionTarget"
        """
        arguments = { }

        out_params = self.call_action("GetFanDirectionTarget", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentDirectionTarget",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFanSpeed(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFanSpeed action.

            :returns: "CurrentFanSpeedStatus"
        """
        arguments = { }

        out_params = self.call_action("GetFanSpeed", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentFanSpeedStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFanSpeedTarget(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFanSpeedTarget action.

            :returns: "CurrentFanSpeedTarget"
        """
        arguments = { }

        out_params = self.call_action("GetFanSpeedTarget", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentFanSpeedTarget",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetFanDirection(self, NewDirectionTarget, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetFanDirection action.
        """
        arguments = {
            "NewDirectionTarget": NewDirectionTarget,
        }

        self.call_action("SetFanDirection", arguments=arguments, aspects=aspects)

        return

    def action_SetFanSpeed(self, NewFanSpeedTarget, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetFanSpeed action.
        """
        arguments = {
            "NewFanSpeedTarget": NewFanSpeedTarget,
        }

        self.call_action("SetFanSpeed", arguments=arguments, aspects=aspects)

        return
