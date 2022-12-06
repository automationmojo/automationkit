"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANDSLLinkConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANDSLLinkConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANDSLLinkConfig:1'

    SERVICE_DEFAULT_VARIABLES = {
        "ATMEncapsulation": { "data_type": "string", "default": None, "allowed_list": None},
        "AutoConfig": { "data_type": "boolean", "default": None, "allowed_list": None},
        "DestinationAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "FCSPreserved": { "data_type": "boolean", "default": None, "allowed_list": None},
        "LinkStatus": { "data_type": "string", "default": None, "allowed_list": "['Up', 'Down']"},
        "LinkType": { "data_type": "string", "default": None, "allowed_list": None},
        "ModulationType": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetATMEncapsulation(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetATMEncapsulation action.

            :returns: "NewATMEncapsulation"
        """
        arguments = { }

        out_params = self.call_action("GetATMEncapsulation", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewATMEncapsulation",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAutoConfig(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAutoConfig action.

            :returns: "NewAutoConfig"
        """
        arguments = { }

        out_params = self.call_action("GetAutoConfig", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAutoConfig",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDSLLinkInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDSLLinkInfo action.

            :returns: "NewLinkType", "NewLinkStatus"
        """
        arguments = { }

        out_params = self.call_action("GetDSLLinkInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewLinkType", "NewLinkStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDestinationAddress(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDestinationAddress action.

            :returns: "NewDestinationAddress"
        """
        arguments = { }

        out_params = self.call_action("GetDestinationAddress", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDestinationAddress",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFCSPreserved(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFCSPreserved action.

            :returns: "NewFCSPreserved"
        """
        arguments = { }

        out_params = self.call_action("GetFCSPreserved", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewFCSPreserved",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetModulationType(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetModulationType action.

            :returns: "NewModulationType"
        """
        arguments = { }

        out_params = self.call_action("GetModulationType", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewModulationType",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetATMEncapsulation(self, NewATMEncapsulation, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetATMEncapsulation action.
        """
        arguments = {
            "NewATMEncapsulation": NewATMEncapsulation,
        }

        self.call_action("SetATMEncapsulation", arguments=arguments, aspects=aspects)

        return

    def action_SetDSLLinkType(self, NewLinkType, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDSLLinkType action.
        """
        arguments = {
            "NewLinkType": NewLinkType,
        }

        self.call_action("SetDSLLinkType", arguments=arguments, aspects=aspects)

        return

    def action_SetDestinationAddress(self, NewDestinationAddress, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDestinationAddress action.
        """
        arguments = {
            "NewDestinationAddress": NewDestinationAddress,
        }

        self.call_action("SetDestinationAddress", arguments=arguments, aspects=aspects)

        return

    def action_SetFCSPreserved(self, NewFCSPreserved, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetFCSPreserved action.
        """
        arguments = {
            "NewFCSPreserved": NewFCSPreserved,
        }

        self.call_action("SetFCSPreserved", arguments=arguments, aspects=aspects)

        return
