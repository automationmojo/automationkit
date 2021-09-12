"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class MediaManagement2ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'MediaManagement2' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:MediaManagement:2'

    SERVICE_EVENT_VARIABLES = {
        "MediaSessionInfo": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_GetMediaCapabilities(self, TSMediaCapabilityInfo, extract_returns=True):
        """
            Calls the GetMediaCapabilities action.

            :returns: "SupportedMediaCapabilityInfo"
        """
        arguments = {
            "TSMediaCapabilityInfo": TSMediaCapabilityInfo,
        }

        out_params = self._proxy_call_action("GetMediaCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedMediaCapabilityInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMediaSessionInfo(self, TargetMediaSessionID, extract_returns=True):
        """
            Calls the GetMediaSessionInfo action.

            :returns: "MediaSessionInfoList"
        """
        arguments = {
            "TargetMediaSessionID": TargetMediaSessionID,
        }

        out_params = self._proxy_call_action("GetMediaSessionInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MediaSessionInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ModifyMediaSession(self, TargetMediaSessionID, NewMediaCapabilityInfo, extract_returns=True):
        """
            Calls the ModifyMediaSession action.

            :returns: "TCMediaCapabilityInfo"
        """
        arguments = {
            "TargetMediaSessionID": TargetMediaSessionID,
            "NewMediaCapabilityInfo": NewMediaCapabilityInfo,
        }

        out_params = self._proxy_call_action("ModifyMediaSession", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TCMediaCapabilityInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StartMediaSession(self, TSMediaCapabilityInfo, extract_returns=True):
        """
            Calls the StartMediaSession action.

            :returns: "MediaSessionID", "TCMediaCapabilityInfo"
        """
        arguments = {
            "TSMediaCapabilityInfo": TSMediaCapabilityInfo,
        }

        out_params = self._proxy_call_action("StartMediaSession", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MediaSessionID", "TCMediaCapabilityInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StopMediaSession(self, TargetMediaSessionID):
        """
            Calls the StopMediaSession action.
        """
        arguments = {
            "TargetMediaSessionID": TargetMediaSessionID,
        }

        self._proxy_call_action("StopMediaSession", arguments=arguments)

        return
