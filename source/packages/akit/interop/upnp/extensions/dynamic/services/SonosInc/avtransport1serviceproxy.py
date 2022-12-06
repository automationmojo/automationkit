"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class AVTransport1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'AVTransport1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:AVTransport:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AVTransportURI": { "data_type": "string", "default": None, "allowed_list": None},
        "AVTransportURIMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "AbsoluteCounterPosition": { "data_type": "i4", "default": None, "allowed_list": None},
        "AbsoluteTimePosition": { "data_type": "string", "default": None, "allowed_list": None},
        "AlarmIDRunning": { "data_type": "ui4", "default": None, "allowed_list": None},
        "AlarmLoggedStartTime": { "data_type": "string", "default": None, "allowed_list": None},
        "AlarmRunning": { "data_type": "boolean", "default": None, "allowed_list": None},
        "CurrentCrossfadeMode": { "data_type": "boolean", "default": None, "allowed_list": None},
        "CurrentMediaDuration": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentPlayMode": { "data_type": "string", "default": "NORMAL", "allowed_list": "['NORMAL', 'REPEAT_ALL', 'REPEAT_ONE', 'SHUFFLE_NOREPEAT', 'SHUFFLE', 'SHUFFLE_REPEAT_ONE']"},
        "CurrentRecordQualityMode": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentSection": { "data_type": "ui4", "default": None, "allowed_list": None},
        "CurrentTrack": { "data_type": "ui4", "default": None, "allowed_list": None},
        "CurrentTrackDuration": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTrackMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTrackURI": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTransportActions": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentValidPlayModes": { "data_type": "string", "default": None, "allowed_list": None},
        "DirectControlAccountID": { "data_type": "string", "default": None, "allowed_list": None},
        "DirectControlClientID": { "data_type": "string", "default": None, "allowed_list": None},
        "DirectControlIsSuspended": { "data_type": "boolean", "default": None, "allowed_list": None},
        "EnqueuedTransportURI": { "data_type": "string", "default": None, "allowed_list": None},
        "EnqueuedTransportURIMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "MuseSessions": { "data_type": "string", "default": None, "allowed_list": None},
        "NextAVTransportURI": { "data_type": "string", "default": None, "allowed_list": None},
        "NextAVTransportURIMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "NextTrackMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "NextTrackURI": { "data_type": "string", "default": None, "allowed_list": None},
        "NumberOfTracks": { "data_type": "ui4", "default": None, "allowed_list": None},
        "PlaybackStorageMedium": { "data_type": "string", "default": None, "allowed_list": "['NONE', 'NETWORK']"},
        "PossiblePlaybackStorageMedia": { "data_type": "string", "default": None, "allowed_list": None},
        "PossibleRecordQualityModes": { "data_type": "string", "default": None, "allowed_list": None},
        "PossibleRecordStorageMedia": { "data_type": "string", "default": None, "allowed_list": None},
        "QueueUpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "RecordMediumWriteStatus": { "data_type": "string", "default": None, "allowed_list": None},
        "RecordStorageMedium": { "data_type": "string", "default": None, "allowed_list": "['NONE']"},
        "RelativeCounterPosition": { "data_type": "i4", "default": None, "allowed_list": None},
        "RelativeTimePosition": { "data_type": "string", "default": None, "allowed_list": None},
        "RestartPending": { "data_type": "boolean", "default": None, "allowed_list": None},
        "SleepTimerGeneration": { "data_type": "ui4", "default": None, "allowed_list": None},
        "SnoozeRunning": { "data_type": "boolean", "default": None, "allowed_list": None},
        "TransportErrorDescription": { "data_type": "string", "default": None, "allowed_list": None},
        "TransportErrorHttpCode": { "data_type": "string", "default": None, "allowed_list": None},
        "TransportErrorHttpHeaders": { "data_type": "string", "default": None, "allowed_list": None},
        "TransportErrorURI": { "data_type": "string", "default": None, "allowed_list": None},
        "TransportPlaySpeed": { "data_type": "string", "default": None, "allowed_list": "['1']"},
        "TransportState": { "data_type": "string", "default": None, "allowed_list": "['STOPPED', 'PLAYING', 'PAUSED_PLAYBACK', 'TRANSITIONING']"},
        "TransportStatus": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddMultipleURIsToQueue(self, InstanceID, UpdateID, NumberOfURIs, EnqueuedURIs, EnqueuedURIsMetaData, ContainerURI, ContainerMetaData, DesiredFirstTrackNumberEnqueued, EnqueueAsNext, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddMultipleURIsToQueue action.

            :returns: "FirstTrackNumberEnqueued", "NumTracksAdded", "NewQueueLength", "NewUpdateID"
        """
        arguments = {
            "InstanceID": InstanceID,
            "UpdateID": UpdateID,
            "NumberOfURIs": NumberOfURIs,
            "EnqueuedURIs": EnqueuedURIs,
            "EnqueuedURIsMetaData": EnqueuedURIsMetaData,
            "ContainerURI": ContainerURI,
            "ContainerMetaData": ContainerMetaData,
            "DesiredFirstTrackNumberEnqueued": DesiredFirstTrackNumberEnqueued,
            "EnqueueAsNext": EnqueueAsNext,
        }

        out_params = self.call_action("AddMultipleURIsToQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FirstTrackNumberEnqueued", "NumTracksAdded", "NewQueueLength", "NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AddURIToQueue(self, InstanceID, EnqueuedURI, EnqueuedURIMetaData, DesiredFirstTrackNumberEnqueued, EnqueueAsNext, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddURIToQueue action.

            :returns: "FirstTrackNumberEnqueued", "NumTracksAdded", "NewQueueLength"
        """
        arguments = {
            "InstanceID": InstanceID,
            "EnqueuedURI": EnqueuedURI,
            "EnqueuedURIMetaData": EnqueuedURIMetaData,
            "DesiredFirstTrackNumberEnqueued": DesiredFirstTrackNumberEnqueued,
            "EnqueueAsNext": EnqueueAsNext,
        }

        out_params = self.call_action("AddURIToQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FirstTrackNumberEnqueued", "NumTracksAdded", "NewQueueLength",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AddURIToSavedQueue(self, InstanceID, ObjectID, UpdateID, EnqueuedURI, EnqueuedURIMetaData, AddAtIndex, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddURIToSavedQueue action.

            :returns: "NumTracksAdded", "NewQueueLength", "NewUpdateID"
        """
        arguments = {
            "InstanceID": InstanceID,
            "ObjectID": ObjectID,
            "UpdateID": UpdateID,
            "EnqueuedURI": EnqueuedURI,
            "EnqueuedURIMetaData": EnqueuedURIMetaData,
            "AddAtIndex": AddAtIndex,
        }

        out_params = self.call_action("AddURIToSavedQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NumTracksAdded", "NewQueueLength", "NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_BackupQueue(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the BackupQueue action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("BackupQueue", arguments=arguments, aspects=aspects)

        return

    def action_BecomeCoordinatorOfStandaloneGroup(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the BecomeCoordinatorOfStandaloneGroup action.

            :returns: "DelegatedGroupCoordinatorID", "NewGroupID"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("BecomeCoordinatorOfStandaloneGroup", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DelegatedGroupCoordinatorID", "NewGroupID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_BecomeGroupCoordinator(self, InstanceID, CurrentCoordinator, CurrentGroupID, OtherMembers, TransportSettings, CurrentURI, CurrentURIMetaData, SleepTimerState, AlarmState, StreamRestartState, CurrentQueueTrackList, CurrentVLIState, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the BecomeGroupCoordinator action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "CurrentCoordinator": CurrentCoordinator,
            "CurrentGroupID": CurrentGroupID,
            "OtherMembers": OtherMembers,
            "TransportSettings": TransportSettings,
            "CurrentURI": CurrentURI,
            "CurrentURIMetaData": CurrentURIMetaData,
            "SleepTimerState": SleepTimerState,
            "AlarmState": AlarmState,
            "StreamRestartState": StreamRestartState,
            "CurrentQueueTrackList": CurrentQueueTrackList,
            "CurrentVLIState": CurrentVLIState,
        }

        self.call_action("BecomeGroupCoordinator", arguments=arguments, aspects=aspects)

        return

    def action_BecomeGroupCoordinatorAndSource(self, InstanceID, CurrentCoordinator, CurrentGroupID, OtherMembers, CurrentURI, CurrentURIMetaData, SleepTimerState, AlarmState, StreamRestartState, CurrentAVTTrackList, CurrentQueueTrackList, CurrentSourceState, ResumePlayback, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the BecomeGroupCoordinatorAndSource action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "CurrentCoordinator": CurrentCoordinator,
            "CurrentGroupID": CurrentGroupID,
            "OtherMembers": OtherMembers,
            "CurrentURI": CurrentURI,
            "CurrentURIMetaData": CurrentURIMetaData,
            "SleepTimerState": SleepTimerState,
            "AlarmState": AlarmState,
            "StreamRestartState": StreamRestartState,
            "CurrentAVTTrackList": CurrentAVTTrackList,
            "CurrentQueueTrackList": CurrentQueueTrackList,
            "CurrentSourceState": CurrentSourceState,
            "ResumePlayback": ResumePlayback,
        }

        self.call_action("BecomeGroupCoordinatorAndSource", arguments=arguments, aspects=aspects)

        return

    def action_ChangeCoordinator(self, InstanceID, CurrentCoordinator, NewCoordinator, NewTransportSettings, CurrentAVTransportURI, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ChangeCoordinator action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "CurrentCoordinator": CurrentCoordinator,
            "NewCoordinator": NewCoordinator,
            "NewTransportSettings": NewTransportSettings,
            "CurrentAVTransportURI": CurrentAVTransportURI,
        }

        self.call_action("ChangeCoordinator", arguments=arguments, aspects=aspects)

        return

    def action_ChangeTransportSettings(self, InstanceID, NewTransportSettings, CurrentAVTransportURI, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ChangeTransportSettings action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NewTransportSettings": NewTransportSettings,
            "CurrentAVTransportURI": CurrentAVTransportURI,
        }

        self.call_action("ChangeTransportSettings", arguments=arguments, aspects=aspects)

        return

    def action_ConfigureSleepTimer(self, InstanceID, NewSleepTimerDuration, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ConfigureSleepTimer action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NewSleepTimerDuration": NewSleepTimerDuration,
        }

        self.call_action("ConfigureSleepTimer", arguments=arguments, aspects=aspects)

        return

    def action_CreateSavedQueue(self, InstanceID, Title, EnqueuedURI, EnqueuedURIMetaData, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateSavedQueue action.

            :returns: "NumTracksAdded", "NewQueueLength", "AssignedObjectID", "NewUpdateID"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Title": Title,
            "EnqueuedURI": EnqueuedURI,
            "EnqueuedURIMetaData": EnqueuedURIMetaData,
        }

        out_params = self.call_action("CreateSavedQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NumTracksAdded", "NewQueueLength", "AssignedObjectID", "NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DelegateGroupCoordinationTo(self, InstanceID, NewCoordinator, RejoinGroup, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DelegateGroupCoordinationTo action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NewCoordinator": NewCoordinator,
            "RejoinGroup": RejoinGroup,
        }

        self.call_action("DelegateGroupCoordinationTo", arguments=arguments, aspects=aspects)

        return

    def action_EndDirectControlSession(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the EndDirectControlSession action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("EndDirectControlSession", arguments=arguments, aspects=aspects)

        return

    def action_GetCrossfadeMode(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCrossfadeMode action.

            :returns: "CrossfadeMode"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetCrossfadeMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CrossfadeMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCurrentTransportActions(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCurrentTransportActions action.

            :returns: "Actions"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetCurrentTransportActions", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Actions",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDeviceCapabilities(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDeviceCapabilities action.

            :returns: "PlayMedia", "RecMedia", "RecQualityModes"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetDeviceCapabilities", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PlayMedia", "RecMedia", "RecQualityModes",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMediaInfo(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMediaInfo action.

            :returns: "NrTracks", "MediaDuration", "CurrentURI", "CurrentURIMetaData", "NextURI", "NextURIMetaData", "PlayMedium", "RecordMedium", "WriteStatus"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetMediaInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NrTracks", "MediaDuration", "CurrentURI", "CurrentURIMetaData", "NextURI", "NextURIMetaData", "PlayMedium", "RecordMedium", "WriteStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPositionInfo(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPositionInfo action.

            :returns: "Track", "TrackDuration", "TrackMetaData", "TrackURI", "RelTime", "AbsTime", "RelCount", "AbsCount"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetPositionInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Track", "TrackDuration", "TrackMetaData", "TrackURI", "RelTime", "AbsTime", "RelCount", "AbsCount",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRemainingSleepTimerDuration(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRemainingSleepTimerDuration action.

            :returns: "RemainingSleepTimerDuration", "CurrentSleepTimerGeneration"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetRemainingSleepTimerDuration", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RemainingSleepTimerDuration", "CurrentSleepTimerGeneration",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRunningAlarmProperties(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRunningAlarmProperties action.

            :returns: "AlarmID", "GroupID", "LoggedStartTime"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetRunningAlarmProperties", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AlarmID", "GroupID", "LoggedStartTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTransportInfo(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTransportInfo action.

            :returns: "CurrentTransportState", "CurrentTransportStatus", "CurrentSpeed"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetTransportInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTransportState", "CurrentTransportStatus", "CurrentSpeed",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTransportSettings(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTransportSettings action.

            :returns: "PlayMode", "RecQualityMode"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetTransportSettings", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PlayMode", "RecQualityMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Next(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Next action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Next", arguments=arguments, aspects=aspects)

        return

    def action_NotifyDeletedURI(self, InstanceID, DeletedURI, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the NotifyDeletedURI action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DeletedURI": DeletedURI,
        }

        self.call_action("NotifyDeletedURI", arguments=arguments, aspects=aspects)

        return

    def action_Pause(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Pause action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Pause", arguments=arguments, aspects=aspects)

        return

    def action_Play(self, InstanceID, Speed, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Play action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Speed": Speed,
        }

        self.call_action("Play", arguments=arguments, aspects=aspects)

        return

    def action_Previous(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Previous action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Previous", arguments=arguments, aspects=aspects)

        return

    def action_RemoveAllTracksFromQueue(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveAllTracksFromQueue action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("RemoveAllTracksFromQueue", arguments=arguments, aspects=aspects)

        return

    def action_RemoveTrackFromQueue(self, InstanceID, ObjectID, UpdateID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveTrackFromQueue action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "ObjectID": ObjectID,
            "UpdateID": UpdateID,
        }

        self.call_action("RemoveTrackFromQueue", arguments=arguments, aspects=aspects)

        return

    def action_RemoveTrackRangeFromQueue(self, InstanceID, UpdateID, StartingIndex, NumberOfTracks, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveTrackRangeFromQueue action.

            :returns: "NewUpdateID"
        """
        arguments = {
            "InstanceID": InstanceID,
            "UpdateID": UpdateID,
            "StartingIndex": StartingIndex,
            "NumberOfTracks": NumberOfTracks,
        }

        out_params = self.call_action("RemoveTrackRangeFromQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ReorderTracksInQueue(self, InstanceID, StartingIndex, NumberOfTracks, InsertBefore, UpdateID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ReorderTracksInQueue action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "StartingIndex": StartingIndex,
            "NumberOfTracks": NumberOfTracks,
            "InsertBefore": InsertBefore,
            "UpdateID": UpdateID,
        }

        self.call_action("ReorderTracksInQueue", arguments=arguments, aspects=aspects)

        return

    def action_ReorderTracksInSavedQueue(self, InstanceID, ObjectID, UpdateID, TrackList, NewPositionList, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ReorderTracksInSavedQueue action.

            :returns: "QueueLengthChange", "NewQueueLength", "NewUpdateID"
        """
        arguments = {
            "InstanceID": InstanceID,
            "ObjectID": ObjectID,
            "UpdateID": UpdateID,
            "TrackList": TrackList,
            "NewPositionList": NewPositionList,
        }

        out_params = self.call_action("ReorderTracksInSavedQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("QueueLengthChange", "NewQueueLength", "NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RunAlarm(self, InstanceID, AlarmID, LoggedStartTime, Duration, ProgramURI, ProgramMetaData, PlayMode, Volume, IncludeLinkedZones, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RunAlarm action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "AlarmID": AlarmID,
            "LoggedStartTime": LoggedStartTime,
            "Duration": Duration,
            "ProgramURI": ProgramURI,
            "ProgramMetaData": ProgramMetaData,
            "PlayMode": PlayMode,
            "Volume": Volume,
            "IncludeLinkedZones": IncludeLinkedZones,
        }

        self.call_action("RunAlarm", arguments=arguments, aspects=aspects)

        return

    def action_SaveQueue(self, InstanceID, Title, ObjectID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SaveQueue action.

            :returns: "AssignedObjectID"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Title": Title,
            "ObjectID": ObjectID,
        }

        out_params = self.call_action("SaveQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AssignedObjectID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Seek(self, InstanceID, Unit, Target, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Seek action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Unit": Unit,
            "Target": Target,
        }

        self.call_action("Seek", arguments=arguments, aspects=aspects)

        return

    def action_SetAVTransportURI(self, InstanceID, CurrentURI, CurrentURIMetaData, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAVTransportURI action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "CurrentURI": CurrentURI,
            "CurrentURIMetaData": CurrentURIMetaData,
        }

        self.call_action("SetAVTransportURI", arguments=arguments, aspects=aspects)

        return

    def action_SetCrossfadeMode(self, InstanceID, CrossfadeMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetCrossfadeMode action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "CrossfadeMode": CrossfadeMode,
        }

        self.call_action("SetCrossfadeMode", arguments=arguments, aspects=aspects)

        return

    def action_SetNextAVTransportURI(self, InstanceID, NextURI, NextURIMetaData, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetNextAVTransportURI action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NextURI": NextURI,
            "NextURIMetaData": NextURIMetaData,
        }

        self.call_action("SetNextAVTransportURI", arguments=arguments, aspects=aspects)

        return

    def action_SetPlayMode(self, InstanceID, NewPlayMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetPlayMode action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NewPlayMode": NewPlayMode,
        }

        self.call_action("SetPlayMode", arguments=arguments, aspects=aspects)

        return

    def action_SnoozeAlarm(self, InstanceID, Duration, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SnoozeAlarm action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Duration": Duration,
        }

        self.call_action("SnoozeAlarm", arguments=arguments, aspects=aspects)

        return

    def action_StartAutoplay(self, InstanceID, ProgramURI, ProgramMetaData, Volume, IncludeLinkedZones, ResetVolumeAfter, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartAutoplay action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "ProgramURI": ProgramURI,
            "ProgramMetaData": ProgramMetaData,
            "Volume": Volume,
            "IncludeLinkedZones": IncludeLinkedZones,
            "ResetVolumeAfter": ResetVolumeAfter,
        }

        self.call_action("StartAutoplay", arguments=arguments, aspects=aspects)

        return

    def action_Stop(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Stop action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Stop", arguments=arguments, aspects=aspects)

        return
