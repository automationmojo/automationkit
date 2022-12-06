"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class LANHostConfigManagement1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'LANHostConfigManagement1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:LANHostConfigManagement:1'

    SERVICE_DEFAULT_VARIABLES = {
        "DHCPRelay": { "data_type": "boolean", "default": None, "allowed_list": None},
        "DHCPServerConfigurable": { "data_type": "boolean", "default": None, "allowed_list": None},
        "DNSServers": { "data_type": "string", "default": None, "allowed_list": None},
        "DomainName": { "data_type": "string", "default": None, "allowed_list": None},
        "IPRouters": { "data_type": "string", "default": None, "allowed_list": None},
        "MaxAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "MinAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "ReservedAddresses": { "data_type": "string", "default": None, "allowed_list": None},
        "SubnetMask": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_DeleteDNSServer(self, NewDNSServers, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteDNSServer action.
        """
        arguments = {
            "NewDNSServers": NewDNSServers,
        }

        self.call_action("DeleteDNSServer", arguments=arguments, aspects=aspects)

        return

    def action_DeleteIPRouter(self, NewIPRouters, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteIPRouter action.
        """
        arguments = {
            "NewIPRouters": NewIPRouters,
        }

        self.call_action("DeleteIPRouter", arguments=arguments, aspects=aspects)

        return

    def action_DeleteReservedAddress(self, NewReservedAddresses, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DeleteReservedAddress action.
        """
        arguments = {
            "NewReservedAddresses": NewReservedAddresses,
        }

        self.call_action("DeleteReservedAddress", arguments=arguments, aspects=aspects)

        return

    def action_GetAddressRange(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAddressRange action.

            :returns: "NewMinAddress", "NewMaxAddress"
        """
        arguments = { }

        out_params = self.call_action("GetAddressRange", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewMinAddress", "NewMaxAddress",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDHCPRelay(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDHCPRelay action.

            :returns: "NewDHCPRelay"
        """
        arguments = { }

        out_params = self.call_action("GetDHCPRelay", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDHCPRelay",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDHCPServerConfigurable(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDHCPServerConfigurable action.

            :returns: "NewDHCPServerConfigurable"
        """
        arguments = { }

        out_params = self.call_action("GetDHCPServerConfigurable", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDHCPServerConfigurable",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDNSServers(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDNSServers action.

            :returns: "NewDNSServers"
        """
        arguments = { }

        out_params = self.call_action("GetDNSServers", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDNSServers",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDomainName(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDomainName action.

            :returns: "NewDomainName"
        """
        arguments = { }

        out_params = self.call_action("GetDomainName", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDomainName",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetIPRoutersList(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetIPRoutersList action.

            :returns: "NewIPRouters"
        """
        arguments = { }

        out_params = self.call_action("GetIPRoutersList", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewIPRouters",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetReservedAddresses(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetReservedAddresses action.

            :returns: "NewReservedAddresses"
        """
        arguments = { }

        out_params = self.call_action("GetReservedAddresses", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewReservedAddresses",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSubnetMask(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSubnetMask action.

            :returns: "NewSubnetMask"
        """
        arguments = { }

        out_params = self.call_action("GetSubnetMask", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewSubnetMask",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetAddressRange(self, NewMinAddress, NewMaxAddress, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAddressRange action.
        """
        arguments = {
            "NewMinAddress": NewMinAddress,
            "NewMaxAddress": NewMaxAddress,
        }

        self.call_action("SetAddressRange", arguments=arguments, aspects=aspects)

        return

    def action_SetDHCPRelay(self, NewDHCPRelay, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDHCPRelay action.
        """
        arguments = {
            "NewDHCPRelay": NewDHCPRelay,
        }

        self.call_action("SetDHCPRelay", arguments=arguments, aspects=aspects)

        return

    def action_SetDHCPServerConfigurable(self, NewDHCPServerConfigurable, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDHCPServerConfigurable action.
        """
        arguments = {
            "NewDHCPServerConfigurable": NewDHCPServerConfigurable,
        }

        self.call_action("SetDHCPServerConfigurable", arguments=arguments, aspects=aspects)

        return

    def action_SetDNSServer(self, NewDNSServers, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDNSServer action.
        """
        arguments = {
            "NewDNSServers": NewDNSServers,
        }

        self.call_action("SetDNSServer", arguments=arguments, aspects=aspects)

        return

    def action_SetDomainName(self, NewDomainName, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDomainName action.
        """
        arguments = {
            "NewDomainName": NewDomainName,
        }

        self.call_action("SetDomainName", arguments=arguments, aspects=aspects)

        return

    def action_SetIPRouter(self, NewIPRouters, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetIPRouter action.
        """
        arguments = {
            "NewIPRouters": NewIPRouters,
        }

        self.call_action("SetIPRouter", arguments=arguments, aspects=aspects)

        return

    def action_SetReservedAddress(self, NewReservedAddresses, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetReservedAddress action.
        """
        arguments = {
            "NewReservedAddresses": NewReservedAddresses,
        }

        self.call_action("SetReservedAddress", arguments=arguments, aspects=aspects)

        return

    def action_SetSubnetMask(self, NewSubnetMask, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetSubnetMask action.
        """
        arguments = {
            "NewSubnetMask": NewSubnetMask,
        }

        self.call_action("SetSubnetMask", arguments=arguments, aspects=aspects)

        return
