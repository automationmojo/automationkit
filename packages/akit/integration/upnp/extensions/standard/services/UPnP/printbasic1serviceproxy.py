"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import Aspects, DEFAULT_ASPECTS

from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class PrintBasic1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'PrintBasic1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:PrintBasic:1'

    SERVICE_EVENT_VARIABLES = {
        "JobEndState": { "data_type": "string", "default": None, "allowed_list": None},
        "JobIdList": { "data_type": "string", "default": None, "allowed_list": None},
        "JobMediaSheetsCompleted": { "data_type": "i4", "default": None, "allowed_list": None},
        "PrinterState": { "data_type": "string", "default": "idle", "allowed_list": "['idle', 'processing', 'stopped']"},
        "PrinterStateReasons": { "data_type": "string", "default": "none", "allowed_list": "['none', 'attention-required', 'media-jam', 'paused', 'door-open', 'media-low', 'media-empty', 'output-area-almost-full', 'output-area-full', 'marker-supply-low', 'marker-supply-empty', 'marker-failure', 'media-change-request']"},
    }

    def action_CancelJob(self, JobId, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the CancelJob action.
        """
        arguments = {
            "JobId": JobId,
        }

        self._proxy_call_action("CancelJob", arguments=arguments, aspects=aspects)

        return

    def action_CreateJob(self, JobName, JobOriginatingUserName, DocumentFormat, Copies, Sides, NumberUp, OrientationRequested, MediaSize, MediaType, PrintQuality, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
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

        out_params = self._proxy_call_action("CreateJob", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("JobId", "DataSink",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetJobAttributes(self, JobId, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetJobAttributes action.

            :returns: "JobName", "JobOriginatingUserName", "JobMediaSheetsCompleted"
        """
        arguments = {
            "JobId": JobId,
        }

        out_params = self._proxy_call_action("GetJobAttributes", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("JobName", "JobOriginatingUserName", "JobMediaSheetsCompleted",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPrinterAttributes(self, extract_returns=True, aspects:Aspects=DEFAULT_ASPECTS):
        """
            Calls the GetPrinterAttributes action.

            :returns: "PrinterState", "PrinterStateReasons", "JobIdList", "JobId"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetPrinterAttributes", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PrinterState", "PrinterStateReasons", "JobIdList", "JobId",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
