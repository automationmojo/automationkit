"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Feeder1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Feeder1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Feeder:1'

    SERVICE_EVENT_VARIABLES = {
        "MorePages": { "data_type": "boolean", "default": "0", "allowed_list": None},
    }

    def action_Eject(self, JobIDIn, EntireDocumentIn, extract_returns=True):
        """
            Calls the Eject action.

            :returns: "StateOut"
        """
        arguments = {
            "JobIDIn": JobIDIn,
            "EntireDocumentIn": EntireDocumentIn,
        }

        out_params = self._proxy_call_action("Eject", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFeederMode(self, extract_returns=True):
        """
            Calls the GetFeederMode action.

            :returns: "FeederModeOut"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetFeederMode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FeederModeOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetState(self, extract_returns=True):
        """
            Calls the GetState action.

            :returns: "StateOut", "MorePagesOut", "FailureCodeOut"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetState", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut", "MorePagesOut", "FailureCodeOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Load(self, JobIDIn, extract_returns=True):
        """
            Calls the Load action.

            :returns: "StateOut"
        """
        arguments = {
            "JobIDIn": JobIDIn,
        }

        out_params = self._proxy_call_action("Load", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Reset(self, JobIDIn, extract_returns=True):
        """
            Calls the Reset action.

            :returns: "StateOut"
        """
        arguments = {
            "JobIDIn": JobIDIn,
        }

        out_params = self._proxy_call_action("Reset", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetFeederMode(self, JobIDIn, FeederModeIn):
        """
            Calls the SetFeederMode action.
        """
        arguments = {
            "JobIDIn": JobIDIn,
            "FeederModeIn": FeederModeIn,
        }

        self._proxy_call_action("SetFeederMode", arguments=arguments)

        return
