"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class SoftwareManagement1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'SoftwareManagement1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:SoftwareManagement:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_GetActiveEUIDs(self, extract_returns=True):
        """
            Calls the GetActiveEUIDs action.

            :returns: "ActiveEUIDs"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetActiveEUIDs", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ActiveEUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDUIDs(self, extract_returns=True):
        """
            Calls the GetDUIDs action.

            :returns: "DUIDs"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetDUIDs", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDUInfo(self, DUID, extract_returns=True):
        """
            Calls the GetDUInfo action.

            :returns: "DUName", "DUVersion", "DUType", "DUState", "DUURI"
        """
        arguments = {
            "DUID": DUID,
        }

        out_params = self._proxy_call_action("GetDUInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DUName", "DUVersion", "DUType", "DUState", "DUURI",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetEUIDs(self, extract_returns=True):
        """
            Calls the GetEUIDs action.

            :returns: "EUIDs"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetEUIDs", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("EUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetEUInfo(self, EUID, extract_returns=True):
        """
            Calls the GetEUInfo action.

            :returns: "EUName", "EUVersion", "EURequestedState", "EUExecutionState"
        """
        arguments = {
            "EUID": EUID,
        }

        out_params = self._proxy_call_action("GetEUInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("EUName", "EUVersion", "EURequestedState", "EUExecutionState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetErrorEUIDs(self, extract_returns=True):
        """
            Calls the GetErrorEUIDs action.

            :returns: "ErrorEUIDs"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetErrorEUIDs", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ErrorEUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOperationIDs(self, extract_returns=True):
        """
            Calls the GetOperationIDs action.

            :returns: "OperationIDs"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetOperationIDs", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOperationInfo(self, OperationID, extract_returns=True):
        """
            Calls the GetOperationInfo action.

            :returns: "OperationState", "TargetedIDs", "Action", "ErrorDescription", "AdditionalInfo"
        """
        arguments = {
            "OperationID": OperationID,
        }

        out_params = self._proxy_call_action("GetOperationInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationState", "TargetedIDs", "Action", "ErrorDescription", "AdditionalInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRunningEUIDs(self, extract_returns=True):
        """
            Calls the GetRunningEUIDs action.

            :returns: "RunningEUIDs"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetRunningEUIDs", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RunningEUIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Install(self, DUURI, DUType, HandleDependencies, extract_returns=True):
        """
            Calls the Install action.

            :returns: "OperationID"
        """
        arguments = {
            "DUURI": DUURI,
            "DUType": DUType,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self._proxy_call_action("Install", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Start(self, EUID, HandleDependencies, extract_returns=True):
        """
            Calls the Start action.

            :returns: "OperationID"
        """
        arguments = {
            "EUID": EUID,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self._proxy_call_action("Start", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Stop(self, EUID, HandleDependencies, extract_returns=True):
        """
            Calls the Stop action.

            :returns: "OperationID"
        """
        arguments = {
            "EUID": EUID,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self._proxy_call_action("Stop", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Uninstall(self, DUID, HandleDependencies, extract_returns=True):
        """
            Calls the Uninstall action.

            :returns: "OperationID"
        """
        arguments = {
            "DUID": DUID,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self._proxy_call_action("Uninstall", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Update(self, DUID, NewDUURI, HandleDependencies, extract_returns=True):
        """
            Calls the Update action.

            :returns: "OperationID"
        """
        arguments = {
            "DUID": DUID,
            "NewDUURI": NewDUURI,
            "HandleDependencies": HandleDependencies,
        }

        out_params = self._proxy_call_action("Update", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OperationID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
