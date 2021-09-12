"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class LinkAuthentication1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'LinkAuthentication1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:LinkAuthentication:1'

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
        "LastError": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddEntry(self, NewIdentifier, NewSecret, NewSecretType, NewAuthType, NewAuthState, NewCredentialState, NewDescription, NewMACAddress, NewCredentialDuration, NewLinkedIdentifier, extract_returns=True):
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

        out_params = self._proxy_call_action("AddEntry", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfEntries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteEntry(self, NewIdentifier, extract_returns=True):
        """
            Calls the DeleteEntry action.

            :returns: "NewNumberOfEntries"
        """
        arguments = {
            "NewIdentifier": NewIdentifier,
        }

        out_params = self._proxy_call_action("DeleteEntry", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfEntries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_FactoryDefaultReset(self):
        """
            Calls the FactoryDefaultReset action.
        """
        arguments = { }


        self._proxy_call_action("FactoryDefaultReset", arguments=arguments)

        return

    def action_GetGenericEntry(self, NewIndex, extract_returns=True):
        """
            Calls the GetGenericEntry action.

            :returns: "NewIdentifier", "NewSecret", "NewSecretType", "NewAuthType", "NewAuthState", "NewCredentialState", "NewDescription", "NewMACAddress", "NewCredentialDuration", "NewLinkedIdentifier"
        """
        arguments = {
            "NewIndex": NewIndex,
        }

        out_params = self._proxy_call_action("GetGenericEntry", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewIdentifier", "NewSecret", "NewSecretType", "NewAuthType", "NewAuthState", "NewCredentialState", "NewDescription", "NewMACAddress", "NewCredentialDuration", "NewLinkedIdentifier",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetNumberOfEntries(self, extract_returns=True):
        """
            Calls the GetNumberOfEntries action.

            :returns: "NewNumberOfEntries"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetNumberOfEntries", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfEntries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSpecificEntry(self, NewIdentifierKey, extract_returns=True):
        """
            Calls the GetSpecificEntry action.

            :returns: "NewIdentifier", "NewSecret", "NewSecretType", "NewAuthType", "NewAuthState", "NewCredentialState", "NewDescription", "NewMACAddress", "NewCredentialDuration", "NewLinkedIdentifier"
        """
        arguments = {
            "NewIdentifierKey": NewIdentifierKey,
        }

        out_params = self._proxy_call_action("GetSpecificEntry", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewIdentifier", "NewSecret", "NewSecretType", "NewAuthType", "NewAuthState", "NewCredentialState", "NewDescription", "NewMACAddress", "NewCredentialDuration", "NewLinkedIdentifier",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetAuthentication(self):
        """
            Calls the ResetAuthentication action.
        """
        arguments = { }


        self._proxy_call_action("ResetAuthentication", arguments=arguments)

        return

    def action_UpdateEntry(self, NewIdentifier, NewSecret, NewSecretType, NewAuthType, NewAuthState, NewCredentialState, NewDescription, NewMACAddress, NewCredentialDuration, NewLinkedIdentifier, extract_returns=True):
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

        out_params = self._proxy_call_action("UpdateEntry", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfEntries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
