"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class InputConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'InputConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:InputConfig:1'

    SERVICE_DEFAULT_VARIABLES = {
        "InputConnectionList": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "DeviceInputCapability": { "data_type": "string", "default": None, "allowed_list": None},
        "RequiredInputType": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_GetInputCapability(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetInputCapability action.

            :returns: "SupportedCapabilities"
        """
        arguments = { }

        out_params = self.call_action("GetInputCapability", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedCapabilities",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetInputConnectionList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetInputConnectionList action.

            :returns: "CurrentConnectionList"
        """
        arguments = { }

        out_params = self.call_action("GetInputConnectionList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentConnectionList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetInputSession(self, SelectedCapability, ReceiverInfo, PeerDeviceInfo, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetInputSession action.

            :returns: "SessionID", "ConnectionInfo"
        """
        arguments = {
            "SelectedCapability": SelectedCapability,
            "ReceiverInfo": ReceiverInfo,
            "PeerDeviceInfo": PeerDeviceInfo,
        }

        out_params = self.call_action("SetInputSession", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SessionID", "ConnectionInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetMonopolizedSender(self, OwnerDeviceInfo, OwnedSessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetMonopolizedSender action.
        """
        arguments = {
            "OwnerDeviceInfo": OwnerDeviceInfo,
            "OwnedSessionID": OwnedSessionID,
        }

        self.call_action("SetMonopolizedSender", arguments=arguments, aspects=aspects)

        return

    def action_SetMultiInputMode(self, NewMultiInputMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetMultiInputMode action.
        """
        arguments = {
            "NewMultiInputMode": NewMultiInputMode,
        }

        self.call_action("SetMultiInputMode", arguments=arguments, aspects=aspects)

        return

    def action_StartInputSession(self, SessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartInputSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self.call_action("StartInputSession", arguments=arguments, aspects=aspects)

        return

    def action_StopInputsession(self, SessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StopInputsession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self.call_action("StopInputsession", arguments=arguments, aspects=aspects)

        return

    def action_SwitchInputSession(self, SessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SwitchInputSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self.call_action("SwitchInputSession", arguments=arguments, aspects=aspects)

        return
