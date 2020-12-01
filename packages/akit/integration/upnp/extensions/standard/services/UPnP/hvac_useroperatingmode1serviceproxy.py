"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class HVAC_UserOperatingMode1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'HVAC_UserOperatingMode1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:HVAC_UserOperatingMode:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_GetModeStatus(self, extract_returns=True):
        """
            Calls the GetModeStatus action.

            :returns: "CurrentModeStatus"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetModeStatus", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentModeStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetModeTarget(self, extract_returns=True):
        """
            Calls the GetModeTarget action.

            :returns: "CurrentModeTarget"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetModeTarget", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentModeTarget",)]
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

    def action_SetModeTarget(self, NewModeTarget, extract_returns=True):
        """
            Calls the SetModeTarget action.

            :returns: "result"
        """
        arguments = {
            "NewModeTarget": NewModeTarget,
        }

        out_params = self._proxy_call_action("SetModeTarget", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetName(self, NewName, extract_returns=True):
        """
            Calls the SetName action.

            :returns: "result"
        """
        arguments = {
            "NewName": NewName,
        }

        out_params = self._proxy_call_action("SetName", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
