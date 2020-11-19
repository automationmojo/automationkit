"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class HVAC_SetpointSchedule1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'HVAC_SetpointSchedule1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:HVAC_SetpointSchedule:1'
    
    SERVICE_EVENT_VARIABLES = {}


    def action_GetEventsPerDay(self, SubmittedDayOfWeek, extract_returns=True):
        """
            Calls the GetEventsPerDay action.

            :returns: "CurrentEventsPerDay"
        """
        arguments = {
            "SubmittedDayOfWeek": SubmittedDayOfWeek,
        }

        out_params = self._proxy_call_action("GetEventsPerDay", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentEventsPerDay",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_SetEventParameters(self, SubmittedDayOfWeek, SubmittedEventName, NewStartTime, NewHeatingSetpoint, NewCoolingSetpoint, extract_returns=True):
        """
            Calls the SetEventParameters action.

            :returns: "result"
        """
        arguments = {
            "SubmittedDayOfWeek": SubmittedDayOfWeek,
            "SubmittedEventName": SubmittedEventName,
            "NewStartTime": NewStartTime,
            "NewHeatingSetpoint": NewHeatingSetpoint,
            "NewCoolingSetpoint": NewCoolingSetpoint,
        }

        out_params = self._proxy_call_action("SetEventParameters", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

