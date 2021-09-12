"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANEthernetLinkConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANEthernetLinkConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANEthernetLinkConfig:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_GetEthernetLinkStatus(self, extract_returns=True):
        """
            Calls the GetEthernetLinkStatus action.

            :returns: "NewEthernetLinkStatus"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetEthernetLinkStatus", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewEthernetLinkStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
