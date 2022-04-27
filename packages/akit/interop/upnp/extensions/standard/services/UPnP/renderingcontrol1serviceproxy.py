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

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RenderingControl:1'

    SERVICE_DEFAULT_VARIABLES = {
        "BlueVideoBlackLevel": { "data_type": "ui2", "default": None, "allowed_list": None},
        "BlueVideoGain": { "data_type": "ui2", "default": None, "allowed_list": None},
        "Brightness": { "data_type": "ui2", "default": None, "allowed_list": None},
        "ColorTemperature": { "data_type": "ui2", "default": None, "allowed_list": None},
        "Contrast": { "data_type": "ui2", "default": None, "allowed_list": None},
        "GreenVideoBlackLevel": { "data_type": "ui2", "default": None, "allowed_list": None},
        "GreenVideoGain": { "data_type": "ui2", "default": None, "allowed_list": None},
        "HorizontalKeystone": { "data_type": "i2", "default": None, "allowed_list": None},
        "Loudness": { "data_type": "boolean", "default": None, "allowed_list": None},
        "Mute": { "data_type": "boolean", "default": None, "allowed_list": None},
        "PresetNameList": { "data_type": "string", "default": None, "allowed_list": None},
        "RedVideoBlackLevel": { "data_type": "ui2", "default": None, "allowed_list": None},
        "RedVideoGain": { "data_type": "ui2", "default": None, "allowed_list": None},
        "Sharpness": { "data_type": "ui2", "default": None, "allowed_list": None},
        "VerticalKeystone": { "data_type": "i2", "default": None, "allowed_list": None},
        "Volume": { "data_type": "ui2", "default": None, "allowed_list": None},
        "VolumeDB": { "data_type": "i2", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_GetBlueVideoBlackLevel(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBlueVideoBlackLevel action.

            :returns: "CurrentBlueVideoBlackLevel"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetBlueVideoBlackLevel", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentBlueVideoBlackLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBlueVideoGain(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBlueVideoGain action.

            :returns: "CurrentBlueVideoGain"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetBlueVideoGain", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentBlueVideoGain",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBrightness(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBrightness action.

            :returns: "CurrentBrightness"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetBrightness", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentBrightness",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetColorTemperature(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetColorTemperature action.

            :returns: "CurrentColorTemperature"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetColorTemperature", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentColorTemperature",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetContrast(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetContrast action.

            :returns: "CurrentContrast"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetContrast", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentContrast",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetGreenVideoBlackLevel(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetGreenVideoBlackLevel action.

            :returns: "CurrentGreenVideoBlackLevel"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetGreenVideoBlackLevel", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentGreenVideoBlackLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetGreenVideoGain(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetGreenVideoGain action.

            :returns: "CurrentGreenVideoGain"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetGreenVideoGain", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentGreenVideoGain",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetHorizontalKeystone(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetHorizontalKeystone action.

            :returns: "CurrentHorizontalKeystone"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetHorizontalKeystone", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentHorizontalKeystone",)]
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

    def action_GetRedVideoBlackLevel(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRedVideoBlackLevel action.

            :returns: "CurrentRedVideoBlackLevel"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetRedVideoBlackLevel", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentRedVideoBlackLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRedVideoGain(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRedVideoGain action.

            :returns: "CurrentRedVideoGain"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetRedVideoGain", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentRedVideoGain",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSharpness(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSharpness action.

            :returns: "CurrentSharpness"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetSharpness", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentSharpness",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVerticalKeystone(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetVerticalKeystone action.

            :returns: "CurrentVerticalKeystone"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetVerticalKeystone", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentVerticalKeystone",)]
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

    def action_ListPresets(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ListPresets action.

            :returns: "CurrentPresetNameList"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("ListPresets", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentPresetNameList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SelectPreset(self, InstanceID, PresetName, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SelectPreset action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "PresetName": PresetName,
        }

        self.call_action("SelectPreset", arguments=arguments, aspects=aspects)

        return

    def action_SetBlueVideoBlackLevel(self, InstanceID, DesiredBlueVideoBlackLevel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetBlueVideoBlackLevel action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredBlueVideoBlackLevel": DesiredBlueVideoBlackLevel,
        }

        self.call_action("SetBlueVideoBlackLevel", arguments=arguments, aspects=aspects)

        return

    def action_SetBlueVideoGain(self, InstanceID, DesiredBlueVideoGain, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetBlueVideoGain action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredBlueVideoGain": DesiredBlueVideoGain,
        }

        self.call_action("SetBlueVideoGain", arguments=arguments, aspects=aspects)

        return

    def action_SetBrightness(self, InstanceID, DesiredBrightness, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetBrightness action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredBrightness": DesiredBrightness,
        }

        self.call_action("SetBrightness", arguments=arguments, aspects=aspects)

        return

    def action_SetColorTemperature(self, InstanceID, DesiredColorTemperature, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetColorTemperature action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredColorTemperature": DesiredColorTemperature,
        }

        self.call_action("SetColorTemperature", arguments=arguments, aspects=aspects)

        return

    def action_SetContrast(self, InstanceID, DesiredContrast, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetContrast action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredContrast": DesiredContrast,
        }

        self.call_action("SetContrast", arguments=arguments, aspects=aspects)

        return

    def action_SetGreenVideoBlackLevel(self, InstanceID, DesiredGreenVideoBlackLevel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetGreenVideoBlackLevel action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredGreenVideoBlackLevel": DesiredGreenVideoBlackLevel,
        }

        self.call_action("SetGreenVideoBlackLevel", arguments=arguments, aspects=aspects)

        return

    def action_SetGreenVideoGain(self, InstanceID, DesiredGreenVideoGain, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetGreenVideoGain action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredGreenVideoGain": DesiredGreenVideoGain,
        }

        self.call_action("SetGreenVideoGain", arguments=arguments, aspects=aspects)

        return

    def action_SetHorizontalKeystone(self, InstanceID, DesiredHorizontalKeystone, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetHorizontalKeystone action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredHorizontalKeystone": DesiredHorizontalKeystone,
        }

        self.call_action("SetHorizontalKeystone", arguments=arguments, aspects=aspects)

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

    def action_SetRedVideoBlackLevel(self, InstanceID, DesiredRedVideoBlackLevel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRedVideoBlackLevel action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredRedVideoBlackLevel": DesiredRedVideoBlackLevel,
        }

        self.call_action("SetRedVideoBlackLevel", arguments=arguments, aspects=aspects)

        return

    def action_SetRedVideoGain(self, InstanceID, DesiredRedVideoGain, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRedVideoGain action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredRedVideoGain": DesiredRedVideoGain,
        }

        self.call_action("SetRedVideoGain", arguments=arguments, aspects=aspects)

        return

    def action_SetSharpness(self, InstanceID, DesiredSharpness, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetSharpness action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredSharpness": DesiredSharpness,
        }

        self.call_action("SetSharpness", arguments=arguments, aspects=aspects)

        return

    def action_SetVerticalKeystone(self, InstanceID, DesiredVerticalKeystone, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetVerticalKeystone action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredVerticalKeystone": DesiredVerticalKeystone,
        }

        self.call_action("SetVerticalKeystone", arguments=arguments, aspects=aspects)

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
