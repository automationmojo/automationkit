"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RenderingControl1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RenderingControl1' service.
    """

    SERVICE_MANUFACTURER = 'MicrosoftCorporation'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RenderingControl:1'

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

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

    def action_SelectPreset(self, InstanceID, PresetName, extract_returns=True):
        """
            Calls the SelectPreset action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
            "PresetName": PresetName,
        }

        out_params = self._proxy_call_action("SelectPreset", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetMute(self, InstanceID, Channel, DesiredMute, extract_returns=True):
        """
            Calls the SetMute action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredMute": DesiredMute,
        }

        out_params = self._proxy_call_action("SetMute", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetVolume(self, InstanceID, Channel, DesiredVolume, extract_returns=True):
        """
            Calls the SetVolume action.

            :returns: "result"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Channel": Channel,
            "DesiredVolume": DesiredVolume,
        }

        out_params = self._proxy_call_action("SetVolume", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
