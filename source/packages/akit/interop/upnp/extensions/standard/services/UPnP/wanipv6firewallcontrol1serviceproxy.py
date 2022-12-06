"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WANIPv6FirewallControl1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WANIPv6FirewallControl1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WANIPv6FirewallControl:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "FirewallEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "InboundPinholeAllowed": { "data_type": "boolean", "default": None, "allowed_list": None},
    }

    def action_AddPinhole(self, RemoteHost, RemotePort, InternalClient, InternalPort, Protocol, LeaseTime, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddPinhole action.

            :returns: "UniqueID"
        """
        arguments = {
            "RemoteHost": RemoteHost,
            "RemotePort": RemotePort,
            "InternalClient": InternalClient,
            "InternalPort": InternalPort,
            "Protocol": Protocol,
            "LeaseTime": LeaseTime,
        }

        out_params = self.call_action("AddPinhole", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("UniqueID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_CheckPinholeWorking(self, UniqueID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CheckPinholeWorking action.

            :returns: "IsWorking"
        """
        arguments = {
            "UniqueID": UniqueID,
        }

        out_params = self.call_action("CheckPinholeWorking", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("IsWorking",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DeletePinhole(self, UniqueID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeletePinhole action.
        """
        arguments = {
            "UniqueID": UniqueID,
        }

        self.call_action("DeletePinhole", arguments=arguments, aspects=aspects)

        return

    def action_GetFirewallStatus(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFirewallStatus action.

            :returns: "FirewallEnabled", "InboundPinholeAllowed"
        """
        arguments = { }

        out_params = self.call_action("GetFirewallStatus", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FirewallEnabled", "InboundPinholeAllowed",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetOutboundPinholeTimeout(self, RemoteHost, RemotePort, InternalClient, InternalPort, Protocol, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetOutboundPinholeTimeout action.

            :returns: "OutboundPinholeTimeout"
        """
        arguments = {
            "RemoteHost": RemoteHost,
            "RemotePort": RemotePort,
            "InternalClient": InternalClient,
            "InternalPort": InternalPort,
            "Protocol": Protocol,
        }

        out_params = self.call_action("GetOutboundPinholeTimeout", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("OutboundPinholeTimeout",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPinholePackets(self, UniqueID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPinholePackets action.

            :returns: "PinholePackets"
        """
        arguments = {
            "UniqueID": UniqueID,
        }

        out_params = self.call_action("GetPinholePackets", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("PinholePackets",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_UpdatePinhole(self, UniqueID, NewLeaseTime, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UpdatePinhole action.
        """
        arguments = {
            "UniqueID": UniqueID,
            "NewLeaseTime": NewLeaseTime,
        }

        self.call_action("UpdatePinhole", arguments=arguments, aspects=aspects)

        return
