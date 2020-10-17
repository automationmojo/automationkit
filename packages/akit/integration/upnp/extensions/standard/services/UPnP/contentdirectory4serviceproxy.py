"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ContentDirectory4ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ContentDirectory4' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ContentDirectory:4'


    def action_Browse(self, ObjectID, BrowseFlag, Filter, StartingIndex, RequestedCount, SortCriteria, extract_returns=True):
        """
            Calls the Browse action.

            :returns: "Result", "NumberReturned", "TotalMatches", "UpdateID"
        """
        arguments = {
            "ObjectID": ObjectID,
            "BrowseFlag": BrowseFlag,
            "Filter": Filter,
            "StartingIndex": StartingIndex,
            "RequestedCount": RequestedCount,
            "SortCriteria": SortCriteria,
        }

        out_params = self.proxy_call_action("Browse", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "NumberReturned", "TotalMatches", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_CancelDeviceMode(self, DeviceModeID, extract_returns=True):
        """
            Calls the CancelDeviceMode action.

            :returns: "result"
        """
        arguments = {
            "DeviceModeID": DeviceModeID,
        }

        out_params = self.proxy_call_action("CancelDeviceMode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_CancelTransformTask(self, TransformTaskID, extract_returns=True):
        """
            Calls the CancelTransformTask action.

            :returns: "result"
        """
        arguments = {
            "TransformTaskID": TransformTaskID,
        }

        out_params = self.proxy_call_action("CancelTransformTask", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_CreateObject(self, ContainerID, Elements, extract_returns=True):
        """
            Calls the CreateObject action.

            :returns: "ObjectID", "Result"
        """
        arguments = {
            "ContainerID": ContainerID,
            "Elements": Elements,
        }

        out_params = self.proxy_call_action("CreateObject", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ObjectID", "Result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_CreateReference(self, ContainerID, ObjectID, extract_returns=True):
        """
            Calls the CreateReference action.

            :returns: "NewID"
        """
        arguments = {
            "ContainerID": ContainerID,
            "ObjectID": ObjectID,
        }

        out_params = self.proxy_call_action("CreateReference", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_DeleteResource(self, ResourceURI, extract_returns=True):
        """
            Calls the DeleteResource action.

            :returns: "result"
        """
        arguments = {
            "ResourceURI": ResourceURI,
        }

        out_params = self.proxy_call_action("DeleteResource", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_DestroyObject(self, ObjectID, extract_returns=True):
        """
            Calls the DestroyObject action.

            :returns: "result"
        """
        arguments = {
            "ObjectID": ObjectID,
        }

        out_params = self.proxy_call_action("DestroyObject", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_EvaluateTransforms(self, TransformResourceDesc, TransformSettings, extract_returns=True):
        """
            Calls the EvaluateTransforms action.

            :returns: "EvaluationResult"
        """
        arguments = {
            "TransformResourceDesc": TransformResourceDesc,
            "TransformSettings": TransformSettings,
        }

        out_params = self.proxy_call_action("EvaluateTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("EvaluationResult",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_ExportResource(self, SourceURI, DestinationURI, extract_returns=True):
        """
            Calls the ExportResource action.

            :returns: "TransferID"
        """
        arguments = {
            "SourceURI": SourceURI,
            "DestinationURI": DestinationURI,
        }

        out_params = self.proxy_call_action("ExportResource", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransferID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_ExtendDeviceMode(self, DeviceModeID, DeviceModeRequest, extract_returns=True):
        """
            Calls the ExtendDeviceMode action.

            :returns: "DeviceModeStatus"
        """
        arguments = {
            "DeviceModeID": DeviceModeID,
            "DeviceModeRequest": DeviceModeRequest,
        }

        out_params = self.proxy_call_action("ExtendDeviceMode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DeviceModeStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_FreeFormQuery(self, ContainerID, CDSView, QueryRequest, extract_returns=True):
        """
            Calls the FreeFormQuery action.

            :returns: "QueryResult", "UpdateID"
        """
        arguments = {
            "ContainerID": ContainerID,
            "CDSView": CDSView,
            "QueryRequest": QueryRequest,
        }

        out_params = self.proxy_call_action("FreeFormQuery", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("QueryResult", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetAllAvailableTransforms(self, extract_returns=True):
        """
            Calls the GetAllAvailableTransforms action.

            :returns: "AllAvailableTransforms"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetAllAvailableTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AllAvailableTransforms",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetAllowedTransforms(self, TransformResourceObjectDesc, extract_returns=True):
        """
            Calls the GetAllowedTransforms action.

            :returns: "AllowedTransforms"
        """
        arguments = {
            "TransformResourceObjectDesc": TransformResourceObjectDesc,
        }

        out_params = self.proxy_call_action("GetAllowedTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AllowedTransforms",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetCurrentTransformStatusList(self, extract_returns=True):
        """
            Calls the GetCurrentTransformStatusList action.

            :returns: "TransformStatus"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetCurrentTransformStatusList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransformStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetDeviceMode(self, extract_returns=True):
        """
            Calls the GetDeviceMode action.

            :returns: "DeviceMode"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetDeviceMode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DeviceMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetDeviceModeStatus(self, extract_returns=True):
        """
            Calls the GetDeviceModeStatus action.

            :returns: "DeviceModeStatus"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetDeviceModeStatus", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DeviceModeStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetFeatureList(self, extract_returns=True):
        """
            Calls the GetFeatureList action.

            :returns: "FeatureList"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetFeatureList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FeatureList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetFreeFormQueryCapabilities(self, extract_returns=True):
        """
            Calls the GetFreeFormQueryCapabilities action.

            :returns: "FFQCapabilities"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetFreeFormQueryCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FFQCapabilities",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetPermissionsInfo(self, extract_returns=True):
        """
            Calls the GetPermissionsInfo action.

            :returns: "PermissionsInfo"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetPermissionsInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PermissionsInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetSearchCapabilities(self, extract_returns=True):
        """
            Calls the GetSearchCapabilities action.

            :returns: "SearchCaps"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetSearchCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SearchCaps",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetServiceResetToken(self, extract_returns=True):
        """
            Calls the GetServiceResetToken action.

            :returns: "ResetToken"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetServiceResetToken", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ResetToken",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetSortCapabilities(self, extract_returns=True):
        """
            Calls the GetSortCapabilities action.

            :returns: "SortCaps"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetSortCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SortCaps",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetSortExtensionCapabilities(self, extract_returns=True):
        """
            Calls the GetSortExtensionCapabilities action.

            :returns: "SortExtensionCaps"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetSortExtensionCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SortExtensionCaps",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetSystemUpdateID(self, extract_returns=True):
        """
            Calls the GetSystemUpdateID action.

            :returns: "Id"
        """
        arguments = { }

        out_params = self.proxy_call_action("GetSystemUpdateID", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Id",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetTransferProgress(self, TransferID, extract_returns=True):
        """
            Calls the GetTransferProgress action.

            :returns: "TransferStatus", "TransferLength", "TransferTotal"
        """
        arguments = {
            "TransferID": TransferID,
        }

        out_params = self.proxy_call_action("GetTransferProgress", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransferStatus", "TransferLength", "TransferTotal",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetTransformTaskResult(self, TransformTaskID, TransformTaskResultFilter, extract_returns=True):
        """
            Calls the GetTransformTaskResult action.

            :returns: "TransformTaskResult"
        """
        arguments = {
            "TransformTaskID": TransformTaskID,
            "TransformTaskResultFilter": TransformTaskResultFilter,
        }

        out_params = self.proxy_call_action("GetTransformTaskResult", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransformTaskResult",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetTransforms(self, TransformTaskID, extract_returns=True):
        """
            Calls the GetTransforms action.

            :returns: "CurrentTransformSettings"
        """
        arguments = {
            "TransformTaskID": TransformTaskID,
        }

        out_params = self.proxy_call_action("GetTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTransformSettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_ImportResource(self, SourceURI, DestinationURI, extract_returns=True):
        """
            Calls the ImportResource action.

            :returns: "TransferID"
        """
        arguments = {
            "SourceURI": SourceURI,
            "DestinationURI": DestinationURI,
        }

        out_params = self.proxy_call_action("ImportResource", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransferID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_MoveObject(self, ObjectID, NewParentID, extract_returns=True):
        """
            Calls the MoveObject action.

            :returns: "NewObjectID"
        """
        arguments = {
            "ObjectID": ObjectID,
            "NewParentID": NewParentID,
        }

        out_params = self.proxy_call_action("MoveObject", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewObjectID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_PauseTransformTask(self, TransformTaskID, extract_returns=True):
        """
            Calls the PauseTransformTask action.

            :returns: "result"
        """
        arguments = {
            "TransformTaskID": TransformTaskID,
        }

        out_params = self.proxy_call_action("PauseTransformTask", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_RequestDeviceMode(self, CPID, DeviceModeRequest, extract_returns=True):
        """
            Calls the RequestDeviceMode action.

            :returns: "DeviceModeID", "DeviceModeStatus"
        """
        arguments = {
            "CPID": CPID,
            "DeviceModeRequest": DeviceModeRequest,
        }

        out_params = self.proxy_call_action("RequestDeviceMode", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DeviceModeID", "DeviceModeStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_ResumeTransformTask(self, TransformTaskID, extract_returns=True):
        """
            Calls the ResumeTransformTask action.

            :returns: "result"
        """
        arguments = {
            "TransformTaskID": TransformTaskID,
        }

        out_params = self.proxy_call_action("ResumeTransformTask", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_RollbackTransformTask(self, TransformTaskID, extract_returns=True):
        """
            Calls the RollbackTransformTask action.

            :returns: "result"
        """
        arguments = {
            "TransformTaskID": TransformTaskID,
        }

        out_params = self.proxy_call_action("RollbackTransformTask", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_Search(self, ContainerID, SearchCriteria, Filter, StartingIndex, RequestedCount, SortCriteria, extract_returns=True):
        """
            Calls the Search action.

            :returns: "Result", "NumberReturned", "TotalMatches", "UpdateID"
        """
        arguments = {
            "ContainerID": ContainerID,
            "SearchCriteria": SearchCriteria,
            "Filter": Filter,
            "StartingIndex": StartingIndex,
            "RequestedCount": RequestedCount,
            "SortCriteria": SortCriteria,
        }

        out_params = self.proxy_call_action("Search", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "NumberReturned", "TotalMatches", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_StartTransformTask(self, TransformResourceDesc, TransformSettings, TransformOverwrite, TransformRollback, extract_returns=True):
        """
            Calls the StartTransformTask action.

            :returns: "TransformTaskID"
        """
        arguments = {
            "TransformResourceDesc": TransformResourceDesc,
            "TransformSettings": TransformSettings,
            "TransformOverwrite": TransformOverwrite,
            "TransformRollback": TransformRollback,
        }

        out_params = self.proxy_call_action("StartTransformTask", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransformTaskID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_StopTransferResource(self, TransferID, extract_returns=True):
        """
            Calls the StopTransferResource action.

            :returns: "result"
        """
        arguments = {
            "TransferID": TransferID,
        }

        out_params = self.proxy_call_action("StopTransferResource", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_UpdateObject(self, ObjectID, CurrentTagValue, NewTagValue, extract_returns=True):
        """
            Calls the UpdateObject action.

            :returns: "result"
        """
        arguments = {
            "ObjectID": ObjectID,
            "CurrentTagValue": CurrentTagValue,
            "NewTagValue": NewTagValue,
        }

        out_params = self.proxy_call_action("UpdateObject", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

