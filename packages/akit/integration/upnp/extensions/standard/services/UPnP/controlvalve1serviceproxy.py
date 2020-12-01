"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ControlValve1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ControlValve1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ControlValve:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_GetMinMax(self, extract_returns=True):
        """
            Calls the GetMinMax action.

            :returns: "CurrentMinPosition", "CurrentMaxPosition"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetMinMax", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentMinPosition", "CurrentMaxPosition",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMode(self, extract_returns=True):
        """
            Calls the GetMode action.

            :returns: "CurrentControlMode"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetMode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentControlMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPosition(self, extract_returns=True):
        """
            Calls the GetPosition action.

            :returns: "CurrentPositionStatus"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetPosition", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentPositionStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPositionTarget(self, extract_returns=True):
        """
            Calls the GetPositionTarget action.

            :returns: "CurrentPositionTarget"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetPositionTarget", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentPositionTarget",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetMinMax(self, NewMinPosition, NewMaxPosition, extract_returns=True):
        """
            Calls the SetMinMax action.

            :returns: "result"
        """
        arguments = {
            "NewMinPosition": NewMinPosition,
            "NewMaxPosition": NewMaxPosition,
        }

        out_params = self._proxy_call_action("SetMinMax", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetMode(self, NewControlMode, extract_returns=True):
        """
            Calls the SetMode action.

            :returns: "result"
        """
        arguments = {
            "NewControlMode": NewControlMode,
        }

        out_params = self._proxy_call_action("SetMode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetPosition(self, NewPositionTarget, extract_returns=True):
        """
            Calls the SetPosition action.

            :returns: "result"
        """
        arguments = {
            "NewPositionTarget": NewPositionTarget,
        }

        out_params = self._proxy_call_action("SetPosition", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
