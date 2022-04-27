"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Scan1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Scan1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Scan:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AppendSideNumber": { "data_type": "string", "default": "0", "allowed_list": "['device-setting', '0']"},
        "BaseName": { "data_type": "string", "default": "pull-relative", "allowed_list": None},
        "BitDepth": { "data_type": "string", "default": "8", "allowed_list": "['device-setting', '8']"},
        "ColorSpace": { "data_type": "string", "default": "sRGB", "allowed_list": "['device-setting', 'sRGB']"},
        "ColorType": { "data_type": "string", "default": "Color", "allowed_list": "['device-setting', 'Color']"},
        "CompressionFactor": { "data_type": "i4", "default": "100", "allowed_list": None},
        "Destination": { "data_type": "string", "default": None, "allowed_list": None},
        "DeviceID": { "data_type": "string", "default": None, "allowed_list": None},
        "ErrorTimeout": { "data_type": "i4", "default": None, "allowed_list": None},
        "HeightLimit": { "data_type": "i4", "default": None, "allowed_list": None},
        "ImageFormat": { "data_type": "string", "default": "image/jpeg", "allowed_list": "['device-setting', 'image/jpeg']"},
        "ImageType": { "data_type": "string", "default": "Mixed", "allowed_list": "['device-setting', 'Mixed']"},
        "JobID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "JobName": { "data_type": "string", "default": None, "allowed_list": None},
        "RegistrationID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "Resolution": { "data_type": "string", "default": None, "allowed_list": None},
        "SideCount": { "data_type": "i4", "default": "0", "allowed_list": None},
        "StateReason": { "data_type": "string", "default": None, "allowed_list": None},
        "Timeout": { "data_type": "i4", "default": None, "allowed_list": None},
        "UseFeeder": { "data_type": "string", "default": "0", "allowed_list": "['device-setting', '0']"},
        "WidthLimit": { "data_type": "i4", "default": None, "allowed_list": None},
        "XValueLimit": { "data_type": "i4", "default": None, "allowed_list": None},
        "YValueLimit": { "data_type": "i4", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "DestinationID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "FailureCode": { "data_type": "string", "default": "No Error", "allowed_list": "['No Error', 'Jammed', 'Timeout Reached', 'ErredTimeout Reached', 'Destination Not Reachable']"},
        "ScanLength": { "data_type": "i4", "default": "0", "allowed_list": None},
        "SideNumber": { "data_type": "i4", "default": "1", "allowed_list": None},
        "State": { "data_type": "string", "default": "Idle", "allowed_list": "['Idle', 'Reserved', 'NotReady', 'Pending', 'Scanning', 'Finishing', 'Erred']"},
    }

    def action_GetConfiguration(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetConfiguration action.

            :returns: "JobNameOut", "ResolutionOut", "ImageXOffsetOut", "ImageYOffsetOut", "ImageWidthOut", "ImageHeightOut", "ImageFormatOut", "CompressionFactorOut", "ImageTypeOut", "ColorTypeOut", "BitDepthOut", "ColorSpaceOut", "BaseNameOut", "AppendSideNumberOut", "TimeoutOut"
        """
        arguments = { }

        out_params = self.call_action("GetConfiguration", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("JobNameOut", "ResolutionOut", "ImageXOffsetOut", "ImageYOffsetOut", "ImageWidthOut", "ImageHeightOut", "ImageFormatOut", "CompressionFactorOut", "ImageTypeOut", "ColorTypeOut", "BitDepthOut", "ColorSpaceOut", "BaseNameOut", "AppendSideNumberOut", "TimeoutOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSideInformation(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSideInformation action.

            :returns: "SideNumberOut", "SideCountOut", "ScanLengthOut"
        """
        arguments = { }

        out_params = self.call_action("GetSideInformation", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SideNumberOut", "SideCountOut", "ScanLengthOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetState(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetState action.

            :returns: "StateOut", "StateReasonOut", "FailureCodeOut"
        """
        arguments = { }

        out_params = self.call_action("GetState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut", "StateReasonOut", "FailureCodeOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StartScan(self, RegistrationIDIn, UseFeederIn, SideCountIn, JobNameIn, ResolutionIn, ImageXOffsetIn, ImageYOffsetIn, ImageWidthIn, ImageHeightIn, ImageFormatIn, CompressionFactorIn, ImageTypeIn, ColorTypeIn, BitDepthIn, ColorSpaceIn, BaseNameIn, AppendSideNumberIn, TimeoutIn, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartScan action.

            :returns: "ActualTimeoutOut", "JobIDOut", "ActualWidthOut", "ActualHeightOut"
        """
        arguments = {
            "RegistrationIDIn": RegistrationIDIn,
            "UseFeederIn": UseFeederIn,
            "SideCountIn": SideCountIn,
            "JobNameIn": JobNameIn,
            "ResolutionIn": ResolutionIn,
            "ImageXOffsetIn": ImageXOffsetIn,
            "ImageYOffsetIn": ImageYOffsetIn,
            "ImageWidthIn": ImageWidthIn,
            "ImageHeightIn": ImageHeightIn,
            "ImageFormatIn": ImageFormatIn,
            "CompressionFactorIn": CompressionFactorIn,
            "ImageTypeIn": ImageTypeIn,
            "ColorTypeIn": ColorTypeIn,
            "BitDepthIn": BitDepthIn,
            "ColorSpaceIn": ColorSpaceIn,
            "BaseNameIn": BaseNameIn,
            "AppendSideNumberIn": AppendSideNumberIn,
            "TimeoutIn": TimeoutIn,
        }

        out_params = self.call_action("StartScan", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ActualTimeoutOut", "JobIDOut", "ActualWidthOut", "ActualHeightOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
