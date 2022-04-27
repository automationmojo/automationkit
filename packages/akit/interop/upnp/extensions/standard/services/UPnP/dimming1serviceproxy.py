"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Dimming1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Dimming1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Dimming:1'

    SERVICE_DEFAULT_VARIABLES = {
        "LoadLevelTarget": { "data_type": "ui1", "default": "0", "allowed_list": None},
        "OnEffect": { "data_type": "string", "default": "Default", "allowed_list": "['OnEffectLevel', 'LastSetting', 'Default']"},
        "OnEffectLevel": { "data_type": "ui1", "default": "100", "allowed_list": None},
        "RampTime": { "data_type": "ui4", "default": "0", "allowed_list": None},
        "ValidOutputValues": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "IsRamping": { "data_type": "boolean", "default": "0", "allowed_list": None},
        "LoadLevelStatus": { "data_type": "ui1", "default": "0", "allowed_list": None},
        "RampPaused": { "data_type": "boolean", "default": "0", "allowed_list": None},
        "RampRate": { "data_type": "ui1", "default": "0", "allowed_list": None},
        "StepDelta": { "data_type": "ui1", "default": "Manufacturer defined default value", "allowed_list": None},
    }

    def action_GetIsRamping(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetIsRamping action.

            :returns: "retIsRamping"
        """
        arguments = { }

        out_params = self.call_action("GetIsRamping", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("retIsRamping",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLoadLevelStatus(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLoadLevelStatus action.

            :returns: "retLoadlevelStatus"
        """
        arguments = { }

        out_params = self.call_action("GetLoadLevelStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("retLoadlevelStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLoadLevelTarget(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLoadLevelTarget action.

            :returns: "GetLoadlevelTarget"
        """
        arguments = { }

        out_params = self.call_action("GetLoadLevelTarget", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("GetLoadlevelTarget",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOnEffectParameters(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetOnEffectParameters action.

            :returns: "retOnEffect", "retOnEffectLevel"
        """
        arguments = { }

        out_params = self.call_action("GetOnEffectParameters", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("retOnEffect", "retOnEffectLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRampPaused(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRampPaused action.

            :returns: "retRampPaused"
        """
        arguments = { }

        out_params = self.call_action("GetRampPaused", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("retRampPaused",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRampRate(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRampRate action.

            :returns: "retRampRate"
        """
        arguments = { }

        out_params = self.call_action("GetRampRate", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("retRampRate",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRampTime(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRampTime action.

            :returns: "retRampTime"
        """
        arguments = { }

        out_params = self.call_action("GetRampTime", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("retRampTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetStepDelta(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetStepDelta action.

            :returns: "retStepDelta"
        """
        arguments = { }

        out_params = self.call_action("GetStepDelta", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("retStepDelta",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_PauseRamp(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the PauseRamp action.
        """
        arguments = { }

        self.call_action("PauseRamp", arguments=arguments, aspects=aspects)

        return

    def action_ResumeRamp(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ResumeRamp action.
        """
        arguments = { }

        self.call_action("ResumeRamp", arguments=arguments, aspects=aspects)

        return

    def action_SetLoadLevelTarget(self, newLoadlevelTarget, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetLoadLevelTarget action.
        """
        arguments = {
            "newLoadlevelTarget": newLoadlevelTarget,
        }

        self.call_action("SetLoadLevelTarget", arguments=arguments, aspects=aspects)

        return

    def action_SetOnEffect(self, newOnEffect, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetOnEffect action.
        """
        arguments = {
            "newOnEffect": newOnEffect,
        }

        self.call_action("SetOnEffect", arguments=arguments, aspects=aspects)

        return

    def action_SetOnEffectLevel(self, newOnEffectLevel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetOnEffectLevel action.
        """
        arguments = {
            "newOnEffectLevel": newOnEffectLevel,
        }

        self.call_action("SetOnEffectLevel", arguments=arguments, aspects=aspects)

        return

    def action_SetRampRate(self, newRampRate, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRampRate action.
        """
        arguments = {
            "newRampRate": newRampRate,
        }

        self.call_action("SetRampRate", arguments=arguments, aspects=aspects)

        return

    def action_SetStepDelta(self, newStepDelta, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetStepDelta action.
        """
        arguments = {
            "newStepDelta": newStepDelta,
        }

        self.call_action("SetStepDelta", arguments=arguments, aspects=aspects)

        return

    def action_StartRampDown(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartRampDown action.
        """
        arguments = { }

        self.call_action("StartRampDown", arguments=arguments, aspects=aspects)

        return

    def action_StartRampToLevel(self, newLoadLevelTarget, newRampTime, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartRampToLevel action.
        """
        arguments = {
            "newLoadLevelTarget": newLoadLevelTarget,
            "newRampTime": newRampTime,
        }

        self.call_action("StartRampToLevel", arguments=arguments, aspects=aspects)

        return

    def action_StartRampUp(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartRampUp action.
        """
        arguments = { }

        self.call_action("StartRampUp", arguments=arguments, aspects=aspects)

        return

    def action_StepDown(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StepDown action.
        """
        arguments = { }

        self.call_action("StepDown", arguments=arguments, aspects=aspects)

        return

    def action_StepUp(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StepUp action.
        """
        arguments = { }

        self.call_action("StepUp", arguments=arguments, aspects=aspects)

        return

    def action_StopRamp(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StopRamp action.
        """
        arguments = { }

        self.call_action("StopRamp", arguments=arguments, aspects=aspects)

        return
