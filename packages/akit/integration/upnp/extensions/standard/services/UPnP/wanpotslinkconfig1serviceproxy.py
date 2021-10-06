"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import Aspects, DEFAULT_ASPECTS

from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANPOTSLinkConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANPOTSLinkConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANPOTSLinkConfig:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_GetCallRetryInfo(self, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetCallRetryInfo action.

            :returns: "NewNumberOfRetries", "NewDelayBetweenRetries"
        """
        arguments = { }

        out_params = self.call_action("GetCallRetryInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewNumberOfRetries", "NewDelayBetweenRetries",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDataCompression(self, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetDataCompression action.

            :returns: "NewDataCompression"
        """
        arguments = { }

        out_params = self.call_action("GetDataCompression", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDataCompression",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDataModulationSupported(self, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetDataModulationSupported action.

            :returns: "NewDataModulationSupported"
        """
        arguments = { }

        out_params = self.call_action("GetDataModulationSupported", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDataModulationSupported",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDataProtocol(self, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetDataProtocol action.

            :returns: "NewDataProtocol"
        """
        arguments = { }

        out_params = self.call_action("GetDataProtocol", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDataProtocol",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFclass(self, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetFclass action.

            :returns: "NewFclass"
        """
        arguments = { }

        out_params = self.call_action("GetFclass", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewFclass",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetISPInfo(self, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetISPInfo action.

            :returns: "NewISPPhoneNumber", "NewISPInfo", "NewLinkType"
        """
        arguments = { }

        out_params = self.call_action("GetISPInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewISPPhoneNumber", "NewISPInfo", "NewLinkType",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPlusVTRCommandSupported(self, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetPlusVTRCommandSupported action.

            :returns: "NewPlusVTRCommandSupported"
        """
        arguments = { }

        out_params = self.call_action("GetPlusVTRCommandSupported", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPlusVTRCommandSupported",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetCallRetryInfo(self, NewNumberOfRetries, NewDelayBetweenRetries, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the SetCallRetryInfo action.
        """
        arguments = {
            "NewNumberOfRetries": NewNumberOfRetries,
            "NewDelayBetweenRetries": NewDelayBetweenRetries,
        }

        self.call_action("SetCallRetryInfo", arguments=arguments, aspects=aspects)

        return

    def action_SetISPInfo(self, NewISPPhoneNumber, NewISPInfo, NewLinkType, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the SetISPInfo action.
        """
        arguments = {
            "NewISPPhoneNumber": NewISPPhoneNumber,
            "NewISPInfo": NewISPInfo,
            "NewLinkType": NewLinkType,
        }

        self.call_action("SetISPInfo", arguments=arguments, aspects=aspects)

        return
