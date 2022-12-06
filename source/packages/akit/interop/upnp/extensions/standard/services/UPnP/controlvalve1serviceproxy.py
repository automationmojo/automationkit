"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ControlValve1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ControlValve1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ControlValve:1'

    SERVICE_DEFAULT_VARIABLES = {
        "ControlMode": { "data_type": "string", "default": "CLOSED", "allowed_list": "['OPEN', 'CLOSED', 'AUTO']"},
        "MaxPosition": { "data_type": "ui1", "default": "100", "allowed_list": None},
        "MinPosition": { "data_type": "ui1", "default": "0", "allowed_list": None},
        "PositionStatus": { "data_type": "ui1", "default": "0", "allowed_list": None},
        "PositionTarget": { "data_type": "ui1", "default": "0", "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetMinMax(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMinMax action.

            :returns: "CurrentMinPosition", "CurrentMaxPosition"
        """
        arguments = { }

        out_params = self.call_action("GetMinMax", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentMinPosition", "CurrentMaxPosition",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMode(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMode action.

            :returns: "CurrentControlMode"
        """
        arguments = { }

        out_params = self.call_action("GetMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentControlMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPosition(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPosition action.

            :returns: "CurrentPositionStatus"
        """
        arguments = { }

        out_params = self.call_action("GetPosition", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentPositionStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPositionTarget(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPositionTarget action.

            :returns: "CurrentPositionTarget"
        """
        arguments = { }

        out_params = self.call_action("GetPositionTarget", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentPositionTarget",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetMinMax(self, NewMinPosition, NewMaxPosition, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetMinMax action.
        """
        arguments = {
            "NewMinPosition": NewMinPosition,
            "NewMaxPosition": NewMaxPosition,
        }

        self.call_action("SetMinMax", arguments=arguments, aspects=aspects)

        return

    def action_SetMode(self, NewControlMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetMode action.
        """
        arguments = {
            "NewControlMode": NewControlMode,
        }

        self.call_action("SetMode", arguments=arguments, aspects=aspects)

        return

    def action_SetPosition(self, NewPositionTarget, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetPosition action.
        """
        arguments = {
            "NewPositionTarget": NewPositionTarget,
        }

        self.call_action("SetPosition", arguments=arguments, aspects=aspects)

        return
