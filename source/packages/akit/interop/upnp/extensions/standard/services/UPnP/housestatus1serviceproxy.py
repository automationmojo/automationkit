"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class HouseStatus1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'HouseStatus1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:HouseStatus:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "ActivityLevel": { "data_type": "string", "default": "Regular", "allowed_list": "['Regular', 'Asleep', 'HighActivity']"},
        "DormancyLevel": { "data_type": "string", "default": "Regular", "allowed_list": "['Regular', 'Vacation', 'PetsAtHome']"},
        "OccupancyState": { "data_type": "string", "default": "Occupied", "allowed_list": "['Occupied', 'Unoccupied', 'Indeterminate']"},
    }

    def action_GetActivityLevel(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetActivityLevel action.

            :returns: "CurrentActivityLevel"
        """
        arguments = { }

        out_params = self.call_action("GetActivityLevel", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentActivityLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDormancyLevel(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDormancyLevel action.

            :returns: "CurrentDormancyLevel"
        """
        arguments = { }

        out_params = self.call_action("GetDormancyLevel", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentDormancyLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOccupancyState(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetOccupancyState action.

            :returns: "CurrentOccupancyState"
        """
        arguments = { }

        out_params = self.call_action("GetOccupancyState", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentOccupancyState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetActivityLevel(self, NewActivityLevel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetActivityLevel action.
        """
        arguments = {
            "NewActivityLevel": NewActivityLevel,
        }

        self.call_action("SetActivityLevel", arguments=arguments, aspects=aspects)

        return

    def action_SetDormancyLevel(self, NewDormancyLevel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDormancyLevel action.
        """
        arguments = {
            "NewDormancyLevel": NewDormancyLevel,
        }

        self.call_action("SetDormancyLevel", arguments=arguments, aspects=aspects)

        return

    def action_SetOccupancyState(self, NewOccupancyState, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetOccupancyState action.
        """
        arguments = {
            "NewOccupancyState": NewOccupancyState,
        }

        self.call_action("SetOccupancyState", arguments=arguments, aspects=aspects)

        return
