"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANEthernetLinkConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANEthernetLinkConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANEthernetLinkConfig:1'

    SERVICE_DEFAULT_VARIABLES = {
        "EthernetLinkStatus": { "data_type": "string", "default": None, "allowed_list": "['Up', 'Down']"},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetEthernetLinkStatus(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetEthernetLinkStatus action.

            :returns: "NewEthernetLinkStatus"
        """
        arguments = { }

        out_params = self.call_action("GetEthernetLinkStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewEthernetLinkStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
