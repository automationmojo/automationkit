"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Scan1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Scan1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Scan:1'

    SERVICE_EVENT_VARIABLES = {
        "DestinationID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "FailureCode": { "data_type": "string", "default": "No Error", "allowed_list": "['No Error', 'Jammed', 'Timeout Reached', 'ErredTimeout Reached', 'Destination Not Reachable']"},
        "ScanLength": { "data_type": "i4", "default": "0", "allowed_list": None},
        "SideNumber": { "data_type": "i4", "default": "1", "allowed_list": None},
        "State": { "data_type": "string", "default": "Idle", "allowed_list": "['Idle', 'Reserved', 'NotReady', 'Pending', 'Scanning', 'Finishing', 'Erred']"},
    }

    def action_GetConfiguration(self, extract_returns=True):
        """
            Calls the GetConfiguration action.

            :returns: "JobNameOut", "ResolutionOut", "ImageXOffsetOut", "ImageYOffsetOut", "ImageWidthOut", "ImageHeightOut", "ImageFormatOut", "CompressionFactorOut", "ImageTypeOut", "ColorTypeOut", "BitDepthOut", "ColorSpaceOut", "BaseNameOut", "AppendSideNumberOut", "TimeoutOut"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetConfiguration", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("JobNameOut", "ResolutionOut", "ImageXOffsetOut", "ImageYOffsetOut", "ImageWidthOut", "ImageHeightOut", "ImageFormatOut", "CompressionFactorOut", "ImageTypeOut", "ColorTypeOut", "BitDepthOut", "ColorSpaceOut", "BaseNameOut", "AppendSideNumberOut", "TimeoutOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSideInformation(self, extract_returns=True):
        """
            Calls the GetSideInformation action.

            :returns: "SideNumberOut", "SideCountOut", "ScanLengthOut"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetSideInformation", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SideNumberOut", "SideCountOut", "ScanLengthOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetState(self, extract_returns=True):
        """
            Calls the GetState action.

            :returns: "StateOut", "StateReasonOut", "FailureCodeOut"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetState", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateOut", "StateReasonOut", "FailureCodeOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StartScan(self, RegistrationIDIn, UseFeederIn, SideCountIn, JobNameIn, ResolutionIn, ImageXOffsetIn, ImageYOffsetIn, ImageWidthIn, ImageHeightIn, ImageFormatIn, CompressionFactorIn, ImageTypeIn, ColorTypeIn, BitDepthIn, ColorSpaceIn, BaseNameIn, AppendSideNumberIn, TimeoutIn, extract_returns=True):
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

        out_params = self._proxy_call_action("StartScan", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ActualTimeoutOut", "JobIDOut", "ActualWidthOut", "ActualHeightOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
