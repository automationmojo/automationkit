"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ScheduledRecording2ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ScheduledRecording2' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ScheduledRecording:2'

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_BrowseRecordSchedules(self, Filter, StartingIndex, RequestedCount, SortCriteria, extract_returns=True):
        """
            Calls the BrowseRecordSchedules action.

            :returns: "Result", "NumberReturned", "TotalMatches", "UpdateID"
        """
        arguments = {
            "Filter": Filter,
            "StartingIndex": StartingIndex,
            "RequestedCount": RequestedCount,
            "SortCriteria": SortCriteria,
        }

        out_params = self._proxy_call_action("BrowseRecordSchedules", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "NumberReturned", "TotalMatches", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_BrowseRecordTasks(self, RecordScheduleID, Filter, StartingIndex, RequestedCount, SortCriteria, extract_returns=True):
        """
            Calls the BrowseRecordTasks action.

            :returns: "Result", "NumberReturned", "TotalMatches", "UpdateID"
        """
        arguments = {
            "RecordScheduleID": RecordScheduleID,
            "Filter": Filter,
            "StartingIndex": StartingIndex,
            "RequestedCount": RequestedCount,
            "SortCriteria": SortCriteria,
        }

        out_params = self._proxy_call_action("BrowseRecordTasks", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "NumberReturned", "TotalMatches", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_CreateRecordSchedule(self, Elements, extract_returns=True):
        """
            Calls the CreateRecordSchedule action.

            :returns: "RecordScheduleID", "Result", "UpdateID"
        """
        arguments = {
            "Elements": Elements,
        }

        out_params = self._proxy_call_action("CreateRecordSchedule", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RecordScheduleID", "Result", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteRecordSchedule(self, RecordScheduleID):
        """
            Calls the DeleteRecordSchedule action.
        """
        arguments = {
            "RecordScheduleID": RecordScheduleID,
        }

        self._proxy_call_action("DeleteRecordSchedule", arguments=arguments)

        return

    def action_DeleteRecordTask(self, RecordTaskID):
        """
            Calls the DeleteRecordTask action.
        """
        arguments = {
            "RecordTaskID": RecordTaskID,
        }

        self._proxy_call_action("DeleteRecordTask", arguments=arguments)

        return

    def action_DisableRecordSchedule(self, RecordScheduleID):
        """
            Calls the DisableRecordSchedule action.
        """
        arguments = {
            "RecordScheduleID": RecordScheduleID,
        }

        self._proxy_call_action("DisableRecordSchedule", arguments=arguments)

        return

    def action_DisableRecordTask(self, RecordTaskID):
        """
            Calls the DisableRecordTask action.
        """
        arguments = {
            "RecordTaskID": RecordTaskID,
        }

        self._proxy_call_action("DisableRecordTask", arguments=arguments)

        return

    def action_EnableRecordSchedule(self, RecordScheduleID):
        """
            Calls the EnableRecordSchedule action.
        """
        arguments = {
            "RecordScheduleID": RecordScheduleID,
        }

        self._proxy_call_action("EnableRecordSchedule", arguments=arguments)

        return

    def action_EnableRecordTask(self, RecordTaskID):
        """
            Calls the EnableRecordTask action.
        """
        arguments = {
            "RecordTaskID": RecordTaskID,
        }

        self._proxy_call_action("EnableRecordTask", arguments=arguments)

        return

    def action_GetAllowedValues(self, DataTypeID, Filter, extract_returns=True):
        """
            Calls the GetAllowedValues action.

            :returns: "PropertyInfo"
        """
        arguments = {
            "DataTypeID": DataTypeID,
            "Filter": Filter,
        }

        out_params = self._proxy_call_action("GetAllowedValues", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PropertyInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPropertyList(self, DataTypeID, extract_returns=True):
        """
            Calls the GetPropertyList action.

            :returns: "PropertyList"
        """
        arguments = {
            "DataTypeID": DataTypeID,
        }

        out_params = self._proxy_call_action("GetPropertyList", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PropertyList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRecordSchedule(self, RecordScheduleID, Filter, extract_returns=True):
        """
            Calls the GetRecordSchedule action.

            :returns: "Result", "UpdateID"
        """
        arguments = {
            "RecordScheduleID": RecordScheduleID,
            "Filter": Filter,
        }

        out_params = self._proxy_call_action("GetRecordSchedule", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRecordScheduleConflicts(self, RecordScheduleID, extract_returns=True):
        """
            Calls the GetRecordScheduleConflicts action.

            :returns: "RecordScheduleConflictIDList", "UpdateID"
        """
        arguments = {
            "RecordScheduleID": RecordScheduleID,
        }

        out_params = self._proxy_call_action("GetRecordScheduleConflicts", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RecordScheduleConflictIDList", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRecordTask(self, RecordTaskID, Filter, extract_returns=True):
        """
            Calls the GetRecordTask action.

            :returns: "Result", "UpdateID"
        """
        arguments = {
            "RecordTaskID": RecordTaskID,
            "Filter": Filter,
        }

        out_params = self._proxy_call_action("GetRecordTask", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRecordTaskConflicts(self, RecordTaskID, extract_returns=True):
        """
            Calls the GetRecordTaskConflicts action.

            :returns: "RecordTaskConflictIDList", "UpdateID"
        """
        arguments = {
            "RecordTaskID": RecordTaskID,
        }

        out_params = self._proxy_call_action("GetRecordTaskConflicts", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RecordTaskConflictIDList", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSortCapabilities(self, extract_returns=True):
        """
            Calls the GetSortCapabilities action.

            :returns: "SortCaps", "SortLevelCap"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetSortCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SortCaps", "SortLevelCap",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetStateUpdateID(self, extract_returns=True):
        """
            Calls the GetStateUpdateID action.

            :returns: "Id"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetStateUpdateID", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Id",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetRecordTask(self, RecordTaskID):
        """
            Calls the ResetRecordTask action.
        """
        arguments = {
            "RecordTaskID": RecordTaskID,
        }

        self._proxy_call_action("ResetRecordTask", arguments=arguments)

        return
