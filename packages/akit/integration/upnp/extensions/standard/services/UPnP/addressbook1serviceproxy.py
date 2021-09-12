"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class AddressBook1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'AddressBook1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:AddressBook:1'

    SERVICE_EVENT_VARIABLES = {
        "IncomingRequest": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_Accept(self, RequestID):
        """
            Calls the Accept action.
        """
        arguments = {
            "RequestID": RequestID,
        }

        self._proxy_call_action("Accept", arguments=arguments)

        return

    def action_FetchcontactInfo(self, Targetcontacts, ShareInfo):
        """
            Calls the FetchcontactInfo action.
        """
        arguments = {
            "Targetcontacts": Targetcontacts,
            "ShareInfo": ShareInfo,
        }

        self._proxy_call_action("FetchcontactInfo", arguments=arguments)

        return

    def action_ImportContacts(self, NetworkAddressBookID):
        """
            Calls the ImportContacts action.
        """
        arguments = {
            "NetworkAddressBookID": NetworkAddressBookID,
        }

        self._proxy_call_action("ImportContacts", arguments=arguments)

        return

    def action_Reject(self, RequestID):
        """
            Calls the Reject action.
        """
        arguments = {
            "RequestID": RequestID,
        }

        self._proxy_call_action("Reject", arguments=arguments)

        return

    def action_RetrieveIncomingRequests(self, extract_returns=True):
        """
            Calls the RetrieveIncomingRequests action.

            :returns: "ActiveIncomingRequests"
        """
        arguments = { }

        out_params = self._proxy_call_action("RetrieveIncomingRequests", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ActiveIncomingRequests",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ShareContacts(self, SharedContacts, SharedInfo, TargetContacts):
        """
            Calls the ShareContacts action.
        """
        arguments = {
            "SharedContacts": SharedContacts,
            "SharedInfo": SharedInfo,
            "TargetContacts": TargetContacts,
        }

        self._proxy_call_action("ShareContacts", arguments=arguments)

        return

    def action_SharePCC(self, TargetContacts, ShareInfo):
        """
            Calls the SharePCC action.
        """
        arguments = {
            "TargetContacts": TargetContacts,
            "ShareInfo": ShareInfo,
        }

        self._proxy_call_action("SharePCC", arguments=arguments)

        return
