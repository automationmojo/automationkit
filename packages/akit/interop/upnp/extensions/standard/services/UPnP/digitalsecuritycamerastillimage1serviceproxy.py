"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class DigitalSecurityCameraStillImage1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'DigitalSecurityCameraStillImage1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:DigitalSecurityCameraStillImage:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AvailableCompressionLevels": { "data_type": "string", "default": None, "allowed_list": None},
        "AvailableEncodings": { "data_type": "string", "default": None, "allowed_list": None},
        "AvailableResolutions": { "data_type": "string", "default": None, "allowed_list": None},
        "ImagePresentationURL": { "data_type": "string", "default": None, "allowed_list": None},
        "ImageURL": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "DefaultCompressionLevel": { "data_type": "string", "default": None, "allowed_list": None},
        "DefaultEncoding": { "data_type": "string", "default": None, "allowed_list": None},
        "DefaultResolution": { "data_type": "string", "default": None, "allowed_list": None},
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

    def action_GetDefaultImagePresentationURL(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDefaultImagePresentationURL action.

            :returns: "RetImagePresentationURL"
        """
        arguments = { }

        out_params = self.call_action("GetDefaultImagePresentationURL", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetImagePresentationURL",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultImageURL(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDefaultImageURL action.

            :returns: "RetImageURL"
        """
        arguments = { }

        out_params = self.call_action("GetDefaultImageURL", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetImageURL",)]
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

    def action_GetImagePresentationURL(self, ReqEncoding, ReqCompression, ReqResolution, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetImagePresentationURL action.

            :returns: "RetImagePresentationURL"
        """
        arguments = {
            "ReqEncoding": ReqEncoding,
            "ReqCompression": ReqCompression,
            "ReqResolution": ReqResolution,
        }

        out_params = self.call_action("GetImagePresentationURL", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetImagePresentationURL",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetImageURL(self, ReqEncoding, ReqCompression, ReqResolution, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetImageURL action.

            :returns: "RetImageURL"
        """
        arguments = {
            "ReqEncoding": ReqEncoding,
            "ReqCompression": ReqCompression,
            "ReqResolution": ReqResolution,
        }

        out_params = self.call_action("GetImageURL", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetImageURL",)]
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
