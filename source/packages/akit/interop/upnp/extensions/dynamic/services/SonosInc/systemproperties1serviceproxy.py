"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class SystemProperties1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'SystemProperties1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:SystemProperties:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "CustomerID": { "data_type": "string", "default": None, "allowed_list": None},
        "ThirdPartyHash": { "data_type": "string", "default": None, "allowed_list": None},
        "UpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "UpdateIDX": { "data_type": "ui4", "default": None, "allowed_list": None},
        "VoiceUpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
    }

    def action_AddAccountX(self, AccountType, AccountID, AccountPassword, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddAccountX action.

            :returns: "AccountUDN"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
            "AccountPassword": AccountPassword,
        }

        out_params = self.call_action("AddAccountX", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AccountUDN",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AddOAuthAccountX(self, AccountType, AccountToken, AccountKey, OAuthDeviceID, AuthorizationCode, RedirectURI, UserIdHashCode, AccountTier, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddOAuthAccountX action.

            :returns: "AccountUDN", "AccountNickname"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountToken": AccountToken,
            "AccountKey": AccountKey,
            "OAuthDeviceID": OAuthDeviceID,
            "AuthorizationCode": AuthorizationCode,
            "RedirectURI": RedirectURI,
            "UserIdHashCode": UserIdHashCode,
            "AccountTier": AccountTier,
        }

        out_params = self.call_action("AddOAuthAccountX", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AccountUDN", "AccountNickname",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DoPostUpdateTasks(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DoPostUpdateTasks action.
        """
        arguments = { }

        self.call_action("DoPostUpdateTasks", arguments=arguments, aspects=aspects)

        return

    def action_EditAccountMd(self, AccountType, AccountID, NewAccountMd, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the EditAccountMd action.
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
            "NewAccountMd": NewAccountMd,
        }

        self.call_action("EditAccountMd", arguments=arguments, aspects=aspects)

        return

    def action_EditAccountPasswordX(self, AccountType, AccountID, NewAccountPassword, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the EditAccountPasswordX action.
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
            "NewAccountPassword": NewAccountPassword,
        }

        self.call_action("EditAccountPasswordX", arguments=arguments, aspects=aspects)

        return

    def action_EnableRDM(self, RDMValue, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the EnableRDM action.
        """
        arguments = {
            "RDMValue": RDMValue,
        }

        self.call_action("EnableRDM", arguments=arguments, aspects=aspects)

        return

    def action_GetRDM(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRDM action.

            :returns: "RDMValue"
        """
        arguments = { }

        out_params = self.call_action("GetRDM", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RDMValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetString(self, VariableName, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetString action.

            :returns: "StringValue"
        """
        arguments = {
            "VariableName": VariableName,
        }

        out_params = self.call_action("GetString", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StringValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetWebCode(self, AccountType, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetWebCode action.

            :returns: "WebCode"
        """
        arguments = {
            "AccountType": AccountType,
        }

        out_params = self.call_action("GetWebCode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("WebCode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ProvisionCredentialedTrialAccountX(self, AccountType, AccountID, AccountPassword, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ProvisionCredentialedTrialAccountX action.

            :returns: "IsExpired", "AccountUDN"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
            "AccountPassword": AccountPassword,
        }

        out_params = self.call_action("ProvisionCredentialedTrialAccountX", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("IsExpired", "AccountUDN",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RefreshAccountCredentialsX(self, AccountType, AccountUID, AccountToken, AccountKey, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RefreshAccountCredentialsX action.
        """
        arguments = {
            "AccountType": AccountType,
            "AccountUID": AccountUID,
            "AccountToken": AccountToken,
            "AccountKey": AccountKey,
        }

        self.call_action("RefreshAccountCredentialsX", arguments=arguments, aspects=aspects)

        return

    def action_Remove(self, VariableName, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Remove action.
        """
        arguments = {
            "VariableName": VariableName,
        }

        self.call_action("Remove", arguments=arguments, aspects=aspects)

        return

    def action_RemoveAccount(self, AccountType, AccountID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveAccount action.
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
        }

        self.call_action("RemoveAccount", arguments=arguments, aspects=aspects)

        return

    def action_ReplaceAccountX(self, AccountUDN, NewAccountID, NewAccountPassword, AccountToken, AccountKey, OAuthDeviceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ReplaceAccountX action.

            :returns: "NewAccountUDN"
        """
        arguments = {
            "AccountUDN": AccountUDN,
            "NewAccountID": NewAccountID,
            "NewAccountPassword": NewAccountPassword,
            "AccountToken": AccountToken,
            "AccountKey": AccountKey,
            "OAuthDeviceID": OAuthDeviceID,
        }

        out_params = self.call_action("ReplaceAccountX", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAccountUDN",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetThirdPartyCredentials(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ResetThirdPartyCredentials action.
        """
        arguments = { }

        self.call_action("ResetThirdPartyCredentials", arguments=arguments, aspects=aspects)

        return

    def action_SetAccountNicknameX(self, AccountUDN, AccountNickname, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAccountNicknameX action.
        """
        arguments = {
            "AccountUDN": AccountUDN,
            "AccountNickname": AccountNickname,
        }

        self.call_action("SetAccountNicknameX", arguments=arguments, aspects=aspects)

        return

    def action_SetString(self, VariableName, StringValue, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetString action.
        """
        arguments = {
            "VariableName": VariableName,
            "StringValue": StringValue,
        }

        self.call_action("SetString", arguments=arguments, aspects=aspects)

        return
