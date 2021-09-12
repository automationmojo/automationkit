"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class HouseStatus1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'HouseStatus1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:HouseStatus:1'

    SERVICE_EVENT_VARIABLES = {
        "ActivityLevel": { "data_type": "string", "default": "Regular", "allowed_list": "['Regular', 'Asleep', 'HighActivity']"},
        "DormancyLevel": { "data_type": "string", "default": "Regular", "allowed_list": "['Regular', 'Vacation', 'PetsAtHome']"},
        "OccupancyState": { "data_type": "string", "default": "Occupied", "allowed_list": "['Occupied', 'Unoccupied', 'Indeterminate']"},
    }

    def action_GetActivityLevel(self, extract_returns=True):
        """
            Calls the GetActivityLevel action.

            :returns: "CurrentActivityLevel"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetActivityLevel", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentActivityLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDormancyLevel(self, extract_returns=True):
        """
            Calls the GetDormancyLevel action.

            :returns: "CurrentDormancyLevel"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetDormancyLevel", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentDormancyLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOccupancyState(self, extract_returns=True):
        """
            Calls the GetOccupancyState action.

            :returns: "CurrentOccupancyState"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetOccupancyState", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentOccupancyState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetActivityLevel(self, NewActivityLevel):
        """
            Calls the SetActivityLevel action.
        """
        arguments = {
            "NewActivityLevel": NewActivityLevel,
        }

        self._proxy_call_action("SetActivityLevel", arguments=arguments)

        return

    def action_SetDormancyLevel(self, NewDormancyLevel):
        """
            Calls the SetDormancyLevel action.
        """
        arguments = {
            "NewDormancyLevel": NewDormancyLevel,
        }

        self._proxy_call_action("SetDormancyLevel", arguments=arguments)

        return

    def action_SetOccupancyState(self, NewOccupancyState):
        """
            Calls the SetOccupancyState action.
        """
        arguments = {
            "NewOccupancyState": NewOccupancyState,
        }

        self._proxy_call_action("SetOccupancyState", arguments=arguments)

        return
