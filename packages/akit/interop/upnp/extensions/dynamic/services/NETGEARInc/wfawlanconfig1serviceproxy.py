"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WFAWLANConfig1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WFAWLANConfig1' service.
    """

    SERVICE_MANUFACTURER = 'NETGEARInc'
    SERVICE_TYPE = 'urn:schemas-wifialliance-org:service:WFAWLANConfig:1'

    SERVICE_EVENT_VARIABLES = {
        "APStatus": { "data_type": "ui1", "default": None, "allowed_list": None},
        "STAStatus": { "data_type": "ui1", "default": None, "allowed_list": None},
        "WLANEvent": { "data_type": "bin.base64", "default": None, "allowed_list": None},
    }

    def action_DelAPSettings(self, NewAPSettings, extract_returns=True):
        """
            Calls the DelAPSettings action.

            :returns: "result"
        """
        arguments = {
            "NewAPSettings": NewAPSettings,
        }

        out_params = self._proxy_call_action("DelAPSettings", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DelSTASettings(self, NewSTASettings, extract_returns=True):
        """
            Calls the DelSTASettings action.

            :returns: "result"
        """
        arguments = {
            "NewSTASettings": NewSTASettings,
        }

        out_params = self._proxy_call_action("DelSTASettings", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAPSettings(self, NewMessage, extract_returns=True):
        """
            Calls the GetAPSettings action.

            :returns: "NewAPSettings"
        """
        arguments = {
            "NewMessage": NewMessage,
        }

        out_params = self._proxy_call_action("GetAPSettings", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAPSettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDeviceInfo(self, extract_returns=True):
        """
            Calls the GetDeviceInfo action.

            :returns: "NewDeviceInfo"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetDeviceInfo", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDeviceInfo",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSTASettings(self, NewMessage, extract_returns=True):
        """
            Calls the GetSTASettings action.

            :returns: "NewSTASettings"
        """
        arguments = {
            "NewMessage": NewMessage,
        }

        out_params = self._proxy_call_action("GetSTASettings", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewSTASettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_PutMessage(self, NewInMessage, extract_returns=True):
        """
            Calls the PutMessage action.

            :returns: "NewOutMessage"
        """
        arguments = {
            "NewInMessage": NewInMessage,
        }

        out_params = self._proxy_call_action("PutMessage", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewOutMessage",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_PutWLANResponse(self, NewMessage, NewWLANEventType, NewWLANEventMAC, extract_returns=True):
        """
            Calls the PutWLANResponse action.

            :returns: "result"
        """
        arguments = {
            "NewMessage": NewMessage,
            "NewWLANEventType": NewWLANEventType,
            "NewWLANEventMAC": NewWLANEventMAC,
        }

        out_params = self._proxy_call_action("PutWLANResponse", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RebootAP(self, NewAPSettings, extract_returns=True):
        """
            Calls the RebootAP action.

            :returns: "result"
        """
        arguments = {
            "NewAPSettings": NewAPSettings,
        }

        out_params = self._proxy_call_action("RebootAP", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RebootSTA(self, NewSTASettings, extract_returns=True):
        """
            Calls the RebootSTA action.

            :returns: "result"
        """
        arguments = {
            "NewSTASettings": NewSTASettings,
        }

        out_params = self._proxy_call_action("RebootSTA", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetAP(self, NewMessage, extract_returns=True):
        """
            Calls the ResetAP action.

            :returns: "result"
        """
        arguments = {
            "NewMessage": NewMessage,
        }

        out_params = self._proxy_call_action("ResetAP", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetSTA(self, NewMessage, extract_returns=True):
        """
            Calls the ResetSTA action.

            :returns: "result"
        """
        arguments = {
            "NewMessage": NewMessage,
        }

        out_params = self._proxy_call_action("ResetSTA", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetAPSettings(self, NewAPSettings, extract_returns=True):
        """
            Calls the SetAPSettings action.

            :returns: "result"
        """
        arguments = {
            "NewAPSettings": NewAPSettings,
        }

        out_params = self._proxy_call_action("SetAPSettings", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetSTASettings(self, extract_returns=True):
        """
            Calls the SetSTASettings action.

            :returns: "NewSTASettings"
        """
        arguments = { }

        out_params = self._proxy_call_action("SetSTASettings", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewSTASettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetSelectedRegistrar(self, NewMessage, extract_returns=True):
        """
            Calls the SetSelectedRegistrar action.

            :returns: "result"
        """
        arguments = {
            "NewMessage": NewMessage,
        }

        out_params = self._proxy_call_action("SetSelectedRegistrar", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
