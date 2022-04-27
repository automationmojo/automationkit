"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class PrintEnhanced1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'PrintEnhanced1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:PrintEnhanced:1'

    SERVICE_DEFAULT_VARIABLES = {
        "CharRepSupported": { "data_type": "string", "default": None, "allowed_list": None},
        "ColorSupported": { "data_type": "boolean", "default": None, "allowed_list": None},
        "Copies": { "data_type": "i4", "default": None, "allowed_list": None},
        "CriticalAttributesSupported": { "data_type": "string", "default": None, "allowed_list": None},
        "DataSink": { "data_type": "uri", "default": None, "allowed_list": None},
        "DeviceId": { "data_type": "string", "default": None, "allowed_list": None},
        "DocumentFormat": { "data_type": "string", "default": None, "allowed_list": "['unknown', 'application/xhtml-print', 'application/xhtml-print-e']"},
        "DocumentUTF16Supported": { "data_type": "string", "default": None, "allowed_list": None},
        "FullBleedSupported": { "data_type": "boolean", "default": None, "allowed_list": None},
        "InternetConnectState": { "data_type": "string", "default": None, "allowed_list": None},
        "JobId": { "data_type": "i4", "default": "0", "allowed_list": None},
        "JobName": { "data_type": "string", "default": None, "allowed_list": None},
        "JobOriginatingUserName": { "data_type": "string", "default": None, "allowed_list": None},
        "MediaSize": { "data_type": "string", "default": None, "allowed_list": "['device-setting']"},
        "MediaType": { "data_type": "string", "default": None, "allowed_list": "['device-setting', 'none']"},
        "NumberUp": { "data_type": "string", "default": "1", "allowed_list": "['1', 'device-setting']"},
        "OrientationRequested": { "data_type": "string", "default": None, "allowed_list": "['portrait', 'device-setting']"},
        "PageMargins": { "data_type": "string", "default": None, "allowed_list": None},
        "PrintQuality": { "data_type": "string", "default": None, "allowed_list": "['normal', 'device-setting']"},
        "PrinterLocation": { "data_type": "string", "default": None, "allowed_list": None},
        "PrinterName": { "data_type": "string", "default": None, "allowed_list": None},
        "Sides": { "data_type": "string", "default": None, "allowed_list": "['one-sided', 'device-setting']"},
        "SourceURI": { "data_type": "uri", "default": None, "allowed_list": None},
        "XHTMLImageSupported": { "data_type": "string", "default": "image/jpeg", "allowed_list": "['image/jpeg']"},
    }

    SERVICE_EVENT_VARIABLES = {
        "ContentCompleteList": { "data_type": "string", "default": None, "allowed_list": None},
        "JobAbortState": { "data_type": "string", "default": None, "allowed_list": None},
        "JobEndState": { "data_type": "string", "default": None, "allowed_list": None},
        "JobIdList": { "data_type": "string", "default": None, "allowed_list": None},
        "JobMediaSheetsCompleted": { "data_type": "i4", "default": None, "allowed_list": None},
        "PrinterState": { "data_type": "string", "default": "idle", "allowed_list": "['idle', 'processing', 'stopped']"},
        "PrinterStateReasons": { "data_type": "string", "default": "none", "allowed_list": "['none', 'attention-required', 'media-jam', 'paused', 'door-open', 'media-low', 'media-empty', 'output-area-almost-full', 'output-area-full', 'marker-supply-low', 'marker-supply-empty', 'marker-failure', 'media-change-request']"},
    }

    def action_CancelJob(self, JobId, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CancelJob action.
        """
        arguments = {
            "JobId": JobId,
        }

        self.call_action("CancelJob", arguments=arguments, aspects=aspects)

        return

    def action_CreateJob(self, JobName, JobOriginatingUserName, DocumentFormat, Copies, Sides, NumberUp, OrientationRequested, MediaSize, MediaType, PrintQuality, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateJob action.

            :returns: "JobId", "DataSink"
        """
        arguments = {
            "JobName": JobName,
            "JobOriginatingUserName": JobOriginatingUserName,
            "DocumentFormat": DocumentFormat,
            "Copies": Copies,
            "Sides": Sides,
            "NumberUp": NumberUp,
            "OrientationRequested": OrientationRequested,
            "MediaSize": MediaSize,
            "MediaType": MediaType,
            "PrintQuality": PrintQuality,
        }

        out_params = self.call_action("CreateJob", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("JobId", "DataSink",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_CreateJobV2(self, JobName, JobOriginatingUserName, DocumentFormat, Copies, Sides, NumberUp, OrientationRequested, MediaSize, MediaType, PrintQuality, CriticalAttributesList, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateJobV2 action.

            :returns: "JobId", "DataSink"
        """
        arguments = {
            "JobName": JobName,
            "JobOriginatingUserName": JobOriginatingUserName,
            "DocumentFormat": DocumentFormat,
            "Copies": Copies,
            "Sides": Sides,
            "NumberUp": NumberUp,
            "OrientationRequested": OrientationRequested,
            "MediaSize": MediaSize,
            "MediaType": MediaType,
            "PrintQuality": PrintQuality,
            "CriticalAttributesList": CriticalAttributesList,
        }

        out_params = self.call_action("CreateJobV2", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("JobId", "DataSink",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_CreateURIJob(self, JobName, JobOriginatingUserName, DocumentFormat, Copies, Sides, NumberUp, OrientationRequested, MediaSize, MediaType, PrintQuality, CriticalAttributesList, SourceURI, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateURIJob action.

            :returns: "JobId"
        """
        arguments = {
            "JobName": JobName,
            "JobOriginatingUserName": JobOriginatingUserName,
            "DocumentFormat": DocumentFormat,
            "Copies": Copies,
            "Sides": Sides,
            "NumberUp": NumberUp,
            "OrientationRequested": OrientationRequested,
            "MediaSize": MediaSize,
            "MediaType": MediaType,
            "PrintQuality": PrintQuality,
            "CriticalAttributesList": CriticalAttributesList,
            "SourceURI": SourceURI,
        }

        out_params = self.call_action("CreateURIJob", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("JobId",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetJobAttributes(self, JobId, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetJobAttributes action.

            :returns: "JobName", "JobOriginatingUserName", "JobMediaSheetsCompleted"
        """
        arguments = {
            "JobId": JobId,
        }

        out_params = self.call_action("GetJobAttributes", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("JobName", "JobOriginatingUserName", "JobMediaSheetsCompleted",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMargins(self, MediaSize, MediaType, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMargins action.

            :returns: "PageMargins", "FullBleedSupported"
        """
        arguments = {
            "MediaSize": MediaSize,
            "MediaType": MediaType,
        }

        out_params = self.call_action("GetMargins", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PageMargins", "FullBleedSupported",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMediaList(self, MediaSize, MediaType, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMediaList action.

            :returns: "MediaList"
        """
        arguments = {
            "MediaSize": MediaSize,
            "MediaType": MediaType,
        }

        out_params = self.call_action("GetMediaList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MediaList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPrinterAttributes(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPrinterAttributes action.

            :returns: "PrinterState", "PrinterStateReasons", "JobIdList", "JobId"
        """
        arguments = { }

        out_params = self.call_action("GetPrinterAttributes", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PrinterState", "PrinterStateReasons", "JobIdList", "JobId",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPrinterAttributesV2(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPrinterAttributesV2 action.

            :returns: "PrinterState", "PrinterStateReasons", "JobIdList", "JobId", "InternetConnectState"
        """
        arguments = { }

        out_params = self.call_action("GetPrinterAttributesV2", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PrinterState", "PrinterStateReasons", "JobIdList", "JobId", "InternetConnectState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
