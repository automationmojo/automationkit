"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class SoftwareManagement1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'SoftwareManagement1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:SoftwareManagement:1'

    SERVICE_DEFAULT_VARIABLES = {
        "ActiveEUIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "DUIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "EUIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "ErrorEUIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "OperationIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "RunningEUIDs": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_GetActiveEUIDs(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetActiveEUIDs action.

            :returns: "ActiveEUIDs"
        """
        arguments = { }

        out_params = self.call_action("GetActiveEUIDs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ActiveEUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDUIDs(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDUIDs action.

            :returns: "DUIDs"
        """
        arguments = { }

        out_params = self.call_action("GetDUIDs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDUInfo(self, DUID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDUInfo action.

            :returns: "DUName", "DUVersion", "DUType", "DUState", "DUURI"
        """
        arguments = {
            "DUID": DUID,
        }

        out_params = self.call_action("GetDUInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DUName", "DUVersion", "DUType", "DUState", "DUURI",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetEUIDs(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetEUIDs action.

            :returns: "EUIDs"
        """
        arguments = { }

        out_params = self.call_action("GetEUIDs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("EUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetEUInfo(self, EUID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetEUInfo action.

            :returns: "EUName", "EUVersion", "EURequestedState", "EUExecutionState"
        """
        arguments = {
            "EUID": EUID,
        }

        out_params = self.call_action("GetEUInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("EUName", "EUVersion", "EURequestedState", "EUExecutionState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetErrorEUIDs(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetErrorEUIDs action.

            :returns: "ErrorEUIDs"
        """
        arguments = { }

        out_params = self.call_action("GetErrorEUIDs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ErrorEUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOperationIDs(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetOperationIDs action.

            :returns: "OperationIDs"
        """
        arguments = { }

        out_params = self.call_action("GetOperationIDs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOperationInfo(self, OperationID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetOperationInfo action.

            :returns: "OperationState", "TargetedIDs", "Action", "ErrorDescription", "AdditionalInfo"
        """
        arguments = {
            "OperationID": OperationID,
        }

        out_params = self.call_action("GetOperationInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationState", "TargetedIDs", "Action", "ErrorDescription", "AdditionalInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRunningEUIDs(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRunningEUIDs action.

            :returns: "RunningEUIDs"
        """
        arguments = { }

        out_params = self.call_action("GetRunningEUIDs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RunningEUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Install(self, DUURI, DUType, HandleDependencies, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Install action.

            :returns: "OperationID"
        """
        arguments = {
            "DUURI": DUURI,
            "DUType": DUType,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self.call_action("Install", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Start(self, EUID, HandleDependencies, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Start action.

            :returns: "OperationID"
        """
        arguments = {
            "EUID": EUID,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self.call_action("Start", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Stop(self, EUID, HandleDependencies, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Stop action.

            :returns: "OperationID"
        """
        arguments = {
            "EUID": EUID,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self.call_action("Stop", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Uninstall(self, DUID, HandleDependencies, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Uninstall action.

            :returns: "OperationID"
        """
        arguments = {
            "DUID": DUID,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self.call_action("Uninstall", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Update(self, DUID, NewDUURI, HandleDependencies, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Update action.

            :returns: "OperationID"
        """
        arguments = {
            "DUID": DUID,
            "NewDUURI": NewDUURI,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self.call_action("Update", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
