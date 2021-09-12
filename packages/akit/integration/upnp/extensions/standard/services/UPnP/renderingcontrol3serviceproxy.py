"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RenderingControl3ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RenderingControl3' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RenderingControl:3'

    SERVICE_EVENT_VARIABLES = {
        "AllowedDefaultTransformSettings": { "data_type": "string", "default": None, "allowed_list": None},
        "DefaultTransformSettings": { "data_type": "string", "default": None, "allowed_list": None},
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_GetAllAvailableTransforms(self, extract_returns=True):
        """
            Calls the GetAllAvailableTransforms action.

            :returns: "AllAllowedTransformSettings"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetAllAvailableTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AllAllowedTransformSettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAllowedDefaultTransforms(self, extract_returns=True):
        """
            Calls the GetAllowedDefaultTransforms action.

            :returns: "AllowedDefaultTransformSettings"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetAllowedDefaultTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AllowedDefaultTransformSettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAllowedTransforms(self, InstanceID, extract_returns=True):
        """
            Calls the GetAllowedTransforms action.

            :returns: "CurrentAllowedTransformSettings"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetAllowedTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentAllowedTransformSettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBlueVideoBlackLevel(self, InstanceID, extract_returns=True):
        """
            Calls the GetBlueVideoBlackLevel action.

            :returns: "CurrentBlueVideoBlackLevel"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetBlueVideoBlackLevel", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentBlueVideoBlackLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBlueVideoGain(self, InstanceID, extract_returns=True):
        """
            Calls the GetBlueVideoGain action.

            :returns: "CurrentBlueVideoGain"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetBlueVideoGain", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentBlueVideoGain",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBrightness(self, InstanceID, extract_returns=True):
        """
            Calls the GetBrightness action.

            :returns: "CurrentBrightness"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetBrightness", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentBrightness",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetColorTemperature(self, InstanceID, extract_returns=True):
        """
            Calls the GetColorTemperature action.

            :returns: "CurrentColorTemperature"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetColorTemperature", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentColorTemperature",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetContrast(self, InstanceID, extract_returns=True):
        """
            Calls the GetContrast action.

            :returns: "CurrentContrast"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetContrast", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentContrast",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultTransforms(self, extract_returns=True):
        """
            Calls the GetDefaultTransforms action.

            :returns: "CurrentDefaultTransformSettings"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetDefaultTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentDefaultTransformSettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetGreenVideoBlackLevel(self, InstanceID, extract_returns=True):
        """
            Calls the GetGreenVideoBlackLevel action.

            :returns: "CurrentGreenVideoBlackLevel"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetGreenVideoBlackLevel", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentGreenVideoBlackLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetGreenVideoGain(self, InstanceID, extract_returns=True):
        """
            Calls the GetGreenVideoGain action.

            :returns: "CurrentGreenVideoGain"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetGreenVideoGain", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentGreenVideoGain",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetHorizontalKeystone(self, InstanceID, extract_returns=True):
        """
            Calls the GetHorizontalKeystone action.

            :returns: "CurrentHorizontalKeystone"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetHorizontalKeystone", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentHorizontalKeystone",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLoudness(self, InstanceID, Channel, extract_returns=True):
        """
            Calls the GetLoudness action.

            :returns: "CurrentLoudness"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self._proxy_call_action("GetLoudness", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentLoudness",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMute(self, InstanceID, Channel, extract_returns=True):
        """
            Calls the GetMute action.

            :returns: "CurrentMute"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self._proxy_call_action("GetMute", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentMute",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRedVideoBlackLevel(self, InstanceID, extract_returns=True):
        """
            Calls the GetRedVideoBlackLevel action.

            :returns: "CurrentRedVideoBlackLevel"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetRedVideoBlackLevel", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentRedVideoBlackLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRedVideoGain(self, InstanceID, extract_returns=True):
        """
            Calls the GetRedVideoGain action.

            :returns: "CurrentRedVideoGain"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetRedVideoGain", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentRedVideoGain",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSharpness(self, InstanceID, extract_returns=True):
        """
            Calls the GetSharpness action.

            :returns: "CurrentSharpness"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetSharpness", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentSharpness",)]
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

    def action_GetTransforms(self, InstanceID, extract_returns=True):
        """
            Calls the GetTransforms action.

            :returns: "CurrentTransformValues"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetTransforms", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTransformValues",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVerticalKeystone(self, InstanceID, extract_returns=True):
        """
            Calls the GetVerticalKeystone action.

            :returns: "CurrentVerticalKeystone"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("GetVerticalKeystone", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentVerticalKeystone",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVolume(self, InstanceID, Channel, extract_returns=True):
        """
            Calls the GetVolume action.

            :returns: "CurrentVolume"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self._proxy_call_action("GetVolume", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVolumeDB(self, InstanceID, Channel, extract_returns=True):
        """
            Calls the GetVolumeDB action.

            :returns: "CurrentVolume"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self._proxy_call_action("GetVolumeDB", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetVolumeDBRange(self, InstanceID, Channel, extract_returns=True):
        """
            Calls the GetVolumeDBRange action.

            :returns: "MinValue", "MaxValue"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
        }

        out_params = self._proxy_call_action("GetVolumeDBRange", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MinValue", "MaxValue",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ListPresets(self, InstanceID, extract_returns=True):
        """
            Calls the ListPresets action.

            :returns: "CurrentPresetNameList"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self._proxy_call_action("ListPresets", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentPresetNameList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SelectPreset(self, InstanceID, PresetName):
        """
            Calls the SelectPreset action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "PresetName": PresetName,
        }

        self._proxy_call_action("SelectPreset", arguments=arguments)

        return

    def action_SetBlueVideoBlackLevel(self, InstanceID, DesiredBlueVideoBlackLevel):
        """
            Calls the SetBlueVideoBlackLevel action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredBlueVideoBlackLevel": DesiredBlueVideoBlackLevel,
        }

        self._proxy_call_action("SetBlueVideoBlackLevel", arguments=arguments)

        return

    def action_SetBlueVideoGain(self, InstanceID, DesiredBlueVideoGain):
        """
            Calls the SetBlueVideoGain action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredBlueVideoGain": DesiredBlueVideoGain,
        }

        self._proxy_call_action("SetBlueVideoGain", arguments=arguments)

        return

    def action_SetBrightness(self, InstanceID, DesiredBrightness):
        """
            Calls the SetBrightness action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredBrightness": DesiredBrightness,
        }

        self._proxy_call_action("SetBrightness", arguments=arguments)

        return

    def action_SetColorTemperature(self, InstanceID, DesiredColorTemperature):
        """
            Calls the SetColorTemperature action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredColorTemperature": DesiredColorTemperature,
        }

        self._proxy_call_action("SetColorTemperature", arguments=arguments)

        return

    def action_SetContrast(self, InstanceID, DesiredContrast):
        """
            Calls the SetContrast action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredContrast": DesiredContrast,
        }

        self._proxy_call_action("SetContrast", arguments=arguments)

        return

    def action_SetDefaultTransforms(self, DesiredDefaultTransformSettings):
        """
            Calls the SetDefaultTransforms action.
        """
        arguments = {
            "DesiredDefaultTransformSettings": DesiredDefaultTransformSettings,
        }

        self._proxy_call_action("SetDefaultTransforms", arguments=arguments)

        return

    def action_SetGreenVideoBlackLevel(self, InstanceID, DesiredGreenVideoBlackLevel):
        """
            Calls the SetGreenVideoBlackLevel action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredGreenVideoBlackLevel": DesiredGreenVideoBlackLevel,
        }

        self._proxy_call_action("SetGreenVideoBlackLevel", arguments=arguments)

        return

    def action_SetGreenVideoGain(self, InstanceID, DesiredGreenVideoGain):
        """
            Calls the SetGreenVideoGain action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredGreenVideoGain": DesiredGreenVideoGain,
        }

        self._proxy_call_action("SetGreenVideoGain", arguments=arguments)

        return

    def action_SetHorizontalKeystone(self, InstanceID, DesiredHorizontalKeystone):
        """
            Calls the SetHorizontalKeystone action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredHorizontalKeystone": DesiredHorizontalKeystone,
        }

        self._proxy_call_action("SetHorizontalKeystone", arguments=arguments)

        return

    def action_SetLoudness(self, InstanceID, Channel, DesiredLoudness):
        """
            Calls the SetLoudness action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredLoudness": DesiredLoudness,
        }

        self._proxy_call_action("SetLoudness", arguments=arguments)

        return

    def action_SetMute(self, InstanceID, Channel, DesiredMute):
        """
            Calls the SetMute action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredMute": DesiredMute,
        }

        self._proxy_call_action("SetMute", arguments=arguments)

        return

    def action_SetRedVideoBlackLevel(self, InstanceID, DesiredRedVideoBlackLevel):
        """
            Calls the SetRedVideoBlackLevel action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredRedVideoBlackLevel": DesiredRedVideoBlackLevel,
        }

        self._proxy_call_action("SetRedVideoBlackLevel", arguments=arguments)

        return

    def action_SetRedVideoGain(self, InstanceID, DesiredRedVideoGain):
        """
            Calls the SetRedVideoGain action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredRedVideoGain": DesiredRedVideoGain,
        }

        self._proxy_call_action("SetRedVideoGain", arguments=arguments)

        return

    def action_SetSharpness(self, InstanceID, DesiredSharpness):
        """
            Calls the SetSharpness action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredSharpness": DesiredSharpness,
        }

        self._proxy_call_action("SetSharpness", arguments=arguments)

        return

    def action_SetStateVariables(self, InstanceID, RenderingControlUDN, ServiceType, ServiceId, StateVariableValuePairs, extract_returns=True):
        """
            Calls the SetStateVariables action.

            :returns: "StateVariableList"
        """
        arguments = {
            "InstanceID": InstanceID,
            "RenderingControlUDN": RenderingControlUDN,
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

    def action_SetTransforms(self, InstanceID, DesiredTransformValues):
        """
            Calls the SetTransforms action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredTransformValues": DesiredTransformValues,
        }

        self._proxy_call_action("SetTransforms", arguments=arguments)

        return

    def action_SetVerticalKeystone(self, InstanceID, DesiredVerticalKeystone):
        """
            Calls the SetVerticalKeystone action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredVerticalKeystone": DesiredVerticalKeystone,
        }

        self._proxy_call_action("SetVerticalKeystone", arguments=arguments)

        return

    def action_SetVolume(self, InstanceID, Channel, DesiredVolume):
        """
            Calls the SetVolume action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredVolume": DesiredVolume,
        }

        self._proxy_call_action("SetVolume", arguments=arguments)

        return

    def action_SetVolumeDB(self, InstanceID, Channel, DesiredVolume):
        """
            Calls the SetVolumeDB action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredVolume": DesiredVolume,
        }

        self._proxy_call_action("SetVolumeDB", arguments=arguments)

        return
