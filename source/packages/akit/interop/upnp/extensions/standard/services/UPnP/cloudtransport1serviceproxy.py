"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class CloudTransport1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'CloudTransport1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:CloudTransport:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {}

    def action_ConnectMethod(self, Host, MethodLine, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ConnectMethod action.

            :returns: "Identifier", "ConnectWriteCout"
        """
        arguments = {
            "Host": Host,
            "MethodLine": MethodLine,
        }

        out_params = self.call_action("ConnectMethod", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Identifier", "ConnectWriteCout",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_HTTPReadBody(self, Identifier, Size, CRLFFlag, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the HTTPReadBody action.

            :returns: "Body", "ReadLength", "ConnectReadCount"
        """
        arguments = {
            "Identifier": Identifier,
            "Size": Size,
            "CRLFFlag": CRLFFlag,
        }

        out_params = self.call_action("HTTPReadBody", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Body", "ReadLength", "ConnectReadCount",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_HTTPReadHeaders(self, Identifier, CRLFFlag, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the HTTPReadHeaders action.

            :returns: "Headers", "ReadLength", "ConnectReadCount"
        """
        arguments = {
            "Identifier": Identifier,
            "CRLFFlag": CRLFFlag,
        }

        out_params = self.call_action("HTTPReadHeaders", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Headers", "ReadLength", "ConnectReadCount",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_HTTPWriteBody(self, Identifier, Body, Size, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the HTTPWriteBody action.

            :returns: "ConnectWriteCount"
        """
        arguments = {
            "Identifier": Identifier,
            "Body": Body,
            "Size": Size,
        }

        out_params = self.call_action("HTTPWriteBody", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectWriteCount",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_HTTPWriteHeaders(self, Identifier, Headers, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the HTTPWriteHeaders action.

            :returns: "ConnectWriteCount"
        """
        arguments = {
            "Identifier": Identifier,
            "Headers": Headers,
        }

        out_params = self.call_action("HTTPWriteHeaders", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectWriteCount",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
