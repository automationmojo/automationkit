"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RATAConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RATAConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RATAConfig:1'

    SERVICE_EVENT_VARIABLES = {
        "CredentialsList": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddProfile(self, NewProfileConfigInfo):
        """
            Calls the AddProfile action.
        """
        arguments = {
            "NewProfileConfigInfo": NewProfileConfigInfo,
        }

        self._proxy_call_action("AddProfile", arguments=arguments)

        return

    def action_DeleteProfile(self, ProfileID):
        """
            Calls the DeleteProfile action.
        """
        arguments = {
            "ProfileID": ProfileID,
        }

        self._proxy_call_action("DeleteProfile", arguments=arguments)

        return

    def action_EditProfile(self, ProfileID, UpdatedProfileConfigInfo):
        """
            Calls the EditProfile action.
        """
        arguments = {
            "ProfileID": ProfileID,
            "UpdatedProfileConfigInfo": UpdatedProfileConfigInfo,
        }

        self._proxy_call_action("EditProfile", arguments=arguments)

        return

    def action_GetCredentialsList(self, extract_returns=True):
        """
            Calls the GetCredentialsList action.

            :returns: "CurrentCredentialsList"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetCredentialsList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentCredentialsList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetProfileConfigInfo(self, ProfileID, extract_returns=True):
        """
            Calls the GetProfileConfigInfo action.

            :returns: "ProfileConfigInfo"
        """
        arguments = {
            "ProfileID": ProfileID,
        }

        out_params = self._proxy_call_action("GetProfileConfigInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ProfileConfigInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetProfileList(self, extract_returns=True):
        """
            Calls the GetProfileList action.

            :returns: "ProfileList"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetProfileList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ProfileList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSupportedCredentialDelivery(self, extract_returns=True):
        """
            Calls the GetSupportedCredentialDelivery action.

            :returns: "SupportedCredentialDelivery"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetSupportedCredentialDelivery", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedCredentialDelivery",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTransportAgentCapabilities(self, extract_returns=True):
        """
            Calls the GetTransportAgentCapabilities action.

            :returns: "TransportAgentCapabilities"
        """
        arguments = { }


        out_params = self._proxy_call_action("GetTransportAgentCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransportAgentCapabilities",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
