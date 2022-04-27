"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class AddressBook1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'AddressBook1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:AddressBook:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "IncomingRequest": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_Accept(self, RequestID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Accept action.
        """
        arguments = {
            "RequestID": RequestID,
        }

        self.call_action("Accept", arguments=arguments, aspects=aspects)

        return

    def action_FetchcontactInfo(self, Targetcontacts, ShareInfo, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the FetchcontactInfo action.
        """
        arguments = {
            "Targetcontacts": Targetcontacts,
            "ShareInfo": ShareInfo,
        }

        self.call_action("FetchcontactInfo", arguments=arguments, aspects=aspects)

        return

    def action_ImportContacts(self, NetworkAddressBookID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ImportContacts action.
        """
        arguments = {
            "NetworkAddressBookID": NetworkAddressBookID,
        }

        self.call_action("ImportContacts", arguments=arguments, aspects=aspects)

        return

    def action_Reject(self, RequestID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Reject action.
        """
        arguments = {
            "RequestID": RequestID,
        }

        self.call_action("Reject", arguments=arguments, aspects=aspects)

        return

    def action_RetrieveIncomingRequests(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RetrieveIncomingRequests action.

            :returns: "ActiveIncomingRequests"
        """
        arguments = { }

        out_params = self.call_action("RetrieveIncomingRequests", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ActiveIncomingRequests",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ShareContacts(self, SharedContacts, SharedInfo, TargetContacts, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ShareContacts action.
        """
        arguments = {
            "SharedContacts": SharedContacts,
            "SharedInfo": SharedInfo,
            "TargetContacts": TargetContacts,
        }

        self.call_action("ShareContacts", arguments=arguments, aspects=aspects)

        return

    def action_SharePCC(self, TargetContacts, ShareInfo, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SharePCC action.
        """
        arguments = {
            "TargetContacts": TargetContacts,
            "ShareInfo": ShareInfo,
        }

        self.call_action("SharePCC", arguments=arguments, aspects=aspects)

        return
