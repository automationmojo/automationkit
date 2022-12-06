"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RenderingControl1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RenderingControl1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RenderingControl:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AudioDelay": { "data_type": "string", "default": None, "allowed_list": None},
        "AudioDelayLeftRear": { "data_type": "string", "default": None, "allowed_list": None},
        "AudioDelayRightRear": { "data_type": "string", "default": None, "allowed_list": None},
        "Bass": { "data_type": "i2", "default": None, "allowed_list": None},
        "DialogLevel": { "data_type": "string", "default": None, "allowed_list": None},
        "EQValue": { "data_type": "i2", "default": None, "allowed_list": None},
        "HeadphoneConnected": { "data_type": "boolean", "default": None, "allowed_list": None},
        "Loudness": { "data_type": "boolean", "default": None, "allowed_list": None},
        "MusicSurroundLevel": { "data_type": "string", "default": None, "allowed_list": None},
        "Mute": { "data_type": "boolean", "default": None, "allowed_list": None},
        "NightMode": { "data_type": "boolean", "default": None, "allowed_list": None},
        "OutputFixed": { "data_type": "boolean", "default": None, "allowed_list": None},
        "PresetNameList": { "data_type": "string", "default": None, "allowed_list": None},
        "RoomCalibrationAvailable": { "data_type": "boolean", "default": None, "allowed_list": None},
        "RoomCalibrationCalibrationMode": { "data_type": "string", "default": None, "allowed_list": None},
        "RoomCalibrationCoefficients": { "data_type": "string", "default": None, "allowed_list": None},
        "RoomCalibrationEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "RoomCalibrationID": { "data_type": "string", "default": None, "allowed_list": None},
        "SpeakerSize": { "data_type": "ui4", "default": None, "allowed_list": None},
        "SubCrossover": { "data_type": "string", "default": None, "allowed_list": None},
        "SubEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "SubGain": { "data_type": "string", "default": None, "allowed_list": None},
        "SubPolarity": { "data_type": "string", "default": None, "allowed_list": None},
        "SupportsOutputFixed": { "data_type": "boolean", "default": None, "allowed_list": None},
        "SurroundEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "SurroundLevel": { "data_type": "string", "default": None, "allowed_list": None},
        "SurroundMode": { "data_type": "string", "default": None, "allowed_list": None},
        "Treble": { "data_type": "i2", "default": None, "allowed_list": None},
        "Volume": { "data_type": "ui2", "default": None, "allowed_list": None},
        "VolumeDB": { "data_type": "i2", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_GetBass(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBass action.

            :returns: "CurrentBass"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetBass", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentBass",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetEQ(self, InstanceID, EQType, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetEQ action.

            :returns: "CurrentValue"
        """
        arguments = {
            "InstanceID": InstanceID,
            "EQType": EQType,
        }

        out_params = self.call_action("GetEQ", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetHeadphoneConnected(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetHeadphoneConnected action.

            :returns: "CurrentHeadphoneConnected"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetHeadphoneConnected", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentHeadphoneConnected",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLoudness(self, InstanceID, Channel, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLoudness action.

            :returns: "CurrentLoudness"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self.call_action("GetLoudness", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentLoudness",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMute(self, InstanceID, Channel, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMute action.

            :returns: "CurrentMute"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self.call_action("GetMute", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentMute",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOutputFixed(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetOutputFixed action.

            :returns: "CurrentFixed"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetOutputFixed", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentFixed",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRoomCalibrationStatus(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRoomCalibrationStatus action.

            :returns: "RoomCalibrationEnabled", "RoomCalibrationAvailable"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetRoomCalibrationStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RoomCalibrationEnabled", "RoomCalibrationAvailable",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSupportsOutputFixed(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSupportsOutputFixed action.

            :returns: "CurrentSupportsFixed"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetSupportsOutputFixed", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentSupportsFixed",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTreble(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTreble action.

            :returns: "CurrentTreble"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetTreble", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTreble",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVolume(self, InstanceID, Channel, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetVolume action.

            :returns: "CurrentVolume"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self.call_action("GetVolume", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVolumeDB(self, InstanceID, Channel, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetVolumeDB action.

            :returns: "CurrentVolume"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self.call_action("GetVolumeDB", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVolumeDBRange(self, InstanceID, Channel, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetVolumeDBRange action.

            :returns: "MinValue", "MaxValue"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self.call_action("GetVolumeDBRange", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MinValue", "MaxValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RampToVolume(self, InstanceID, Channel, RampType, DesiredVolume, ResetVolumeAfter, ProgramURI, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RampToVolume action.

            :returns: "RampTime"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "RampType": RampType,
            "DesiredVolume": DesiredVolume,
            "ResetVolumeAfter": ResetVolumeAfter,
            "ProgramURI": ProgramURI,
        }

        out_params = self.call_action("RampToVolume", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RampTime",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetBasicEQ(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ResetBasicEQ action.

            :returns: "Bass", "Treble", "Loudness", "LeftVolume", "RightVolume"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("ResetBasicEQ", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Bass", "Treble", "Loudness", "LeftVolume", "RightVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetExtEQ(self, InstanceID, EQType, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ResetExtEQ action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "EQType": EQType,
        }

        self.call_action("ResetExtEQ", arguments=arguments, aspects=aspects)

        return

    def action_RestoreVolumePriorToRamp(self, InstanceID, Channel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RestoreVolumePriorToRamp action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        self.call_action("RestoreVolumePriorToRamp", arguments=arguments, aspects=aspects)

        return

    def action_SetBass(self, InstanceID, DesiredBass, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetBass action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredBass": DesiredBass,
        }

        self.call_action("SetBass", arguments=arguments, aspects=aspects)

        return

    def action_SetChannelMap(self, InstanceID, ChannelMap, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetChannelMap action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "ChannelMap": ChannelMap,
        }

        self.call_action("SetChannelMap", arguments=arguments, aspects=aspects)

        return

    def action_SetEQ(self, InstanceID, EQType, DesiredValue, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetEQ action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "EQType": EQType,
            "DesiredValue": DesiredValue,
        }

        self.call_action("SetEQ", arguments=arguments, aspects=aspects)

        return

    def action_SetLoudness(self, InstanceID, Channel, DesiredLoudness, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetLoudness action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredLoudness": DesiredLoudness,
        }

        self.call_action("SetLoudness", arguments=arguments, aspects=aspects)

        return

    def action_SetMute(self, InstanceID, Channel, DesiredMute, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetMute action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredMute": DesiredMute,
        }

        self.call_action("SetMute", arguments=arguments, aspects=aspects)

        return

    def action_SetOutputFixed(self, InstanceID, DesiredFixed, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetOutputFixed action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredFixed": DesiredFixed,
        }

        self.call_action("SetOutputFixed", arguments=arguments, aspects=aspects)

        return

    def action_SetRelativeVolume(self, InstanceID, Channel, Adjustment, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRelativeVolume action.

            :returns: "NewVolume"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "Adjustment": Adjustment,
        }

        out_params = self.call_action("SetRelativeVolume", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetRoomCalibrationStatus(self, InstanceID, RoomCalibrationEnabled, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRoomCalibrationStatus action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "RoomCalibrationEnabled": RoomCalibrationEnabled,
        }

        self.call_action("SetRoomCalibrationStatus", arguments=arguments, aspects=aspects)

        return

    def action_SetRoomCalibrationX(self, InstanceID, CalibrationID, Coefficients, CalibrationMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRoomCalibrationX action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "CalibrationID": CalibrationID,
            "Coefficients": Coefficients,
            "CalibrationMode": CalibrationMode,
        }

        self.call_action("SetRoomCalibrationX", arguments=arguments, aspects=aspects)

        return

    def action_SetTreble(self, InstanceID, DesiredTreble, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetTreble action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredTreble": DesiredTreble,
        }

        self.call_action("SetTreble", arguments=arguments, aspects=aspects)

        return

    def action_SetVolume(self, InstanceID, Channel, DesiredVolume, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetVolume action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredVolume": DesiredVolume,
        }

        self.call_action("SetVolume", arguments=arguments, aspects=aspects)

        return

    def action_SetVolumeDB(self, InstanceID, Channel, DesiredVolume, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetVolumeDB action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredVolume": DesiredVolume,
        }

        self.call_action("SetVolumeDB", arguments=arguments, aspects=aspects)

        return
