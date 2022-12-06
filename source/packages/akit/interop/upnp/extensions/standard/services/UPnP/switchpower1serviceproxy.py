"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class SwitchPower1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'SwitchPower1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:SwitchPower:1'

    SERVICE_DEFAULT_VARIABLES = {
        "Status": { "data_type": "boolean", "default": "0", "allowed_list": None},
        "Target": { "data_type": "boolean", "default": "0", "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetStatus(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetStatus action.

            :returns: "ResultStatus"
        """
        arguments = { }

        out_params = self.call_action("GetStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ResultStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTarget(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTarget action.

            :returns: "RetTargetValue"
        """
        arguments = { }

        out_params = self.call_action("GetTarget", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetTargetValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetTarget(self, newTargetValue, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetTarget action.
        """
        arguments = {
            "newTargetValue": newTargetValue,
        }

        self.call_action("SetTarget", arguments=arguments, aspects=aspects)

        return
