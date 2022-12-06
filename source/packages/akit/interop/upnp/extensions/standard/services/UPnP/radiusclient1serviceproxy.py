"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RadiusClient1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RadiusClient1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RadiusClient:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AuthenticationServerIPAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "AuthenticationServerPortNumber": { "data_type": "ui2", "default": None, "allowed_list": None},
        "AuthenticationServerSharedSecret": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "NumberOfAuthenticationServerEntries": { "data_type": "ui2", "default": None, "allowed_list": None},
    }

    def action_AddAuthenticationServerEntry(self, NewAuthenticationServerIPAddress, NewAuthenticationServerPortNumber, NewAuthenticationServerSharedSecret, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddAuthenticationServerEntry action.
        """
        arguments = {
            "NewAuthenticationServerIPAddress": NewAuthenticationServerIPAddress,
            "NewAuthenticationServerPortNumber": NewAuthenticationServerPortNumber,
            "NewAuthenticationServerSharedSecret": NewAuthenticationServerSharedSecret,
        }

        self.call_action("AddAuthenticationServerEntry", arguments=arguments, aspects=aspects)

        return

    def action_DeleteAuthenticationServerEntry(self, NewAuthenticationServerIPAddress, NewAuthenticationServerPortNumber, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteAuthenticationServerEntry action.
        """
        arguments = {
            "NewAuthenticationServerIPAddress": NewAuthenticationServerIPAddress,
            "NewAuthenticationServerPortNumber": NewAuthenticationServerPortNumber,
        }

        self.call_action("DeleteAuthenticationServerEntry", arguments=arguments, aspects=aspects)

        return

    def action_FactoryDefaultReset(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the FactoryDefaultReset action.
        """
        arguments = { }

        self.call_action("FactoryDefaultReset", arguments=arguments, aspects=aspects)

        return

    def action_GetGenericAuthenticationServerEntry(self, NewAuthenticationServerIndex, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetGenericAuthenticationServerEntry action.

            :returns: "NewAuthenticationServerIPAddress", "NewAuthenticationServerPortNumber", "NewAuthenticationServerSharedSecret"
        """
        arguments = {
            "NewAuthenticationServerIndex": NewAuthenticationServerIndex,
        }

        out_params = self.call_action("GetGenericAuthenticationServerEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAuthenticationServerIPAddress", "NewAuthenticationServerPortNumber", "NewAuthenticationServerSharedSecret",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSpecificAuthenticationServerEntry(self, NewAuthenticationServerIPAddress, NewAuthenticationServerPortNumber, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSpecificAuthenticationServerEntry action.

            :returns: "NewAuthenticationServerSharedSecret"
        """
        arguments = {
            "NewAuthenticationServerIPAddress": NewAuthenticationServerIPAddress,
            "NewAuthenticationServerPortNumber": NewAuthenticationServerPortNumber,
        }

        out_params = self.call_action("GetSpecificAuthenticationServerEntry", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAuthenticationServerSharedSecret",)]
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
