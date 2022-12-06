"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class AVTransport1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'AVTransport1' service.
    """

    SERVICE_MANUFACTURER = 'MicrosoftCorporation'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:AVTransport:1'

    SERVICE_EVENT_VARIABLES = {
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

    def action_Next(self, InstanceID, extract_returns=True):
        """
            Calls the Next action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("Next", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Pause(self, InstanceID, extract_returns=True):
        """
            Calls the Pause action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("Pause", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Play(self, InstanceID, Speed, extract_returns=True):
        """
            Calls the Play action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Speed": Speed,
        }

        out_params = self._proxy_call_action("Play", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Previous(self, InstanceID, extract_returns=True):
        """
            Calls the Previous action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("Previous", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Seek(self, InstanceID, Unit, Target, extract_returns=True):
        """
            Calls the Seek action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Unit": Unit,
            "Target": Target,
        }

        out_params = self._proxy_call_action("Seek", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetAVTransportURI(self, InstanceID, CurrentURI, CurrentURIMetaData, extract_returns=True):
        """
            Calls the SetAVTransportURI action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
            "CurrentURI": CurrentURI,
            "CurrentURIMetaData": CurrentURIMetaData,
        }

        out_params = self._proxy_call_action("SetAVTransportURI", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetNextAVTransportURI(self, InstanceID, NextURI, NextURIMetaData, extract_returns=True):
        """
            Calls the SetNextAVTransportURI action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
            "NextURI": NextURI,
            "NextURIMetaData": NextURIMetaData,
        }

        out_params = self._proxy_call_action("SetNextAVTransportURI", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Stop(self, InstanceID, extract_returns=True):
        """
            Calls the Stop action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("Stop", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
