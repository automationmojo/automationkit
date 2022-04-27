"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class DeviceProtection1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'DeviceProtection1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:DeviceProtection:1'

    SERVICE_DEFAULT_VARIABLES = {
        "SetupReady": { "data_type": "boolean", "default": None, "allowed_list": None},
        "SupportedProtocols": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_AddIdentityList(self, IdentityList, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddIdentityList action.

            :returns: "IdentityListResult"
        """
        arguments = {
            "IdentityList": IdentityList,
        }

        out_params = self.call_action("AddIdentityList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("IdentityListResult",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AddRolesForIdentity(self, Identity, RoleList, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddRolesForIdentity action.
        """
        arguments = {
            "Identity": Identity,
            "RoleList": RoleList,
        }

        self.call_action("AddRolesForIdentity", arguments=arguments, aspects=aspects)

        return

    def action_GetACLData(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetACLData action.

            :returns: "ACL"
        """
        arguments = { }

        out_params = self.call_action("GetACLData", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ACL",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAssignedRoles(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAssignedRoles action.

            :returns: "RoleList"
        """
        arguments = { }

        out_params = self.call_action("GetAssignedRoles", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RoleList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRolesForAction(self, DeviceUDN, ServiceId, ActionName, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRolesForAction action.

            :returns: "RoleList", "RestrictedRoleList"
        """
        arguments = {
            "DeviceUDN": DeviceUDN,
            "ServiceId": ServiceId,
            "ActionName": ActionName,
        }

        out_params = self.call_action("GetRolesForAction", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RoleList", "RestrictedRoleList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSupportedProtocols(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSupportedProtocols action.

            :returns: "ProtocolList"
        """
        arguments = { }

        out_params = self.call_action("GetSupportedProtocols", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ProtocolList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUserLoginChallenge(self, ProtocolType, Name, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUserLoginChallenge action.

            :returns: "Salt", "Challenge"
        """
        arguments = {
            "ProtocolType": ProtocolType,
            "Name": Name,
        }

        out_params = self.call_action("GetUserLoginChallenge", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Salt", "Challenge",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RemoveIdentity(self, Identity, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveIdentity action.
        """
        arguments = {
            "Identity": Identity,
        }

        self.call_action("RemoveIdentity", arguments=arguments, aspects=aspects)

        return

    def action_RemoveRolesForIdentity(self, Identity, RoleList, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveRolesForIdentity action.
        """
        arguments = {
            "Identity": Identity,
            "RoleList": RoleList,
        }

        self.call_action("RemoveRolesForIdentity", arguments=arguments, aspects=aspects)

        return

    def action_SendSetupMessage(self, ProtocolType, InMessage, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SendSetupMessage action.

            :returns: "OutMessage"
        """
        arguments = {
            "ProtocolType": ProtocolType,
            "InMessage": InMessage,
        }

        out_params = self.call_action("SendSetupMessage", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OutMessage",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetUserLoginPassword(self, ProtocolType, Name, Stored, Salt, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetUserLoginPassword action.
        """
        arguments = {
            "ProtocolType": ProtocolType,
            "Name": Name,
            "Stored": Stored,
            "Salt": Salt,
        }

        self.call_action("SetUserLoginPassword", arguments=arguments, aspects=aspects)

        return

    def action_UserLogin(self, ProtocolType, Challenge, Authenticator, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UserLogin action.
        """
        arguments = {
            "ProtocolType": ProtocolType,
            "Challenge": Challenge,
            "Authenticator": Authenticator,
        }

        self.call_action("UserLogin", arguments=arguments, aspects=aspects)

        return

    def action_UserLogout(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UserLogout action.
        """
        arguments = { }

        self.call_action("UserLogout", arguments=arguments, aspects=aspects)

        return
