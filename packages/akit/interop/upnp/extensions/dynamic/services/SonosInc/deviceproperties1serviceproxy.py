"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class DeviceProperties1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'DeviceProperties1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:DeviceProperties:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AutoplayIncludeLinkedZones": { "data_type": "boolean", "default": None, "allowed_list": None},
        "AutoplayRoomUUID": { "data_type": "string", "default": None, "allowed_list": None},
        "AutoplaySource": { "data_type": "string", "default": None, "allowed_list": None},
        "AutoplayUseVolume": { "data_type": "boolean", "default": None, "allowed_list": None},
        "AutoplayVolume": { "data_type": "ui2", "default": None, "allowed_list": None},
        "ButtonLockState": { "data_type": "string", "default": None, "allowed_list": "['On', 'Off']"},
        "CopyrightInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "DisplaySoftwareVersion": { "data_type": "string", "default": None, "allowed_list": None},
        "ExtraInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "Flags": { "data_type": "ui4", "default": None, "allowed_list": None},
        "HTAudioIn": { "data_type": "ui4", "default": None, "allowed_list": None},
        "HardwareVersion": { "data_type": "string", "default": None, "allowed_list": None},
        "HouseholdID": { "data_type": "string", "default": None, "allowed_list": None},
        "IPAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "KeepGrouped": { "data_type": "boolean", "default": None, "allowed_list": None},
        "LEDState": { "data_type": "string", "default": None, "allowed_list": "['On', 'Off']"},
        "MACAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "SatRoomUUID": { "data_type": "string", "default": None, "allowed_list": None},
        "SerialNumber": { "data_type": "string", "default": None, "allowed_list": None},
        "SoftwareVersion": { "data_type": "string", "default": None, "allowed_list": None},
        "TargetRoomName": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "AirPlayEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "AvailableRoomCalibration": { "data_type": "string", "default": None, "allowed_list": None},
        "BehindWifiExtender": { "data_type": "ui4", "default": None, "allowed_list": None},
        "ChannelFreq": { "data_type": "ui4", "default": None, "allowed_list": None},
        "ChannelMapSet": { "data_type": "string", "default": None, "allowed_list": None},
        "ConfigMode": { "data_type": "string", "default": None, "allowed_list": None},
        "Configuration": { "data_type": "string", "default": None, "allowed_list": None},
        "HTBondedZoneCommitState": { "data_type": "ui4", "default": None, "allowed_list": None},
        "HTFreq": { "data_type": "ui4", "default": None, "allowed_list": None},
        "HTSatChanMapSet": { "data_type": "string", "default": None, "allowed_list": None},
        "HasConfiguredSSID": { "data_type": "boolean", "default": None, "allowed_list": None},
        "HdmiCecAvailable": { "data_type": "boolean", "default": None, "allowed_list": None},
        "Icon": { "data_type": "string", "default": None, "allowed_list": None},
        "Invisible": { "data_type": "boolean", "default": None, "allowed_list": None},
        "IsIdle": { "data_type": "boolean", "default": None, "allowed_list": None},
        "IsZoneBridge": { "data_type": "boolean", "default": None, "allowed_list": None},
        "LastChangedPlayState": { "data_type": "string", "default": None, "allowed_list": None},
        "MicEnabled": { "data_type": "ui4", "default": None, "allowed_list": None},
        "MoreInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "Orientation": { "data_type": "i4", "default": None, "allowed_list": None},
        "RoomCalibrationState": { "data_type": "i4", "default": None, "allowed_list": None},
        "SecureRegState": { "data_type": "ui4", "default": None, "allowed_list": None},
        "SettingsReplicationState": { "data_type": "string", "default": None, "allowed_list": None},
        "SupportsAudioClip": { "data_type": "boolean", "default": None, "allowed_list": None},
        "SupportsAudioIn": { "data_type": "boolean", "default": None, "allowed_list": None},
        "TVConfigurationError": { "data_type": "boolean", "default": None, "allowed_list": None},
        "VoiceConfigState": { "data_type": "ui4", "default": None, "allowed_list": None},
        "WifiEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "WirelessLeafOnly": { "data_type": "boolean", "default": None, "allowed_list": None},
        "WirelessMode": { "data_type": "ui4", "default": None, "allowed_list": None},
        "ZoneName": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddBondedZones(self, ChannelMapSet, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddBondedZones action.
        """
        arguments = {
            "ChannelMapSet": ChannelMapSet,
        }

        self.call_action("AddBondedZones", arguments=arguments, aspects=aspects)

        return

    def action_AddHTSatellite(self, HTSatChanMapSet, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddHTSatellite action.
        """
        arguments = {
            "HTSatChanMapSet": HTSatChanMapSet,
        }

        self.call_action("AddHTSatellite", arguments=arguments, aspects=aspects)

        return

    def action_CreateStereoPair(self, ChannelMapSet, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateStereoPair action.
        """
        arguments = {
            "ChannelMapSet": ChannelMapSet,
        }

        self.call_action("CreateStereoPair", arguments=arguments, aspects=aspects)

        return

    def action_EnterConfigMode(self, Mode, Options, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the EnterConfigMode action.

            :returns: "State"
        """
        arguments = {
            "Mode": Mode,
            "Options": Options,
        }

        out_params = self.call_action("EnterConfigMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("State",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ExitConfigMode(self, Options, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ExitConfigMode action.
        """
        arguments = {
            "Options": Options,
        }

        self.call_action("ExitConfigMode", arguments=arguments, aspects=aspects)

        return

    def action_GetAutoplayLinkedZones(self, Source, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAutoplayLinkedZones action.

            :returns: "IncludeLinkedZones"
        """
        arguments = {
            "Source": Source,
        }

        out_params = self.call_action("GetAutoplayLinkedZones", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("IncludeLinkedZones",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAutoplayRoomUUID(self, Source, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAutoplayRoomUUID action.

            :returns: "RoomUUID"
        """
        arguments = {
            "Source": Source,
        }

        out_params = self.call_action("GetAutoplayRoomUUID", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RoomUUID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAutoplayVolume(self, Source, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAutoplayVolume action.

            :returns: "CurrentVolume"
        """
        arguments = {
            "Source": Source,
        }

        out_params = self.call_action("GetAutoplayVolume", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetButtonLockState(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetButtonLockState action.

            :returns: "CurrentButtonLockState"
        """
        arguments = { }

        out_params = self.call_action("GetButtonLockState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentButtonLockState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetButtonState(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetButtonState action.

            :returns: "State"
        """
        arguments = { }

        out_params = self.call_action("GetButtonState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("State",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetHouseholdID(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetHouseholdID action.

            :returns: "CurrentHouseholdID"
        """
        arguments = { }

        out_params = self.call_action("GetHouseholdID", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentHouseholdID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLEDState(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLEDState action.

            :returns: "CurrentLEDState"
        """
        arguments = { }

        out_params = self.call_action("GetLEDState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentLEDState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetUseAutoplayVolume(self, Source, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetUseAutoplayVolume action.

            :returns: "UseVolume"
        """
        arguments = {
            "Source": Source,
        }

        out_params = self.call_action("GetUseAutoplayVolume", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("UseVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetZoneAttributes(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetZoneAttributes action.

            :returns: "CurrentZoneName", "CurrentIcon", "CurrentConfiguration", "CurrentTargetRoomName"
        """
        arguments = { }

        out_params = self.call_action("GetZoneAttributes", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentZoneName", "CurrentIcon", "CurrentConfiguration", "CurrentTargetRoomName",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetZoneInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetZoneInfo action.

            :returns: "SerialNumber", "SoftwareVersion", "DisplaySoftwareVersion", "HardwareVersion", "IPAddress", "MACAddress", "CopyrightInfo", "ExtraInfo", "HTAudioIn", "Flags"
        """
        arguments = { }

        out_params = self.call_action("GetZoneInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SerialNumber", "SoftwareVersion", "DisplaySoftwareVersion", "HardwareVersion", "IPAddress", "MACAddress", "CopyrightInfo", "ExtraInfo", "HTAudioIn", "Flags",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RemoveBondedZones(self, ChannelMapSet, KeepGrouped, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveBondedZones action.
        """
        arguments = {
            "ChannelMapSet": ChannelMapSet,
            "KeepGrouped": KeepGrouped,
        }

        self.call_action("RemoveBondedZones", arguments=arguments, aspects=aspects)

        return

    def action_RemoveHTSatellite(self, SatRoomUUID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveHTSatellite action.
        """
        arguments = {
            "SatRoomUUID": SatRoomUUID,
        }

        self.call_action("RemoveHTSatellite", arguments=arguments, aspects=aspects)

        return

    def action_RoomDetectionStartChirping(self, Channel, DurationMilliseconds, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RoomDetectionStartChirping action.

            :returns: "PlayId", "ChirpIfPlayingSwappableAudio"
        """
        arguments = {
            "Channel": Channel,
            "DurationMilliseconds": DurationMilliseconds,
        }

        out_params = self.call_action("RoomDetectionStartChirping", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PlayId", "ChirpIfPlayingSwappableAudio",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RoomDetectionStopChirping(self, PlayId, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RoomDetectionStopChirping action.
        """
        arguments = {
            "PlayId": PlayId,
        }

        self.call_action("RoomDetectionStopChirping", arguments=arguments, aspects=aspects)

        return

    def action_SeparateStereoPair(self, ChannelMapSet, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SeparateStereoPair action.
        """
        arguments = {
            "ChannelMapSet": ChannelMapSet,
        }

        self.call_action("SeparateStereoPair", arguments=arguments, aspects=aspects)

        return

    def action_SetAutoplayLinkedZones(self, IncludeLinkedZones, Source, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAutoplayLinkedZones action.
        """
        arguments = {
            "IncludeLinkedZones": IncludeLinkedZones,
            "Source": Source,
        }

        self.call_action("SetAutoplayLinkedZones", arguments=arguments, aspects=aspects)

        return

    def action_SetAutoplayRoomUUID(self, RoomUUID, Source, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAutoplayRoomUUID action.
        """
        arguments = {
            "RoomUUID": RoomUUID,
            "Source": Source,
        }

        self.call_action("SetAutoplayRoomUUID", arguments=arguments, aspects=aspects)

        return

    def action_SetAutoplayVolume(self, Volume, Source, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAutoplayVolume action.
        """
        arguments = {
            "Volume": Volume,
            "Source": Source,
        }

        self.call_action("SetAutoplayVolume", arguments=arguments, aspects=aspects)

        return

    def action_SetButtonLockState(self, DesiredButtonLockState, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetButtonLockState action.
        """
        arguments = {
            "DesiredButtonLockState": DesiredButtonLockState,
        }

        self.call_action("SetButtonLockState", arguments=arguments, aspects=aspects)

        return

    def action_SetLEDState(self, DesiredLEDState, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetLEDState action.
        """
        arguments = {
            "DesiredLEDState": DesiredLEDState,
        }

        self.call_action("SetLEDState", arguments=arguments, aspects=aspects)

        return

    def action_SetUseAutoplayVolume(self, UseVolume, Source, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetUseAutoplayVolume action.
        """
        arguments = {
            "UseVolume": UseVolume,
            "Source": Source,
        }

        self.call_action("SetUseAutoplayVolume", arguments=arguments, aspects=aspects)

        return

    def action_SetZoneAttributes(self, DesiredZoneName, DesiredIcon, DesiredConfiguration, DesiredTargetRoomName, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetZoneAttributes action.
        """
        arguments = {
            "DesiredZoneName": DesiredZoneName,
            "DesiredIcon": DesiredIcon,
            "DesiredConfiguration": DesiredConfiguration,
            "DesiredTargetRoomName": DesiredTargetRoomName,
        }

        self.call_action("SetZoneAttributes", arguments=arguments, aspects=aspects)

        return
