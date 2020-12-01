"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Presence1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Presence1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Presence:1'

    SERVICE_EVENT_VARIABLES = {
        "PresenceOfContactsUpdate": { "data_type": "string", "default": None, "allowed_list": None},
        "UserPresenceInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "Watcher": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AuthorizePresenceProactive(self, UserPresenceInfo, Expire, WatcherList, extract_returns=True):
        """
            Calls the AuthorizePresenceProactive action.

            :returns: "result"
        """
        arguments = {
            "UserPresenceInfo": UserPresenceInfo,
            "Expire": Expire,
            "WatcherList": WatcherList,
        }

        out_params = self._proxy_call_action("AuthorizePresenceProactive", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AuthorizePresenceReactive(self, Contact, Expire, UserPresenceInfo, extract_returns=True):
        """
            Calls the AuthorizePresenceReactive action.

            :returns: "result"
        """
        arguments = {
            "Contact": Contact,
            "Expire": Expire,
            "UserPresenceInfo": UserPresenceInfo,
        }

        out_params = self._proxy_call_action("AuthorizePresenceReactive", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetContactPresence(self, TargetContact, extract_returns=True):
        """
            Calls the GetContactPresence action.

            :returns: "ContactPresence"
        """
        arguments = {
            "TargetContact": TargetContact,
        }

        out_params = self._proxy_call_action("GetContactPresence", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ContactPresence",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPresence(self, extract_returns=True):
        """
            Calls the GetPresence action.

            :returns: "UserPresence"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetPresence", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("UserPresence",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPresenceOfContactsUpdate(self, extract_returns=True):
        """
            Calls the GetPresenceOfContactsUpdate action.

            :returns: "ContactPresenceUpdate"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetPresenceOfContactsUpdate", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ContactPresenceUpdate",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RegisterForContactPresence(self, Contact, Expire, extract_returns=True):
        """
            Calls the RegisterForContactPresence action.

            :returns: "RegistrationResult"
        """
        arguments = {
            "Contact": Contact,
            "Expire": Expire,
        }

        out_params = self._proxy_call_action("RegisterForContactPresence", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("RegistrationResult",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_UpdatePresence(self, UpdatedUserPresence, extract_returns=True):
        """
            Calls the UpdatePresence action.

            :returns: "result"
        """
        arguments = {
            "UpdatedUserPresence": UpdatedUserPresence,
        }

        out_params = self._proxy_call_action("UpdatePresence", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
