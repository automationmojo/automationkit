"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class AVTransport3ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'AVTransport3' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:AVTransport:3'

    SERVICE_DEFAULT_VARIABLES = {
        "AVTransportURI": { "data_type": "string", "default": None, "allowed_list": None},
        "AVTransportURIMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "AbsoluteCounterPosition": { "data_type": "ui4", "default": None, "allowed_list": None},
        "AbsoluteTimePosition": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentMediaCategory": { "data_type": "string", "default": None, "allowed_list": "['NO_MEDIA', 'TRACK_AWARE', 'TRACK_UNAWARE']"},
        "CurrentMediaDuration": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentPlayMode": { "data_type": "string", "default": "NORMAL", "allowed_list": "['NORMAL']"},
        "CurrentRecordQualityMode": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTrack": { "data_type": "ui4", "default": None, "allowed_list": None},
        "CurrentTrackDuration": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTrackMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTrackURI": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTransportActions": { "data_type": "string", "default": None, "allowed_list": None},
        "DRMState": { "data_type": "string", "default": "UNKNOWN", "allowed_list": "['OK']"},
        "NextAVTransportURI": { "data_type": "string", "default": None, "allowed_list": None},
        "NextAVTransportURIMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "NumberOfTracks": { "data_type": "ui4", "default": None, "allowed_list": None},
        "PlaybackStorageMedium": { "data_type": "string", "default": None, "allowed_list": None},
        "PossiblePlaybackStorageMedia": { "data_type": "string", "default": None, "allowed_list": None},
        "PossibleRecordQualityModes": { "data_type": "string", "default": None, "allowed_list": None},
        "PossibleRecordStorageMedia": { "data_type": "string", "default": None, "allowed_list": None},
        "RecordMediumWriteStatus": { "data_type": "string", "default": None, "allowed_list": None},
        "RecordStorageMedium": { "data_type": "string", "default": None, "allowed_list": None},
        "RelativeCounterPosition": { "data_type": "i4", "default": None, "allowed_list": None},
        "RelativeTimePosition": { "data_type": "string", "default": None, "allowed_list": None},
        "SyncOffset": { "data_type": "string", "default": None, "allowed_list": None},
        "TransportPlaySpeed": { "data_type": "string", "default": None, "allowed_list": "['1']"},
        "TransportState": { "data_type": "string", "default": None, "allowed_list": "['STOPPED', 'PLAYING']"},
        "TransportStatus": { "data_type": "string", "default": None, "allowed_list": "['OK', 'ERROR_OCCURRED']"},
    }

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AdjustSyncOffset(self, InstanceID, Adjustment, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AdjustSyncOffset action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Adjustment": Adjustment,
        }

        self.call_action("AdjustSyncOffset", arguments=arguments, aspects=aspects)

        return

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

    def action_GetDRMState(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDRMState action.

            :returns: "CurrentDRMState"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetDRMState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentDRMState",)]
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

    def action_GetMediaInfo_Ext(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMediaInfo_Ext action.

            :returns: "CurrentType", "NrTracks", "MediaDuration", "CurrentURI", "CurrentURIMetaData", "NextURI", "NextURIMetaData", "PlayMedium", "RecordMedium", "WriteStatus"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetMediaInfo_Ext", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentType", "NrTracks", "MediaDuration", "CurrentURI", "CurrentURIMetaData", "NextURI", "NextURIMetaData", "PlayMedium", "RecordMedium", "WriteStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPlaylistInfo(self, InstanceID, PlaylistType, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPlaylistInfo action.

            :returns: "PlaylistInfo"
        """
        arguments = {
            "InstanceID": InstanceID,
            "PlaylistType": PlaylistType,
        }

        out_params = self.call_action("GetPlaylistInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PlaylistInfo",)]
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

    def action_GetStateVariables(self, InstanceID, StateVariableList, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetStateVariables action.

            :returns: "StateVariableValuePairs"
        """
        arguments = {
            "InstanceID": InstanceID,
            "StateVariableList": StateVariableList,
        }

        out_params = self.call_action("GetStateVariables", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableValuePairs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSyncOffset(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSyncOffset action.

            :returns: "CurrentSyncOffset"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetSyncOffset", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentSyncOffset",)]
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

    def action_Record(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Record action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Record", arguments=arguments, aspects=aspects)

        return

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

    def action_SetRecordQualityMode(self, InstanceID, NewRecordQualityMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRecordQualityMode action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NewRecordQualityMode": NewRecordQualityMode,
        }

        self.call_action("SetRecordQualityMode", arguments=arguments, aspects=aspects)

        return

    def action_SetStateVariables(self, InstanceID, AVTransportUDN, ServiceType, ServiceId, StateVariableValuePairs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetStateVariables action.

            :returns: "StateVariableList"
        """
        arguments = {
            "InstanceID": InstanceID,
            "AVTransportUDN": AVTransportUDN,
            "ServiceType": ServiceType,
            "ServiceId": ServiceId,
            "StateVariableValuePairs": StateVariableValuePairs,
        }

        out_params = self.call_action("SetStateVariables", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetStaticPlaylist(self, InstanceID, PlaylistData, PlaylistDataLength, PlaylistOffset, PlaylistTotalLength, PlaylistMIMEType, PlaylistExtendedType, PlaylistStartObj, PlaylistStartGroup, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetStaticPlaylist action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "PlaylistData": PlaylistData,
            "PlaylistDataLength": PlaylistDataLength,
            "PlaylistOffset": PlaylistOffset,
            "PlaylistTotalLength": PlaylistTotalLength,
            "PlaylistMIMEType": PlaylistMIMEType,
            "PlaylistExtendedType": PlaylistExtendedType,
            "PlaylistStartObj": PlaylistStartObj,
            "PlaylistStartGroup": PlaylistStartGroup,
        }

        self.call_action("SetStaticPlaylist", arguments=arguments, aspects=aspects)

        return

    def action_SetStreamingPlaylist(self, InstanceID, PlaylistData, PlaylistDataLength, PlaylistMIMEType, PlaylistExtendedType, PlaylistStep, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetStreamingPlaylist action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "PlaylistData": PlaylistData,
            "PlaylistDataLength": PlaylistDataLength,
            "PlaylistMIMEType": PlaylistMIMEType,
            "PlaylistExtendedType": PlaylistExtendedType,
            "PlaylistStep": PlaylistStep,
        }

        self.call_action("SetStreamingPlaylist", arguments=arguments, aspects=aspects)

        return

    def action_SetSyncOffset(self, InstanceID, NewSyncOffset, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetSyncOffset action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NewSyncOffset": NewSyncOffset,
        }

        self.call_action("SetSyncOffset", arguments=arguments, aspects=aspects)

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

    def action_SyncPause(self, InstanceID, PauseTime, ReferenceClockId, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SyncPause action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "PauseTime": PauseTime,
            "ReferenceClockId": ReferenceClockId,
        }

        self.call_action("SyncPause", arguments=arguments, aspects=aspects)

        return

    def action_SyncPlay(self, InstanceID, Speed, ReferencePositionUnits, ReferencePosition, ReferencePresentationTime, ReferenceClockId, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SyncPlay action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Speed": Speed,
            "ReferencePositionUnits": ReferencePositionUnits,
            "ReferencePosition": ReferencePosition,
            "ReferencePresentationTime": ReferencePresentationTime,
            "ReferenceClockId": ReferenceClockId,
        }

        self.call_action("SyncPlay", arguments=arguments, aspects=aspects)

        return

    def action_SyncStop(self, InstanceID, StopTime, ReferenceClockId, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SyncStop action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "StopTime": StopTime,
            "ReferenceClockId": ReferenceClockId,
        }

        self.call_action("SyncStop", arguments=arguments, aspects=aspects)

        return
