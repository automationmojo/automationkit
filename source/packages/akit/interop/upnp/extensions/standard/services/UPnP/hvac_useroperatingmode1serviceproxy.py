"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class HVAC_UserOperatingMode1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'HVAC_UserOperatingMode1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:HVAC_UserOperatingMode:1'

    SERVICE_DEFAULT_VARIABLES = {
        "ModeStatus": { "data_type": "string", "default": "Off", "allowed_list": "['Off', 'InDeadBand', 'HeatOn', 'CoolOn', 'AutoChangeOver', 'AuxHeatOn', 'EconomyHeatOn', 'EmergencyHeatOn', 'AuxCoolOn', 'EconomyCoolOn', 'BuildingProtection', 'EnergySavingsHeating', 'EnergySavingsCooling']"},
        "ModeTarget": { "data_type": "string", "default": "Off", "allowed_list": "['Off', 'HeatOn', 'CoolOn', 'AutoChangeOver', 'AuxHeatOn', 'EconomyHeatOn', 'EmergencyHeatOn', 'AuxCoolOn', 'EconomyCoolOn', 'BuildingProtection', 'EnergySavingsMode']"},
        "Name": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetModeStatus(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetModeStatus action.

            :returns: "CurrentModeStatus"
        """
        arguments = { }

        out_params = self.call_action("GetModeStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentModeStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetModeTarget(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetModeTarget action.

            :returns: "CurrentModeTarget"
        """
        arguments = { }

        out_params = self.call_action("GetModeTarget", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentModeTarget",)]
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

    def action_SetModeTarget(self, NewModeTarget, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetModeTarget action.
        """
        arguments = {
            "NewModeTarget": NewModeTarget,
        }

        self.call_action("SetModeTarget", arguments=arguments, aspects=aspects)

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
