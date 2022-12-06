"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class HTControl1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'HTControl1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:HTControl:1'

    SERVICE_DEFAULT_VARIABLES = {
        "LEDFeedbackState": { "data_type": "string", "default": None, "allowed_list": "['On', 'Off']"},
        "RemoteConfigured": { "data_type": "boolean", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "IRRepeaterState": { "data_type": "string", "default": None, "allowed_list": "['On', 'Off', 'Disabled']"},
        "TOSLinkConnected": { "data_type": "boolean", "default": None, "allowed_list": None},
    }

    def action_CommitLearnedIRCodes(self, Name, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CommitLearnedIRCodes action.
        """
        arguments = {
            "Name": Name,
        }

        self.call_action("CommitLearnedIRCodes", arguments=arguments, aspects=aspects)

        return

    def action_GetIRRepeaterState(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetIRRepeaterState action.

            :returns: "CurrentIRRepeaterState"
        """
        arguments = { }

        out_params = self.call_action("GetIRRepeaterState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentIRRepeaterState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLEDFeedbackState(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLEDFeedbackState action.

            :returns: "LEDFeedbackState"
        """
        arguments = { }

        out_params = self.call_action("GetLEDFeedbackState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("LEDFeedbackState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_IdentifyIRRemote(self, Timeout, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the IdentifyIRRemote action.
        """
        arguments = {
            "Timeout": Timeout,
        }

        self.call_action("IdentifyIRRemote", arguments=arguments, aspects=aspects)

        return

    def action_IsRemoteConfigured(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the IsRemoteConfigured action.

            :returns: "RemoteConfigured"
        """
        arguments = { }

        out_params = self.call_action("IsRemoteConfigured", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RemoteConfigured",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_LearnIRCode(self, IRCode, Timeout, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the LearnIRCode action.
        """
        arguments = {
            "IRCode": IRCode,
            "Timeout": Timeout,
        }

        self.call_action("LearnIRCode", arguments=arguments, aspects=aspects)

        return

    def action_SetIRRepeaterState(self, DesiredIRRepeaterState, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetIRRepeaterState action.
        """
        arguments = {
            "DesiredIRRepeaterState": DesiredIRRepeaterState,
        }

        self.call_action("SetIRRepeaterState", arguments=arguments, aspects=aspects)

        return

    def action_SetLEDFeedbackState(self, LEDFeedbackState, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetLEDFeedbackState action.
        """
        arguments = {
            "LEDFeedbackState": LEDFeedbackState,
        }

        self.call_action("SetLEDFeedbackState", arguments=arguments, aspects=aspects)

        return
