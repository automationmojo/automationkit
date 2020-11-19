"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class DeviceProtection1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'DeviceProtection1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:DeviceProtection:1'
    
    SERVICE_EVENT_VARIABLES = {}


    def action_AddIdentityList(self, IdentityList, extract_returns=True):
        """
            Calls the AddIdentityList action.

            :returns: "IdentityListResult"
        """
        arguments = {
            "IdentityList": IdentityList,
        }

        out_params = self._proxy_call_action("AddIdentityList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("IdentityListResult",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_AddRolesForIdentity(self, Identity, RoleList, extract_returns=True):
        """
            Calls the AddRolesForIdentity action.

            :returns: "result"
        """
        arguments = {
            "Identity": Identity,
            "RoleList": RoleList,
        }

        out_params = self._proxy_call_action("AddRolesForIdentity", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetACLData(self, extract_returns=True):
        """
            Calls the GetACLData action.

            :returns: "ACL"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetACLData", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ACL",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetAssignedRoles(self, extract_returns=True):
        """
            Calls the GetAssignedRoles action.

            :returns: "RoleList"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetAssignedRoles", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RoleList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetRolesForAction(self, DeviceUDN, ServiceId, ActionName, extract_returns=True):
        """
            Calls the GetRolesForAction action.

            :returns: "RoleList", "RestrictedRoleList"
        """
        arguments = {
            "DeviceUDN": DeviceUDN,
            "ServiceId": ServiceId,
            "ActionName": ActionName,
        }

        out_params = self._proxy_call_action("GetRolesForAction", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RoleList", "RestrictedRoleList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetSupportedProtocols(self, extract_returns=True):
        """
            Calls the GetSupportedProtocols action.

            :returns: "ProtocolList"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetSupportedProtocols", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ProtocolList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetUserLoginChallenge(self, ProtocolType, Name, extract_returns=True):
        """
            Calls the GetUserLoginChallenge action.

            :returns: "Salt", "Challenge"
        """
        arguments = {
            "ProtocolType": ProtocolType,
            "Name": Name,
        }

        out_params = self._proxy_call_action("GetUserLoginChallenge", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Salt", "Challenge",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_RemoveIdentity(self, Identity, extract_returns=True):
        """
            Calls the RemoveIdentity action.

            :returns: "result"
        """
        arguments = {
            "Identity": Identity,
        }

        out_params = self._proxy_call_action("RemoveIdentity", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_RemoveRolesForIdentity(self, Identity, RoleList, extract_returns=True):
        """
            Calls the RemoveRolesForIdentity action.

            :returns: "result"
        """
        arguments = {
            "Identity": Identity,
            "RoleList": RoleList,
        }

        out_params = self._proxy_call_action("RemoveRolesForIdentity", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_SendSetupMessage(self, ProtocolType, InMessage, extract_returns=True):
        """
            Calls the SendSetupMessage action.

            :returns: "OutMessage"
        """
        arguments = {
            "ProtocolType": ProtocolType,
            "InMessage": InMessage,
        }

        out_params = self._proxy_call_action("SendSetupMessage", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OutMessage",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_SetUserLoginPassword(self, ProtocolType, Name, Stored, Salt, extract_returns=True):
        """
            Calls the SetUserLoginPassword action.

            :returns: "result"
        """
        arguments = {
            "ProtocolType": ProtocolType,
            "Name": Name,
            "Stored": Stored,
            "Salt": Salt,
        }

        out_params = self._proxy_call_action("SetUserLoginPassword", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_UserLogin(self, ProtocolType, Challenge, Authenticator, extract_returns=True):
        """
            Calls the UserLogin action.

            :returns: "result"
        """
        arguments = {
            "ProtocolType": ProtocolType,
            "Challenge": Challenge,
            "Authenticator": Authenticator,
        }

        out_params = self._proxy_call_action("UserLogin", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_UserLogout(self, extract_returns=True):
        """
            Calls the UserLogout action.

            :returns: "result"
        """
        arguments = { }

        out_params = self._proxy_call_action("UserLogout", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

