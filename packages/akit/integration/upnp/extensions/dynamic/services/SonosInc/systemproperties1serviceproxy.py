"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class SystemProperties1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'SystemProperties1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:SystemProperties:1'

    SERVICE_EVENT_VARIABLES = {
        "CustomerID": { "data_type": "string", "default": None, "allowed_list": None},
        "ThirdPartyHash": { "data_type": "string", "default": None, "allowed_list": None},
        "UpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "UpdateIDX": { "data_type": "ui4", "default": None, "allowed_list": None},
        "VoiceUpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
    }

    def action_AddAccountX(self, AccountType, AccountID, AccountPassword, extract_returns=True):
        """
            Calls the AddAccountX action.

            :returns: "AccountUDN"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
            "AccountPassword": AccountPassword,
        }

        out_params = self._proxy_call_action("AddAccountX", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AccountUDN",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AddOAuthAccountX(self, AccountType, AccountToken, AccountKey, OAuthDeviceID, AuthorizationCode, RedirectURI, UserIdHashCode, AccountTier, extract_returns=True):
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

        out_params = self._proxy_call_action("AddOAuthAccountX", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AccountUDN", "AccountNickname",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DoPostUpdateTasks(self, extract_returns=True):
        """
            Calls the DoPostUpdateTasks action.

            :returns: "result"
        """
        arguments = { }

        out_params = self._proxy_call_action("DoPostUpdateTasks", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_EditAccountMd(self, AccountType, AccountID, NewAccountMd, extract_returns=True):
        """
            Calls the EditAccountMd action.

            :returns: "result"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
            "NewAccountMd": NewAccountMd,
        }

        out_params = self._proxy_call_action("EditAccountMd", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_EditAccountPasswordX(self, AccountType, AccountID, NewAccountPassword, extract_returns=True):
        """
            Calls the EditAccountPasswordX action.

            :returns: "result"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
            "NewAccountPassword": NewAccountPassword,
        }

        out_params = self._proxy_call_action("EditAccountPasswordX", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_EnableRDM(self, RDMValue, extract_returns=True):
        """
            Calls the EnableRDM action.

            :returns: "result"
        """
        arguments = {
            "RDMValue": RDMValue,
        }

        out_params = self._proxy_call_action("EnableRDM", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRDM(self, extract_returns=True):
        """
            Calls the GetRDM action.

            :returns: "RDMValue"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetRDM", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RDMValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetString(self, VariableName, extract_returns=True):
        """
            Calls the GetString action.

            :returns: "StringValue"
        """
        arguments = {
            "VariableName": VariableName,
        }

        out_params = self._proxy_call_action("GetString", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StringValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetWebCode(self, AccountType, extract_returns=True):
        """
            Calls the GetWebCode action.

            :returns: "WebCode"
        """
        arguments = {
            "AccountType": AccountType,
        }

        out_params = self._proxy_call_action("GetWebCode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("WebCode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ProvisionCredentialedTrialAccountX(self, AccountType, AccountID, AccountPassword, extract_returns=True):
        """
            Calls the ProvisionCredentialedTrialAccountX action.

            :returns: "IsExpired", "AccountUDN"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
            "AccountPassword": AccountPassword,
        }

        out_params = self._proxy_call_action("ProvisionCredentialedTrialAccountX", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("IsExpired", "AccountUDN",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RefreshAccountCredentialsX(self, AccountType, AccountUID, AccountToken, AccountKey, extract_returns=True):
        """
            Calls the RefreshAccountCredentialsX action.

            :returns: "result"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountUID": AccountUID,
            "AccountToken": AccountToken,
            "AccountKey": AccountKey,
        }

        out_params = self._proxy_call_action("RefreshAccountCredentialsX", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Remove(self, VariableName):
        """
            Calls the Remove action.

            :returns: "result"
        """
        arguments = {
            "VariableName": VariableName,
        }

        self._proxy_call_action("Remove", arguments=arguments)

        return

    def action_RemoveAccount(self, AccountType, AccountID, extract_returns=True):
        """
            Calls the RemoveAccount action.

            :returns: "result"
        """
        arguments = {
            "AccountType": AccountType,
            "AccountID": AccountID,
        }

        out_params = self._proxy_call_action("RemoveAccount", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ReplaceAccountX(self, AccountUDN, NewAccountID, NewAccountPassword, AccountToken, AccountKey, OAuthDeviceID, extract_returns=True):
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

        out_params = self._proxy_call_action("ReplaceAccountX", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAccountUDN",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetThirdPartyCredentials(self, extract_returns=True):
        """
            Calls the ResetThirdPartyCredentials action.

            :returns: "result"
        """
        arguments = { }

        out_params = self._proxy_call_action("ResetThirdPartyCredentials", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetAccountNicknameX(self, AccountUDN, AccountNickname, extract_returns=True):
        """
            Calls the SetAccountNicknameX action.

            :returns: "result"
        """
        arguments = {
            "AccountUDN": AccountUDN,
            "AccountNickname": AccountNickname,
        }

        out_params = self._proxy_call_action("SetAccountNicknameX", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetString(self, VariableName, StringValue):
        """
            Calls the SetString action.

            :returns: "result"
        """
        arguments = {
            "VariableName": VariableName,
            "StringValue": StringValue,
        }

        self._proxy_call_action("SetString", arguments=arguments)

        return
