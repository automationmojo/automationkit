"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class MediaManagement1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'MediaManagement1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:MediaManagement:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "MediaSessionInfo": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_GetMediaCapabilities(self, TSMediaCapabilityInfo, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMediaCapabilities action.

            :returns: "SupportedMediaCapabilityInfo"
        """
        arguments = {
            "TSMediaCapabilityInfo": TSMediaCapabilityInfo,
        }

        out_params = self.call_action("GetMediaCapabilities", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedMediaCapabilityInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMediaSessionInfo(self, TargetMediaSessionID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMediaSessionInfo action.

            :returns: "MediaSessionInfoList"
        """
        arguments = {
            "TargetMediaSessionID": TargetMediaSessionID,
        }

        out_params = self.call_action("GetMediaSessionInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MediaSessionInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ModifyMediaSession(self, TargetMediaSessionID, NewMediaCapabilityInfo, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ModifyMediaSession action.

            :returns: "TCMediaCapabilityInfo"
        """
        arguments = {
            "TargetMediaSessionID": TargetMediaSessionID,
            "NewMediaCapabilityInfo": NewMediaCapabilityInfo,
        }

        out_params = self.call_action("ModifyMediaSession", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TCMediaCapabilityInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StartMediaSession(self, TSMediaCapabilityInfo, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartMediaSession action.

            :returns: "MediaSessionID", "TCMediaCapabilityInfo"
        """
        arguments = {
            "TSMediaCapabilityInfo": TSMediaCapabilityInfo,
        }

        out_params = self.call_action("StartMediaSession", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MediaSessionID", "TCMediaCapabilityInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StopMediaSession(self, TargetMediaSessionID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StopMediaSession action.
        """
        arguments = {
            "TargetMediaSessionID": TargetMediaSessionID,
        }

        self.call_action("StopMediaSession", arguments=arguments, aspects=aspects)

        return
