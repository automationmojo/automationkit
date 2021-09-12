"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANCableLinkConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANCableLinkConfig1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANCableLinkConfig:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_GetBPIEncryptionEnabled(self, extract_returns=True):
        """
            Calls the GetBPIEncryptionEnabled action.

            :returns: "NewBPIEncryptionEnabled"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetBPIEncryptionEnabled", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewBPIEncryptionEnabled",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCableLinkConfigInfo(self, extract_returns=True):
        """
            Calls the GetCableLinkConfigInfo action.

            :returns: "NewCableLinkConfigState", "NewLinkType"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetCableLinkConfigInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewCableLinkConfigState", "NewLinkType",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetConfigFile(self, extract_returns=True):
        """
            Calls the GetConfigFile action.

            :returns: "NewConfigFile"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetConfigFile", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewConfigFile",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDownstreamFrequency(self, extract_returns=True):
        """
            Calls the GetDownstreamFrequency action.

            :returns: "NewDownstreamFrequency"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetDownstreamFrequency", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDownstreamFrequency",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDownstreamModulation(self, extract_returns=True):
        """
            Calls the GetDownstreamModulation action.

            :returns: "NewDownstreamModulation"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetDownstreamModulation", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDownstreamModulation",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTFTPServer(self, extract_returns=True):
        """
            Calls the GetTFTPServer action.

            :returns: "NewTFTPServer"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetTFTPServer", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTFTPServer",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUpstreamChannelID(self, extract_returns=True):
        """
            Calls the GetUpstreamChannelID action.

            :returns: "NewUpstreamChannelID"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetUpstreamChannelID", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamChannelID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUpstreamFrequency(self, extract_returns=True):
        """
            Calls the GetUpstreamFrequency action.

            :returns: "NewUpstreamFrequency"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetUpstreamFrequency", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamFrequency",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUpstreamModulation(self, extract_returns=True):
        """
            Calls the GetUpstreamModulation action.

            :returns: "NewUpstreamModulation"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetUpstreamModulation", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamModulation",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUpstreamPowerLevel(self, extract_returns=True):
        """
            Calls the GetUpstreamPowerLevel action.

            :returns: "NewUpstreamPowerLevel"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetUpstreamPowerLevel", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpstreamPowerLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
