"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Feeder1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Feeder1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Feeder:1'

    SERVICE_DEFAULT_VARIABLES = {
        "EntireDocument": { "data_type": "string", "default": "1", "allowed_list": "['1', '0', 'device-setting']"},
        "FailureCode": { "data_type": "string", "default": "None", "allowed_list": "['None', 'Jammed', 'Timeout']"},
        "FeederMode": { "data_type": "string", "default": "Simplex", "allowed_list": "['Simplex']"},
        "InputJustification": { "data_type": "string", "default": None, "allowed_list": None},
        "JobID": { "data_type": "ui4", "default": "0", "allowed_list": None},
        "Model": { "data_type": "string", "default": None, "allowed_list": None},
        "SheetHeight": { "data_type": "ui4", "default": None, "allowed_list": None},
        "SheetWidth": { "data_type": "ui4", "default": None, "allowed_list": None},
        "State": { "data_type": "string", "default": "Unloaded", "allowed_list": "['Unloaded', 'Loaded', 'Busy', 'Erred']"},
        "Timeout": { "data_type": "ui4", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "MorePages": { "data_type": "boolean", "default": "0", "allowed_list": None},
    }

    def action_Eject(self, JobIDIn, EntireDocumentIn, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Eject action.

            :returns: "StateOut"
        """
        arguments = {
            "JobIDIn": JobIDIn,
            "EntireDocumentIn": EntireDocumentIn,
        }

        out_params = self.call_action("Eject", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFeederMode(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFeederMode action.

            :returns: "FeederModeOut"
        """
        arguments = { }

        out_params = self.call_action("GetFeederMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FeederModeOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetState(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetState action.

            :returns: "StateOut", "MorePagesOut", "FailureCodeOut"
        """
        arguments = { }

        out_params = self.call_action("GetState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut", "MorePagesOut", "FailureCodeOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Load(self, JobIDIn, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Load action.

            :returns: "StateOut"
        """
        arguments = {
            "JobIDIn": JobIDIn,
        }

        out_params = self.call_action("Load", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Reset(self, JobIDIn, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Reset action.

            :returns: "StateOut"
        """
        arguments = {
            "JobIDIn": JobIDIn,
        }

        out_params = self.call_action("Reset", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetFeederMode(self, JobIDIn, FeederModeIn, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetFeederMode action.
        """
        arguments = {
            "JobIDIn": JobIDIn,
            "FeederModeIn": FeederModeIn,
        }

        self.call_action("SetFeederMode", arguments=arguments, aspects=aspects)

        return
