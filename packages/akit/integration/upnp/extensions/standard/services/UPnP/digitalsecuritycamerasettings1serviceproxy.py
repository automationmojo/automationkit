"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class DigitalSecurityCameraSettings1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'DigitalSecurityCameraSettings1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:DigitalSecurityCameraSettings:1'

    SERVICE_EVENT_VARIABLES = {
        "AutomaticWhiteBalance": { "data_type": "boolean", "default": "1", "allowed_list": None},
        "Brightness": { "data_type": "ui1", "default": "50", "allowed_list": None},
        "ColorSaturation": { "data_type": "ui1", "default": "50", "allowed_list": None},
        "DefaultRotation": { "data_type": "string", "default": None, "allowed_list": None},
        "FixedWhiteBalance": { "data_type": "ui4", "default": "3000", "allowed_list": None},
    }

    def action_DecreaseBrightness(self):
        """
            Calls the DecreaseBrightness action.
        """
        arguments = { }

        self._proxy_call_action("DecreaseBrightness", arguments=arguments)

        return

    def action_DecreaseColorSaturation(self):
        """
            Calls the DecreaseColorSaturation action.
        """
        arguments = { }

        self._proxy_call_action("DecreaseColorSaturation", arguments=arguments)

        return

    def action_GetAutomaticWhiteBalance(self, extract_returns=True):
        """
            Calls the GetAutomaticWhiteBalance action.

            :returns: "RetAutomaticWhiteBalance"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetAutomaticWhiteBalance", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetAutomaticWhiteBalance",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAvailableRotations(self, extract_returns=True):
        """
            Calls the GetAvailableRotations action.

            :returns: "RetAvailableRotations"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetAvailableRotations", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetAvailableRotations",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBrightness(self, extract_returns=True):
        """
            Calls the GetBrightness action.

            :returns: "RetBrightness"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetBrightness", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetBrightness",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetColorSaturation(self, extract_returns=True):
        """
            Calls the GetColorSaturation action.

            :returns: "RetColorSaturation"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetColorSaturation", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetColorSaturation",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultRotation(self, extract_returns=True):
        """
            Calls the GetDefaultRotation action.

            :returns: "RetRotation"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetDefaultRotation", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetRotation",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFixedWhiteBalance(self, extract_returns=True):
        """
            Calls the GetFixedWhiteBalance action.

            :returns: "RetFixedWhiteBalance"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetFixedWhiteBalance", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RetFixedWhiteBalance",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_IncreaseBrightness(self):
        """
            Calls the IncreaseBrightness action.
        """
        arguments = { }

        self._proxy_call_action("IncreaseBrightness", arguments=arguments)

        return

    def action_IncreaseColorSaturation(self):
        """
            Calls the IncreaseColorSaturation action.
        """
        arguments = { }

        self._proxy_call_action("IncreaseColorSaturation", arguments=arguments)

        return

    def action_SetAutomaticWhiteBalance(self, NewAutomaticWhiteBalance):
        """
            Calls the SetAutomaticWhiteBalance action.
        """
        arguments = {
            "NewAutomaticWhiteBalance": NewAutomaticWhiteBalance,
        }

        self._proxy_call_action("SetAutomaticWhiteBalance", arguments=arguments)

        return

    def action_SetBrightness(self, NewBrightness):
        """
            Calls the SetBrightness action.
        """
        arguments = {
            "NewBrightness": NewBrightness,
        }

        self._proxy_call_action("SetBrightness", arguments=arguments)

        return

    def action_SetColorSaturation(self, NewColorSaturation):
        """
            Calls the SetColorSaturation action.
        """
        arguments = {
            "NewColorSaturation": NewColorSaturation,
        }

        self._proxy_call_action("SetColorSaturation", arguments=arguments)

        return

    def action_SetDefaultRotation(self, NewRotation):
        """
            Calls the SetDefaultRotation action.
        """
        arguments = {
            "NewRotation": NewRotation,
        }

        self._proxy_call_action("SetDefaultRotation", arguments=arguments)

        return

    def action_SetFixedWhiteBalance(self, NewFixedWhiteBalance):
        """
            Calls the SetFixedWhiteBalance action.
        """
        arguments = {
            "NewFixedWhiteBalance": NewFixedWhiteBalance,
        }

        self._proxy_call_action("SetFixedWhiteBalance", arguments=arguments)

        return
