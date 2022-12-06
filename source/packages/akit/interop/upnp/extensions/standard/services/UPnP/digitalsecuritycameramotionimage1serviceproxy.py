"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class DigitalSecurityCameraMotionImage1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'DigitalSecurityCameraMotionImage1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:DigitalSecurityCameraMotionImage:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AvailableCompressionLevels": { "data_type": "string", "default": None, "allowed_list": None},
        "AvailableEncodings": { "data_type": "string", "default": None, "allowed_list": None},
        "AvailableResolutions": { "data_type": "string", "default": None, "allowed_list": None},
        "VideoPresentationURL": { "data_type": "string", "default": None, "allowed_list": None},
        "VideoURL": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "DefaultCompressionLevel": { "data_type": "string", "default": None, "allowed_list": None},
        "DefaultEncoding": { "data_type": "string", "default": None, "allowed_list": None},
        "DefaultResolution": { "data_type": "string", "default": None, "allowed_list": None},
        "MaxBandwidth": { "data_type": "ui4", "default": "100", "allowed_list": None},
        "TargetFrameRate": { "data_type": "ui4", "default": "1500", "allowed_list": None},
    }

    def action_GetAvailableCompressionLevels(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAvailableCompressionLevels action.

            :returns: "RetAvailableCompressionLevels"
        """
        arguments = { }

        out_params = self.call_action("GetAvailableCompressionLevels", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetAvailableCompressionLevels",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAvailableEncodings(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAvailableEncodings action.

            :returns: "RetAvailableEncodings"
        """
        arguments = { }

        out_params = self.call_action("GetAvailableEncodings", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetAvailableEncodings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAvailableResolutions(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAvailableResolutions action.

            :returns: "RetAvailableResolutions"
        """
        arguments = { }

        out_params = self.call_action("GetAvailableResolutions", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetAvailableResolutions",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultCompressionLevel(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDefaultCompressionLevel action.

            :returns: "RetCompressionLevel"
        """
        arguments = { }

        out_params = self.call_action("GetDefaultCompressionLevel", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetCompressionLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultEncoding(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDefaultEncoding action.

            :returns: "RetEncoding"
        """
        arguments = { }

        out_params = self.call_action("GetDefaultEncoding", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetEncoding",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultResolution(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDefaultResolution action.

            :returns: "RetResolution"
        """
        arguments = { }

        out_params = self.call_action("GetDefaultResolution", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetResolution",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultVideoPresentationURL(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDefaultVideoPresentationURL action.

            :returns: "RetVideoPresentationURL"
        """
        arguments = { }

        out_params = self.call_action("GetDefaultVideoPresentationURL", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetVideoPresentationURL",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultVideoURL(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDefaultVideoURL action.

            :returns: "RetVideoURL"
        """
        arguments = { }

        out_params = self.call_action("GetDefaultVideoURL", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetVideoURL",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMaxBandwidth(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMaxBandwidth action.

            :returns: "RetMaxBandwidth"
        """
        arguments = { }

        out_params = self.call_action("GetMaxBandwidth", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetMaxBandwidth",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTargetFrameRate(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTargetFrameRate action.

            :returns: "RetTargetFrameRate"
        """
        arguments = { }

        out_params = self.call_action("GetTargetFrameRate", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetTargetFrameRate",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVideoPresentationURL(self, ReqEncoding, ReqCompression, ReqResolution, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetVideoPresentationURL action.

            :returns: "RetVideoPresentationURL"
        """
        arguments = {
            "ReqEncoding": ReqEncoding,
            "ReqCompression": ReqCompression,
            "ReqResolution": ReqResolution,
        }

        out_params = self.call_action("GetVideoPresentationURL", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetVideoPresentationURL",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVideoURL(self, ReqEncoding, ReqCompression, ReqResolution, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetVideoURL action.

            :returns: "RetVideoURL"
        """
        arguments = {
            "ReqEncoding": ReqEncoding,
            "ReqCompression": ReqCompression,
            "ReqResolution": ReqResolution,
        }

        out_params = self.call_action("GetVideoURL", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetVideoURL",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetDefaultCompressionLevel(self, ReqCompressionLevel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDefaultCompressionLevel action.
        """
        arguments = {
            "ReqCompressionLevel": ReqCompressionLevel,
        }

        self.call_action("SetDefaultCompressionLevel", arguments=arguments, aspects=aspects)

        return

    def action_SetDefaultEncoding(self, ReqEncoding, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDefaultEncoding action.
        """
        arguments = {
            "ReqEncoding": ReqEncoding,
        }

        self.call_action("SetDefaultEncoding", arguments=arguments, aspects=aspects)

        return

    def action_SetDefaultResolution(self, ReqResolution, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDefaultResolution action.
        """
        arguments = {
            "ReqResolution": ReqResolution,
        }

        self.call_action("SetDefaultResolution", arguments=arguments, aspects=aspects)

        return

    def action_SetMaxBandwidth(self, ReqMaxBandwidth, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetMaxBandwidth action.
        """
        arguments = {
            "ReqMaxBandwidth": ReqMaxBandwidth,
        }

        self.call_action("SetMaxBandwidth", arguments=arguments, aspects=aspects)

        return

    def action_SetTargetFrameRate(self, ReqTargetFrameRate, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetTargetFrameRate action.
        """
        arguments = {
            "ReqTargetFrameRate": ReqTargetFrameRate,
        }

        self.call_action("SetTargetFrameRate", arguments=arguments, aspects=aspects)

        return
