"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Calendar1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Calendar1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:Calendar:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "CalendarItem": { "data_type": "string", "default": None, "allowed_list": None},
        "MemoInfo": { "data_type": "string", "default": None, "allowed_list": None},
        "TriggeredItem": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddCalendarItems(self, Caltems, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddCalendarItems action.

            :returns: "ItemIDs"
        """
        arguments = {
            "Caltems": Caltems,
        }

        out_params = self.call_action("AddCalendarItems", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ItemIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeleteCalendarItems(self, ItemIDs, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteCalendarItems action.
        """
        arguments = {
            "ItemIDs": ItemIDs,
        }

        self.call_action("DeleteCalendarItems", arguments=arguments, aspects=aspects)

        return

    def action_GetCalendarItems(self, ItemIDs, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetCalendarItems action.

            :returns: "Caltems"
        """
        arguments = {
            "ItemIDs": ItemIDs,
        }

        out_params = self.call_action("GetCalendarItems", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Caltems",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetMemo(self, MemoID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetMemo action.

            :returns: "MemoInfoList"
        """
        arguments = {
            "MemoID": MemoID,
        }

        out_params = self.call_action("GetMemo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MemoInfoList",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTelCPNameList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTelCPNameList action.

            :returns: "TelCPName"
        """
        arguments = { }

        out_params = self.call_action("GetTelCPNameList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TelCPName",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTriggeredItems(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTriggeredItems action.

            :returns: "TriggeredItemIDs"
        """
        arguments = { }

        out_params = self.call_action("GetTriggeredItems", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TriggeredItemIDs",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_PostMemo(self, Memo, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the PostMemo action.

            :returns: "MemoID"
        """
        arguments = {
            "Memo": Memo,
        }

        out_params = self.call_action("PostMemo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("MemoID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RegisterItemDelivery(self, ItemDeliveryMethod, Expires, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RegisterItemDelivery action.
        """
        arguments = {
            "ItemDeliveryMethod": ItemDeliveryMethod,
            "Expires": Expires,
        }

        self.call_action("RegisterItemDelivery", arguments=arguments, aspects=aspects)

        return

    def action_RegisterTelCPName(self, TelCPName, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RegisterTelCPName action.
        """
        arguments = {
            "TelCPName": TelCPName,
        }

        self.call_action("RegisterTelCPName", arguments=arguments, aspects=aspects)

        return

    def action_UnregisterTelCPName(self, TelCPName, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UnregisterTelCPName action.
        """
        arguments = {
            "TelCPName": TelCPName,
        }

        self.call_action("UnregisterTelCPName", arguments=arguments, aspects=aspects)

        return

    def action_UpdateCalendarItems(self, Caltems, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UpdateCalendarItems action.
        """
        arguments = {
            "Caltems": Caltems,
        }

        self.call_action("UpdateCalendarItems", arguments=arguments, aspects=aspects)

        return
