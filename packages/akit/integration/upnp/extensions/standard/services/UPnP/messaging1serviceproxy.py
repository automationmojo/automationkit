"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Messaging1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Messaging1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Messaging:1'

    SERVICE_EVENT_VARIABLES = {
        "NewMessages": { "data_type": "string", "default": None, "allowed_list": None},
        "SessionUpdates": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AcceptSession(self, SessionID):
        """
            Calls the AcceptSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self._proxy_call_action("AcceptSession", arguments=arguments)

        return

    def action_CancelFileTransfer(self, SessionID):
        """
            Calls the CancelFileTransfer action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self._proxy_call_action("CancelFileTransfer", arguments=arguments)

        return

    def action_CloseSession(self, SessionID):
        """
            Calls the CloseSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self._proxy_call_action("CloseSession", arguments=arguments)

        return

    def action_CreateSession(self, SessionClass, SessionRecipients, Subject, SupportedContentType, extract_returns=True):
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

        out_params = self._proxy_call_action("CreateSession", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SessionID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteMessage(self, MessageID):
        """
            Calls the DeleteMessage action.
        """
        arguments = {
            "MessageID": MessageID,
        }

        self._proxy_call_action("DeleteMessage", arguments=arguments)

        return

    def action_GetFileTransferSession(self, SessionID, extract_returns=True):
        """
            Calls the GetFileTransferSession action.

            :returns: "FileInfoList"
        """
        arguments = {
            "SessionID": SessionID,
        }

        out_params = self._proxy_call_action("GetFileTransferSession", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FileInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMessagingCapabilities(self, extract_returns=True):
        """
            Calls the GetMessagingCapabilities action.

            :returns: "SupportedCapabilities"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetMessagingCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedCapabilities",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetNewMessages(self, extract_returns=True):
        """
            Calls the GetNewMessages action.

            :returns: "NewMessages"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetNewMessages", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewMessages",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSessionUpdates(self, extract_returns=True):
        """
            Calls the GetSessionUpdates action.

            :returns: "SessionUpdates"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetSessionUpdates", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SessionUpdates",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSessions(self, SessionID, SessionClass, SessionStatus, extract_returns=True):
        """
            Calls the GetSessions action.

            :returns: "SessionsList"
        """
        arguments = {
            "SessionID": SessionID,
            "SessionClass": SessionClass,
            "SessionStatus": SessionStatus,
        }

        out_params = self._proxy_call_action("GetSessions", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SessionsList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTelephonyIdentity(self, extract_returns=True):
        """
            Calls the GetTelephonyIdentity action.

            :returns: "TelephonyIdentity"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetTelephonyIdentity", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TelephonyIdentity",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_JoinSession(self, SessionID):
        """
            Calls the JoinSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self._proxy_call_action("JoinSession", arguments=arguments)

        return

    def action_LeaveSession(self, SessionID):
        """
            Calls the LeaveSession action.
        """
        arguments = {
            "SessionID": SessionID,
        }

        self._proxy_call_action("LeaveSession", arguments=arguments)

        return

    def action_ModifySession(self, SessionID, SessionRecipientsToAdd, SessionRecipientsToRemove, Subject, SupportedContentType, SessionClass):
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

        self._proxy_call_action("ModifySession", arguments=arguments)

        return

    def action_ReadMessage(self, MessageID, extract_returns=True):
        """
            Calls the ReadMessage action.

            :returns: "MessageRequested"
        """
        arguments = {
            "MessageID": MessageID,
        }

        out_params = self._proxy_call_action("ReadMessage", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MessageRequested",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SearchMessages(self, MessageClass, MessageFolder, MessageStatus, SessionID, extract_returns=True):
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

        out_params = self._proxy_call_action("SearchMessages", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MessageList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SendMessage(self, MessageToSend, extract_returns=True):
        """
            Calls the SendMessage action.

            :returns: "MessageID"
        """
        arguments = {
            "MessageToSend": MessageToSend,
        }

        out_params = self._proxy_call_action("SendMessage", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MessageID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StartFileTransfer(self, FileInfoList):
        """
            Calls the StartFileTransfer action.
        """
        arguments = {
            "FileInfoList": FileInfoList,
        }

        self._proxy_call_action("StartFileTransfer", arguments=arguments)

        return
