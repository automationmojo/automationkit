"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class TemperatureSetpoint1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'TemperatureSetpoint1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:TemperatureSetpoint:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "Application": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentSetpoint": { "data_type": "i4", "default": None, "allowed_list": None},
        "Name": { "data_type": "string", "default": None, "allowed_list": None},
        "SetpointAchieved": { "data_type": "boolean", "default": "0", "allowed_list": None},
    }

    def action_GetApplication(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetApplication action.

            :returns: "CurrentApplication"
        """
        arguments = { }

        out_params = self.call_action("GetApplication", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentApplication",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCurrentSetpoint(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCurrentSetpoint action.

            :returns: "CurrentSP"
        """
        arguments = { }

        out_params = self.call_action("GetCurrentSetpoint", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentSP",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetName(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetName action.

            :returns: "CurrentName"
        """
        arguments = { }

        out_params = self.call_action("GetName", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentName",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSetpointAchieved(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSetpointAchieved action.

            :returns: "CurrentSPA"
        """
        arguments = { }

        out_params = self.call_action("GetSetpointAchieved", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentSPA",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetApplication(self, NewApplication, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetApplication action.
        """
        arguments = {
            "NewApplication": NewApplication,
        }

        self.call_action("SetApplication", arguments=arguments, aspects=aspects)

        return

    def action_SetCurrentSetpoint(self, NewCurrentSetpoint, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetCurrentSetpoint action.
        """
        arguments = {
            "NewCurrentSetpoint": NewCurrentSetpoint,
        }

        self.call_action("SetCurrentSetpoint", arguments=arguments, aspects=aspects)

        return

    def action_SetName(self, NewName, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetName action.
        """
        arguments = {
            "NewName": NewName,
        }

        self.call_action("SetName", arguments=arguments, aspects=aspects)

        return
