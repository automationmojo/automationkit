"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Messaging1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Messaging1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Messaging:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "NewMessages": { "data_type": "string", "default": None, "allowed_list": None},
        "SessionUpdates": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AcceptSession(self, SessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AcceptSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self.call_action("AcceptSession", arguments=arguments, aspects=aspects)

        return

    def action_CancelFileTransfer(self, SessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CancelFileTransfer action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self.call_action("CancelFileTransfer", arguments=arguments, aspects=aspects)

        return

    def action_CloseSession(self, SessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CloseSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self.call_action("CloseSession", arguments=arguments, aspects=aspects)

        return

    def action_CreateSession(self, SessionClass, SessionRecipients, Subject, SupportedContentType, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateSession action.

            :returns: "SessionID"
        """
        arguments = {
            "SessionClass": SessionClass,
            "SessionRecipients": SessionRecipients,
            "Subject": Subject,
            "SupportedContentType": SupportedContentType,
        }

        out_params = self.call_action("CreateSession", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SessionID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteMessage(self, MessageID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteMessage action.
        """
        arguments = {
            "MessageID": MessageID,
        }

        self.call_action("DeleteMessage", arguments=arguments, aspects=aspects)

        return

    def action_GetFileTransferSession(self, SessionID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFileTransferSession action.

            :returns: "FileInfoList"
        """
        arguments = {
            "SessionID": SessionID,
        }

        out_params = self.call_action("GetFileTransferSession", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FileInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMessagingCapabilities(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMessagingCapabilities action.

            :returns: "SupportedCapabilities"
        """
        arguments = { }

        out_params = self.call_action("GetMessagingCapabilities", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedCapabilities",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetNewMessages(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetNewMessages action.

            :returns: "NewMessages"
        """
        arguments = { }

        out_params = self.call_action("GetNewMessages", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewMessages",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSessionUpdates(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSessionUpdates action.

            :returns: "SessionUpdates"
        """
        arguments = { }

        out_params = self.call_action("GetSessionUpdates", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SessionUpdates",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSessions(self, SessionID, SessionClass, SessionStatus, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSessions action.

            :returns: "SessionsList"
        """
        arguments = {
            "SessionID": SessionID,
            "SessionClass": SessionClass,
            "SessionStatus": SessionStatus,
        }

        out_params = self.call_action("GetSessions", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SessionsList",)]
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

    def action_JoinSession(self, SessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the JoinSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self.call_action("JoinSession", arguments=arguments, aspects=aspects)

        return

    def action_LeaveSession(self, SessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the LeaveSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self.call_action("LeaveSession", arguments=arguments, aspects=aspects)

        return

    def action_ModifySession(self, SessionID, SessionRecipientsToAdd, SessionRecipientsToRemove, Subject, SupportedContentType, SessionClass, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ModifySession action.
        """
        arguments = {
            "SessionID": SessionID,
            "SessionRecipientsToAdd": SessionRecipientsToAdd,
            "SessionRecipientsToRemove": SessionRecipientsToRemove,
            "Subject": Subject,
            "SupportedContentType": SupportedContentType,
            "SessionClass": SessionClass,
        }

        self.call_action("ModifySession", arguments=arguments, aspects=aspects)

        return

    def action_ReadMessage(self, MessageID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ReadMessage action.

            :returns: "MessageRequested"
        """
        arguments = {
            "MessageID": MessageID,
        }

        out_params = self.call_action("ReadMessage", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MessageRequested",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SearchMessages(self, MessageClass, MessageFolder, MessageStatus, SessionID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SearchMessages action.

            :returns: "MessageList"
        """
        arguments = {
            "MessageClass": MessageClass,
            "MessageFolder": MessageFolder,
            "MessageStatus": MessageStatus,
            "SessionID": SessionID,
        }

        out_params = self.call_action("SearchMessages", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MessageList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SendMessage(self, MessageToSend, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SendMessage action.

            :returns: "MessageID"
        """
        arguments = {
            "MessageToSend": MessageToSend,
        }

        out_params = self.call_action("SendMessage", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MessageID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StartFileTransfer(self, FileInfoList, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartFileTransfer action.
        """
        arguments = {
            "FileInfoList": FileInfoList,
        }

        self.call_action("StartFileTransfer", arguments=arguments, aspects=aspects)

        return
