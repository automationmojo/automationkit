"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANCableLinkConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANCableLinkConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANCableLinkConfig:1'

    SERVICE_DEFAULT_VARIABLES = {
        "BPIEncryptionEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "CableLinkConfigState": { "data_type": "string", "default": None, "allowed_list": "['notReady', 'dsSyncComplete', 'usParamAcquired', 'rangingComplete', 'ipComplete', 'todEstablished', 'paramTransferComplete', 'registrationComplete', 'operational', 'accessDenied']"},
        "ConfigFile": { "data_type": "string", "default": None, "allowed_list": None},
        "DownstreamFrequency": { "data_type": "ui4", "default": None, "allowed_list": None},
        "DownstreamModulation": { "data_type": "string", "default": None, "allowed_list": "['64QAM', '256QAM']"},
        "LinkType": { "data_type": "string", "default": None, "allowed_list": "['Ethernet']"},
        "TFTPServer": { "data_type": "string", "default": None, "allowed_list": None},
        "UpstreamChannelID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "UpstreamFrequency": { "data_type": "ui4", "default": None, "allowed_list": None},
        "UpstreamModulation": { "data_type": "string", "default": None, "allowed_list": "['QPSK', '16QAM']"},
        "UpstreamPowerLevel": { "data_type": "ui4", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetBPIEncryptionEnabled(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBPIEncryptionEnabled action.

            :returns: "NewBPIEncryptionEnabled"
        """
        arguments = { }

        out_params = self.call_action("GetBPIEncryptionEnabled", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewBPIEncryptionEnabled",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCableLinkConfigInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCableLinkConfigInfo action.

            :returns: "NewCableLinkConfigState", "NewLinkType"
        """
        arguments = { }

        out_params = self.call_action("GetCableLinkConfigInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewCableLinkConfigState", "NewLinkType",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetConfigFile(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetConfigFile action.

            :returns: "NewConfigFile"
        """
        arguments = { }

        out_params = self.call_action("GetConfigFile", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewConfigFile",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDownstreamFrequency(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDownstreamFrequency action.

            :returns: "NewDownstreamFrequency"
        """
        arguments = { }

        out_params = self.call_action("GetDownstreamFrequency", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDownstreamFrequency",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDownstreamModulation(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDownstreamModulation action.

            :returns: "NewDownstreamModulation"
        """
        arguments = { }

        out_params = self.call_action("GetDownstreamModulation", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDownstreamModulation",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTFTPServer(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTFTPServer action.

            :returns: "NewTFTPServer"
        """
        arguments = { }

        out_params = self.call_action("GetTFTPServer", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTFTPServer",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUpstreamChannelID(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUpstreamChannelID action.

            :returns: "NewUpstreamChannelID"
        """
        arguments = { }

        out_params = self.call_action("GetUpstreamChannelID", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamChannelID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUpstreamFrequency(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUpstreamFrequency action.

            :returns: "NewUpstreamFrequency"
        """
        arguments = { }

        out_params = self.call_action("GetUpstreamFrequency", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamFrequency",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUpstreamModulation(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUpstreamModulation action.

            :returns: "NewUpstreamModulation"
        """
        arguments = { }

        out_params = self.call_action("GetUpstreamModulation", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamModulation",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUpstreamPowerLevel(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUpstreamPowerLevel action.

            :returns: "NewUpstreamPowerLevel"
        """
        arguments = { }

        out_params = self.call_action("GetUpstreamPowerLevel", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamPowerLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
