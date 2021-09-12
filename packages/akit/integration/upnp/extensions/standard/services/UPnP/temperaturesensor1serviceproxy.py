"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class TemperatureSensor1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'TemperatureSensor1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:TemperatureSensor:1'

    SERVICE_EVENT_VARIABLES = {
        "Application": { "data_type": "string", "default": "Room", "allowed_list": "['Room', 'Outdoor', 'Pipe', 'AirDuct']"},
        "CurrentTemperature": { "data_type": "i4", "default": "2000", "allowed_list": None},
        "Name": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_GetApplication(self, extract_returns=True):
        """
            Calls the GetApplication action.

            :returns: "CurrentApplication"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetApplication", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentApplication",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCurrentTemperature(self, extract_returns=True):
        """
            Calls the GetCurrentTemperature action.

            :returns: "CurrentTemp"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetCurrentTemperature", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTemp",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetName(self, extract_returns=True):
        """
            Calls the GetName action.

            :returns: "CurrentName"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetName", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentName",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetApplication(self, NewApplication):
        """
            Calls the SetApplication action.
        """
        arguments = {
            "NewApplication": NewApplication,
        }

        self._proxy_call_action("SetApplication", arguments=arguments)

        return

    def action_SetName(self, NewName):
        """
            Calls the SetName action.
        """
        arguments = {
            "NewName": NewName,
        }

        self._proxy_call_action("SetName", arguments=arguments)

        return
