"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ApplicationManagement2ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ApplicationManagement2' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ApplicationManagement:2'

    SERVICE_DEFAULT_VARIABLES = {
        "AppInfoList": { "data_type": "string", "default": None, "allowed_list": None},
        "FeatureList": { "data_type": "string", "default": None, "allowed_list": None},
        "SupportedTargetFields": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "RunningAppList": { "data_type": "string", "default": None, "allowed_list": None},
        "TransitioningApps": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_ConnectApptoApp(self, AppID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ConnectApptoApp action.

            :returns: "ConnectionID"
        """
        arguments = {
            "AppID": AppID,
        }

        out_params = self.call_action("ConnectApptoApp", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectionID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DisconnectApptoApp(self, ConnectionIDs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DisconnectApptoApp action.

            :returns: "DisconnectedConnectionIDs"
        """
        arguments = {
            "ConnectionIDs": ConnectionIDs,
        }

        out_params = self.call_action("DisconnectApptoApp", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("DisconnectedConnectionIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAppConnectionInfo(self, AppIDs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAppConnectionInfo action.

            :returns: "ConnectionInfo"
        """
        arguments = {
            "AppIDs": AppIDs,
        }

        out_params = self.call_action("GetAppConnectionInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectionInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAppIDList(self, Target, TargetFields, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAppIDList action.

            :returns: "AppIDs"
        """
        arguments = {
            "Target": Target,
            "TargetFields": TargetFields,
        }

        out_params = self.call_action("GetAppIDList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AppIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAppInfoByIDs(self, AppIDs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAppInfoByIDs action.

            :returns: "AppInfo"
        """
        arguments = {
            "AppIDs": AppIDs,
        }

        out_params = self.call_action("GetAppInfoByIDs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AppInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetCurrentConnectionInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCurrentConnectionInfo action.

            :returns: "ConnectionIDs", "ConnectionAppIDs"
        """
        arguments = { }

        out_params = self.call_action("GetCurrentConnectionInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ConnectionIDs", "ConnectionAppIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFeatureList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFeatureList action.

            :returns: "FeatureList"
        """
        arguments = { }

        out_params = self.call_action("GetFeatureList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FeatureList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetInstallationStatus(self, AppIDs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetInstallationStatus action.

            :returns: "InstallationStatus"
        """
        arguments = {
            "AppIDs": AppIDs,
        }

        out_params = self.call_action("GetInstallationStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("InstallationStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRunningAppList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRunningAppList action.

            :returns: "RunningAppList"
        """
        arguments = { }

        out_params = self.call_action("GetRunningAppList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RunningAppList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRunningStatus(self, AppIDs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRunningStatus action.

            :returns: "RunningStatus"
        """
        arguments = {
            "AppIDs": AppIDs,
        }

        out_params = self.call_action("GetRunningStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RunningStatus",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSupportedTargetFields(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSupportedTargetFields action.

            :returns: "SupportedTargetFields"
        """
        arguments = { }

        out_params = self.call_action("GetSupportedTargetFields", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SupportedTargetFields",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_InstallAppByID(self, AppID, InstallParameters, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the InstallAppByID action.
        """
        arguments = {
            "AppID": AppID,
            "InstallParameters": InstallParameters,
        }

        self.call_action("InstallAppByID", arguments=arguments, aspects=aspects)

        return

    def action_InstallAppByURI(self, InstallationURI, AppInfo, InstallParameters, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the InstallAppByURI action.

            :returns: "AppID"
        """
        arguments = {
            "InstallationURI": InstallationURI,
            "AppInfo": AppInfo,
            "InstallParameters": InstallParameters,
        }

        out_params = self.call_action("InstallAppByURI", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AppID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StartAppByID(self, AppID, StartParameters, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartAppByID action.
        """
        arguments = {
            "AppID": AppID,
            "StartParameters": StartParameters,
        }

        self.call_action("StartAppByID", arguments=arguments, aspects=aspects)

        return

    def action_StartAppByURI(self, StartURI, AppInfo, StartParameters, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartAppByURI action.

            :returns: "AppID"
        """
        arguments = {
            "StartURI": StartURI,
            "AppInfo": AppInfo,
            "StartParameters": StartParameters,
        }

        out_params = self.call_action("StartAppByURI", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AppID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StopApp(self, AppIDs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StopApp action.

            :returns: "StoppedAppIDs"
        """
        arguments = {
            "AppIDs": AppIDs,
        }

        out_params = self.call_action("StopApp", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StoppedAppIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_UninstallApp(self, AppIDs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UninstallApp action.

            :returns: "UninstalledAppIDs"
        """
        arguments = {
            "AppIDs": AppIDs,
        }

        out_params = self.call_action("UninstallApp", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("UninstalledAppIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
