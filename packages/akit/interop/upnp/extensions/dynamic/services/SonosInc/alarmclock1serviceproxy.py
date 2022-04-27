"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class AlarmClock1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'AlarmClock1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:AlarmClock:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "AlarmListVersion": { "data_type": "string", "default": None, "allowed_list": None},
        "DailyIndexRefreshTime": { "data_type": "string", "default": None, "allowed_list": None},
        "DateFormat": { "data_type": "string", "default": None, "allowed_list": None},
        "TimeFormat": { "data_type": "string", "default": None, "allowed_list": None},
        "TimeGeneration": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TimeServer": { "data_type": "string", "default": None, "allowed_list": None},
        "TimeZone": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_CreateAlarm(self, StartLocalTime, Duration, Recurrence, Enabled, RoomUUID, ProgramURI, ProgramMetaData, PlayMode, Volume, IncludeLinkedZones, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateAlarm action.

            :returns: "AssignedID"
        """
        arguments = {
            "StartLocalTime": StartLocalTime,
            "Duration": Duration,
            "Recurrence": Recurrence,
            "Enabled": Enabled,
            "RoomUUID": RoomUUID,
            "ProgramURI": ProgramURI,
            "ProgramMetaData": ProgramMetaData,
            "PlayMode": PlayMode,
            "Volume": Volume,
            "IncludeLinkedZones": IncludeLinkedZones,
        }

        out_params = self.call_action("CreateAlarm", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AssignedID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DestroyAlarm(self, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DestroyAlarm action.
        """
        arguments = {
            "ID": ID,
        }

        self.call_action("DestroyAlarm", arguments=arguments, aspects=aspects)

        return

    def action_GetDailyIndexRefreshTime(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDailyIndexRefreshTime action.

            :returns: "CurrentDailyIndexRefreshTime"
        """
        arguments = { }

        out_params = self.call_action("GetDailyIndexRefreshTime", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentDailyIndexRefreshTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFormat(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFormat action.

            :returns: "CurrentTimeFormat", "CurrentDateFormat"
        """
        arguments = { }

        out_params = self.call_action("GetFormat", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTimeFormat", "CurrentDateFormat",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetHouseholdTimeAtStamp(self, TimeStamp, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetHouseholdTimeAtStamp action.

            :returns: "HouseholdUTCTime"
        """
        arguments = {
            "TimeStamp": TimeStamp,
        }

        out_params = self.call_action("GetHouseholdTimeAtStamp", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("HouseholdUTCTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTimeNow(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTimeNow action.

            :returns: "CurrentUTCTime", "CurrentLocalTime", "CurrentTimeZone", "CurrentTimeGeneration"
        """
        arguments = { }

        out_params = self.call_action("GetTimeNow", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentUTCTime", "CurrentLocalTime", "CurrentTimeZone", "CurrentTimeGeneration",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTimeServer(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTimeServer action.

            :returns: "CurrentTimeServer"
        """
        arguments = { }

        out_params = self.call_action("GetTimeServer", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTimeServer",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTimeZone(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTimeZone action.

            :returns: "Index", "AutoAdjustDst"
        """
        arguments = { }

        out_params = self.call_action("GetTimeZone", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Index", "AutoAdjustDst",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTimeZoneAndRule(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTimeZoneAndRule action.

            :returns: "Index", "AutoAdjustDst", "CurrentTimeZone"
        """
        arguments = { }

        out_params = self.call_action("GetTimeZoneAndRule", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Index", "AutoAdjustDst", "CurrentTimeZone",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTimeZoneRule(self, Index, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTimeZoneRule action.

            :returns: "TimeZone"
        """
        arguments = {
            "Index": Index,
        }

        out_params = self.call_action("GetTimeZoneRule", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TimeZone",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ListAlarms(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ListAlarms action.

            :returns: "CurrentAlarmList", "CurrentAlarmListVersion"
        """
        arguments = { }

        out_params = self.call_action("ListAlarms", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentAlarmList", "CurrentAlarmListVersion",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetDailyIndexRefreshTime(self, DesiredDailyIndexRefreshTime, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDailyIndexRefreshTime action.
        """
        arguments = {
            "DesiredDailyIndexRefreshTime": DesiredDailyIndexRefreshTime,
        }

        self.call_action("SetDailyIndexRefreshTime", arguments=arguments, aspects=aspects)

        return

    def action_SetFormat(self, DesiredTimeFormat, DesiredDateFormat, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetFormat action.
        """
        arguments = {
            "DesiredTimeFormat": DesiredTimeFormat,
            "DesiredDateFormat": DesiredDateFormat,
        }

        self.call_action("SetFormat", arguments=arguments, aspects=aspects)

        return

    def action_SetTimeNow(self, DesiredTime, TimeZoneForDesiredTime, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetTimeNow action.
        """
        arguments = {
            "DesiredTime": DesiredTime,
            "TimeZoneForDesiredTime": TimeZoneForDesiredTime,
        }

        self.call_action("SetTimeNow", arguments=arguments, aspects=aspects)

        return

    def action_SetTimeServer(self, DesiredTimeServer, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetTimeServer action.
        """
        arguments = {
            "DesiredTimeServer": DesiredTimeServer,
        }

        self.call_action("SetTimeServer", arguments=arguments, aspects=aspects)

        return

    def action_SetTimeZone(self, Index, AutoAdjustDst, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetTimeZone action.
        """
        arguments = {
            "Index": Index,
            "AutoAdjustDst": AutoAdjustDst,
        }

        self.call_action("SetTimeZone", arguments=arguments, aspects=aspects)

        return

    def action_UpdateAlarm(self, ID, StartLocalTime, Duration, Recurrence, Enabled, RoomUUID, ProgramURI, ProgramMetaData, PlayMode, Volume, IncludeLinkedZones, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UpdateAlarm action.
        """
        arguments = {
            "ID": ID,
            "StartLocalTime": StartLocalTime,
            "Duration": Duration,
            "Recurrence": Recurrence,
            "Enabled": Enabled,
            "RoomUUID": RoomUUID,
            "ProgramURI": ProgramURI,
            "ProgramMetaData": ProgramMetaData,
            "PlayMode": PlayMode,
            "Volume": Volume,
            "IncludeLinkedZones": IncludeLinkedZones,
        }

        self.call_action("UpdateAlarm", arguments=arguments, aspects=aspects)

        return
