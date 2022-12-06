"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class CallManagement2ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'CallManagement2' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:CallManagement:2'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "CallBackAvailability": { "data_type": "string", "default": None, "allowed_list": None},
        "CallInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "ParallelCallInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "PushInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "TelCPNameList": { "data_type": "string", "default": None, "allowed_list": None},
        "VoiceMailInfo": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AcceptCall(self, TelCPName, SecretKey, TargetCallID, MediaCapabilityInfo, CallMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AcceptCall action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "TargetCallID": TargetCallID,
            "MediaCapabilityInfo": MediaCapabilityInfo,
            "CallMode": CallMode,
        }

        self.call_action("AcceptCall", arguments=arguments, aspects=aspects)

        return

    def action_AcceptModifyCall(self, TelCPName, SecretKey, TargetCallID, MediaCapabilityInfo, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AcceptModifyCall action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "TargetCallID": TargetCallID,
            "MediaCapabilityInfo": MediaCapabilityInfo,
        }

        self.call_action("AcceptModifyCall", arguments=arguments, aspects=aspects)

        return

    def action_AcceptParallelCall(self, ParallelCalleeID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AcceptParallelCall action.
        """
        arguments = {
            "ParallelCalleeID": ParallelCalleeID,
        }

        self.call_action("AcceptParallelCall", arguments=arguments, aspects=aspects)

        return

    def action_ChangeCallMode(self, TelCPName, SecretKey, CallID, CallMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ChangeCallMode action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "CallID": CallID,
            "CallMode": CallMode,
        }

        self.call_action("ChangeCallMode", arguments=arguments, aspects=aspects)

        return

    def action_ChangeMonopolizer(self, CurrentMonopolizer, SecretKey, TargetCallID, NewMonopolizer, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ChangeMonopolizer action.
        """
        arguments = {
            "CurrentMonopolizer": CurrentMonopolizer,
            "SecretKey": SecretKey,
            "TargetCallID": TargetCallID,
            "NewMonopolizer": NewMonopolizer,
        }

        self.call_action("ChangeMonopolizer", arguments=arguments, aspects=aspects)

        return

    def action_ChangeTelCPName(self, CurrentTelCPName, CurrentSecretKey, NewTelCPName, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ChangeTelCPName action.

            :returns: "NewSecretKey", "Expires"
        """
        arguments = {
            "CurrentTelCPName": CurrentTelCPName,
            "CurrentSecretKey": CurrentSecretKey,
            "NewTelCPName": NewTelCPName,
        }

        out_params = self.call_action("ChangeTelCPName", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewSecretKey", "Expires",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ClearCallBack(self, CallBackID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ClearCallBack action.
        """
        arguments = {
            "CallBackID": CallBackID,
        }

        self.call_action("ClearCallBack", arguments=arguments, aspects=aspects)

        return

    def action_ClearCallLogs(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ClearCallLogs action.
        """
        arguments = { }

        self.call_action("ClearCallLogs", arguments=arguments, aspects=aspects)

        return

    def action_DeleteVoiceMail(self, TelCPName, SecretKey, VoiceMailID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteVoiceMail action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "VoiceMailID": VoiceMailID,
        }

        self.call_action("DeleteVoiceMail", arguments=arguments, aspects=aspects)

        return

    def action_EnhancedInitiateCall(self, CalleeID, CallType, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the EnhancedInitiateCall action.

            :returns: "CallID"
        """
        arguments = {
            "CalleeID": CalleeID,
            "CallType": CallType,
        }

        out_params = self.call_action("EnhancedInitiateCall", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CallID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCallBackInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCallBackInfo action.

            :returns: "CallBackInfo"
        """
        arguments = { }

        out_params = self.call_action("GetCallBackInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CallBackInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCallInfo(self, TelCPName, SecretKey, TargetCallID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCallInfo action.

            :returns: "CallInfoList"
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "TargetCallID": TargetCallID,
        }

        out_params = self.call_action("GetCallInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CallInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCallLogs(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCallLogs action.

            :returns: "CallLogs"
        """
        arguments = { }

        out_params = self.call_action("GetCallLogs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CallLogs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMediaCapabilities(self, TCMediaCapabilityInfo, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMediaCapabilities action.

            :returns: "SupportedMediaCapabilityInfo"
        """
        arguments = {
            "TCMediaCapabilityInfo": TCMediaCapabilityInfo,
        }

        out_params = self.call_action("GetMediaCapabilities", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedMediaCapabilityInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPushInfo(self, PushInfoList, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPushInfo action.
        """
        arguments = {
            "PushInfoList": PushInfoList,
        }

        self.call_action("GetPushInfo", arguments=arguments, aspects=aspects)

        return

    def action_GetTelCPNameList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTelCPNameList action.

            :returns: "TelCPNameList"
        """
        arguments = { }

        out_params = self.call_action("GetTelCPNameList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TelCPNameList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTelephonyIdentity(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTelephonyIdentity action.

            :returns: "TelephonyIdentity"
        """
        arguments = { }

        out_params = self.call_action("GetTelephonyIdentity", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TelephonyIdentity",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVoiceMail(self, TelCPName, SecretKey, VoiceMailID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetVoiceMail action.

            :returns: "VoiceMailInfoList"
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "VoiceMailID": VoiceMailID,
        }

        out_params = self.call_action("GetVoiceMail", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("VoiceMailInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_IgnoreCall(self, TelCPName, SecretKey, CallID, IgnoreReason, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the IgnoreCall action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "CallID": CallID,
            "IgnoreReason": IgnoreReason,
        }

        self.call_action("IgnoreCall", arguments=arguments, aspects=aspects)

        return

    def action_InitiateCall(self, CalleeID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the InitiateCall action.

            :returns: "CallID"
        """
        arguments = {
            "CalleeID": CalleeID,
        }

        out_params = self.call_action("InitiateCall", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CallID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_InitiateParallelCall(self, ParallelCallerID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the InitiateParallelCall action.
        """
        arguments = {
            "ParallelCallerID": ParallelCallerID,
        }

        self.call_action("InitiateParallelCall", arguments=arguments, aspects=aspects)

        return

    def action_ModifyCall(self, TelCPName, SecretKey, TargetCallID, MediaCapabilityInfo, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ModifyCall action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "TargetCallID": TargetCallID,
            "MediaCapabilityInfo": MediaCapabilityInfo,
        }

        self.call_action("ModifyCall", arguments=arguments, aspects=aspects)

        return

    def action_RegisterCallBack(self, CalleeID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RegisterCallBack action.

            :returns: "CallBackID"
        """
        arguments = {
            "CalleeID": CalleeID,
        }

        out_params = self.call_action("RegisterCallBack", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CallBackID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RegisterTelCPName(self, TelCPName, CurrentSecretKey, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RegisterTelCPName action.

            :returns: "NewSecretKey", "Expires"
        """
        arguments = {
            "TelCPName": TelCPName,
            "CurrentSecretKey": CurrentSecretKey,
        }

        out_params = self.call_action("RegisterTelCPName", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewSecretKey", "Expires",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RejectCall(self, TelCPName, SecretKey, TargetCallID, RejectReason, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RejectCall action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "TargetCallID": TargetCallID,
            "RejectReason": RejectReason,
        }

        self.call_action("RejectCall", arguments=arguments, aspects=aspects)

        return

    def action_StartCall(self, TelCPName, SecretKey, CalleeID, CallPriority, MediaCapabilityInfo, CallMode, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartCall action.

            :returns: "CallID"
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "CalleeID": CalleeID,
            "CallPriority": CallPriority,
            "MediaCapabilityInfo": MediaCapabilityInfo,
            "CallMode": CallMode,
        }

        out_params = self.call_action("StartCall", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CallID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StartMediaTransfer(self, TelCPName, SecretKey, TargetCallID, TCList, MediaCapabilityInfo, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartMediaTransfer action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "TargetCallID": TargetCallID,
            "TCList": TCList,
            "MediaCapabilityInfo": MediaCapabilityInfo,
        }

        self.call_action("StartMediaTransfer", arguments=arguments, aspects=aspects)

        return

    def action_StopCall(self, TelCPName, SecretKey, CallID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StopCall action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
            "CallID": CallID,
        }

        self.call_action("StopCall", arguments=arguments, aspects=aspects)

        return

    def action_UnregisterTelCPName(self, TelCPName, SecretKey, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UnregisterTelCPName action.
        """
        arguments = {
            "TelCPName": TelCPName,
            "SecretKey": SecretKey,
        }

        self.call_action("UnregisterTelCPName", arguments=arguments, aspects=aspects)

        return

    def action_WaitingForCall(self, CallerID, MaxWaitingTime, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the WaitingForCall action.
        """
        arguments = {
            "CallerID": CallerID,
            "MaxWaitingTime": MaxWaitingTime,
        }

        self.call_action("WaitingForCall", arguments=arguments, aspects=aspects)

        return
