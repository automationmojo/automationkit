"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class LinkAuthentication1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'LinkAuthentication1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:LinkAuthentication:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AuthState": { "data_type": "string", "default": "Unconfigured", "allowed_list": "['Unconfigured', 'Failed', 'Succeeded']"},
        "AuthType": { "data_type": "string", "default": None, "allowed_list": "['SharedSecret', 'ValidateCredentials']"},
        "CredentialDuration": { "data_type": "ui4", "default": "0", "allowed_list": None},
        "CredentialState": { "data_type": "string", "default": "Unconfigured", "allowed_list": "['Unconfigured', 'Pending', 'Accepted', 'Denied']"},
        "Description": { "data_type": "string", "default": None, "allowed_list": None},
        "Identifier": { "data_type": "string", "default": None, "allowed_list": None},
        "LinkedIdentifier": { "data_type": "string", "default": None, "allowed_list": None},
        "MACAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "NumberOfEntries": { "data_type": "ui2", "default": "0", "allowed_list": None},
        "Secret": { "data_type": "string", "default": None, "allowed_list": None},
        "SecretType": { "data_type": "string", "default": None, "allowed_list": "['TextPassword', 'X509Certificate', 'PublicKey', 'PublicKeyHash160']"},
    }

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
        "LastError": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddEntry(self, NewIdentifier, NewSecret, NewSecretType, NewAuthType, NewAuthState, NewCredentialState, NewDescription, NewMACAddress, NewCredentialDuration, NewLinkedIdentifier, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddEntry action.

            :returns: "NewNumberOfEntries"
        """
        arguments = {
            "NewIdentifier": NewIdentifier,
            "NewSecret": NewSecret,
            "NewSecretType": NewSecretType,
            "NewAuthType": NewAuthType,
            "NewAuthState": NewAuthState,
            "NewCredentialState": NewCredentialState,
            "NewDescription": NewDescription,
            "NewMACAddress": NewMACAddress,
            "NewCredentialDuration": NewCredentialDuration,
            "NewLinkedIdentifier": NewLinkedIdentifier,
        }

        out_params = self.call_action("AddEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfEntries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteEntry(self, NewIdentifier, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteEntry action.

            :returns: "NewNumberOfEntries"
        """
        arguments = {
            "NewIdentifier": NewIdentifier,
        }

        out_params = self.call_action("DeleteEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfEntries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_FactoryDefaultReset(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the FactoryDefaultReset action.
        """
        arguments = { }

        self.call_action("FactoryDefaultReset", arguments=arguments, aspects=aspects)

        return

    def action_GetGenericEntry(self, NewIndex, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetGenericEntry action.

            :returns: "NewIdentifier", "NewSecret", "NewSecretType", "NewAuthType", "NewAuthState", "NewCredentialState", "NewDescription", "NewMACAddress", "NewCredentialDuration", "NewLinkedIdentifier"
        """
        arguments = {
            "NewIndex": NewIndex,
        }

        out_params = self.call_action("GetGenericEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewIdentifier", "NewSecret", "NewSecretType", "NewAuthType", "NewAuthState", "NewCredentialState", "NewDescription", "NewMACAddress", "NewCredentialDuration", "NewLinkedIdentifier",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetNumberOfEntries(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetNumberOfEntries action.

            :returns: "NewNumberOfEntries"
        """
        arguments = { }

        out_params = self.call_action("GetNumberOfEntries", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfEntries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSpecificEntry(self, NewIdentifierKey, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSpecificEntry action.

            :returns: "NewIdentifier", "NewSecret", "NewSecretType", "NewAuthType", "NewAuthState", "NewCredentialState", "NewDescription", "NewMACAddress", "NewCredentialDuration", "NewLinkedIdentifier"
        """
        arguments = {
            "NewIdentifierKey": NewIdentifierKey,
        }

        out_params = self.call_action("GetSpecificEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewIdentifier", "NewSecret", "NewSecretType", "NewAuthType", "NewAuthState", "NewCredentialState", "NewDescription", "NewMACAddress", "NewCredentialDuration", "NewLinkedIdentifier",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetAuthentication(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ResetAuthentication action.
        """
        arguments = { }

        self.call_action("ResetAuthentication", arguments=arguments, aspects=aspects)

        return

    def action_UpdateEntry(self, NewIdentifier, NewSecret, NewSecretType, NewAuthType, NewAuthState, NewCredentialState, NewDescription, NewMACAddress, NewCredentialDuration, NewLinkedIdentifier, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UpdateEntry action.

            :returns: "NewNumberOfEntries"
        """
        arguments = {
            "NewIdentifier": NewIdentifier,
            "NewSecret": NewSecret,
            "NewSecretType": NewSecretType,
            "NewAuthType": NewAuthType,
            "NewAuthState": NewAuthState,
            "NewCredentialState": NewCredentialState,
            "NewDescription": NewDescription,
            "NewMACAddress": NewMACAddress,
            "NewCredentialDuration": NewCredentialDuration,
            "NewLinkedIdentifier": NewLinkedIdentifier,
        }

        out_params = self.call_action("UpdateEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfEntries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
