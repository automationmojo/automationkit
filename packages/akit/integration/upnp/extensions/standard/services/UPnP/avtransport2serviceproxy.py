"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class AVTransport2ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'AVTransport2' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:AVTransport:2'

    SERVICE_EVENT_VARIABLES = {
        "DRMState": { "data_type": "string", "default": "UNKNOWN", "allowed_list": "['OK']"},
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_GetCurrentTransportActions(self, InstanceID, extract_returns=True):
        """
            Calls the GetCurrentTransportActions action.

            :returns: "Actions"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetCurrentTransportActions", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Actions",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDRMState(self, InstanceID, extract_returns=True):
        """
            Calls the GetDRMState action.

            :returns: "CurrentDRMState"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetDRMState", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentDRMState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDeviceCapabilities(self, InstanceID, extract_returns=True):
        """
            Calls the GetDeviceCapabilities action.

            :returns: "PlayMedia", "RecMedia", "RecQualityModes"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetDeviceCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PlayMedia", "RecMedia", "RecQualityModes",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMediaInfo(self, InstanceID, extract_returns=True):
        """
            Calls the GetMediaInfo action.

            :returns: "NrTracks", "MediaDuration", "CurrentURI", "CurrentURIMetaData", "NextURI", "NextURIMetaData", "PlayMedium", "RecordMedium", "WriteStatus"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetMediaInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NrTracks", "MediaDuration", "CurrentURI", "CurrentURIMetaData", "NextURI", "NextURIMetaData", "PlayMedium", "RecordMedium", "WriteStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMediaInfo_Ext(self, InstanceID, extract_returns=True):
        """
            Calls the GetMediaInfo_Ext action.

            :returns: "CurrentType", "NrTracks", "MediaDuration", "CurrentURI", "CurrentURIMetaData", "NextURI", "NextURIMetaData", "PlayMedium", "RecordMedium", "WriteStatus"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetMediaInfo_Ext", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentType", "NrTracks", "MediaDuration", "CurrentURI", "CurrentURIMetaData", "NextURI", "NextURIMetaData", "PlayMedium", "RecordMedium", "WriteStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPositionInfo(self, InstanceID, extract_returns=True):
        """
            Calls the GetPositionInfo action.

            :returns: "Track", "TrackDuration", "TrackMetaData", "TrackURI", "RelTime", "AbsTime", "RelCount", "AbsCount"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetPositionInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Track", "TrackDuration", "TrackMetaData", "TrackURI", "RelTime", "AbsTime", "RelCount", "AbsCount",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetStateVariables(self, InstanceID, StateVariableList, extract_returns=True):
        """
            Calls the GetStateVariables action.

            :returns: "StateVariableValuePairs"
        """
        arguments = {
            "InstanceID": InstanceID,
            "StateVariableList": StateVariableList,
        }

        out_params = self._proxy_call_action("GetStateVariables", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableValuePairs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTransportInfo(self, InstanceID, extract_returns=True):
        """
            Calls the GetTransportInfo action.

            :returns: "CurrentTransportState", "CurrentTransportStatus", "CurrentSpeed"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetTransportInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTransportState", "CurrentTransportStatus", "CurrentSpeed",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTransportSettings(self, InstanceID, extract_returns=True):
        """
            Calls the GetTransportSettings action.

            :returns: "PlayMode", "RecQualityMode"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetTransportSettings", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PlayMode", "RecQualityMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Next(self, InstanceID):
        """
            Calls the Next action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self._proxy_call_action("Next", arguments=arguments)

        return

    def action_Pause(self, InstanceID):
        """
            Calls the Pause action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self._proxy_call_action("Pause", arguments=arguments)

        return

    def action_Play(self, InstanceID, Speed):
        """
            Calls the Play action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Speed": Speed,
        }

        self._proxy_call_action("Play", arguments=arguments)

        return

    def action_Previous(self, InstanceID):
        """
            Calls the Previous action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self._proxy_call_action("Previous", arguments=arguments)

        return

    def action_Record(self, InstanceID):
        """
            Calls the Record action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self._proxy_call_action("Record", arguments=arguments)

        return

    def action_Seek(self, InstanceID, Unit, Target):
        """
            Calls the Seek action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Unit": Unit,
            "Target": Target,
        }

        self._proxy_call_action("Seek", arguments=arguments)

        return

    def action_SetAVTransportURI(self, InstanceID, CurrentURI, CurrentURIMetaData):
        """
            Calls the SetAVTransportURI action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "CurrentURI": CurrentURI,
            "CurrentURIMetaData": CurrentURIMetaData,
        }

        self._proxy_call_action("SetAVTransportURI", arguments=arguments)

        return

    def action_SetNextAVTransportURI(self, InstanceID, NextURI, NextURIMetaData):
        """
            Calls the SetNextAVTransportURI action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NextURI": NextURI,
            "NextURIMetaData": NextURIMetaData,
        }

        self._proxy_call_action("SetNextAVTransportURI", arguments=arguments)

        return

    def action_SetPlayMode(self, InstanceID, NewPlayMode):
        """
            Calls the SetPlayMode action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NewPlayMode": NewPlayMode,
        }

        self._proxy_call_action("SetPlayMode", arguments=arguments)

        return

    def action_SetRecordQualityMode(self, InstanceID, NewRecordQualityMode):
        """
            Calls the SetRecordQualityMode action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "NewRecordQualityMode": NewRecordQualityMode,
        }

        self._proxy_call_action("SetRecordQualityMode", arguments=arguments)

        return

    def action_SetStateVariables(self, InstanceID, AVTransportUDN, ServiceType, ServiceId, StateVariableValuePairs, extract_returns=True):
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

        out_params = self._proxy_call_action("SetStateVariables", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StateVariableList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Stop(self, InstanceID):
        """
            Calls the Stop action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self._proxy_call_action("Stop", arguments=arguments)

        return
