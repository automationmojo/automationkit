"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RADASync1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RADASync1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RADASync:1'

    SERVICE_DEFAULT_VARIABLES = {
        "SystemInfo": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {}

    def action_AddRemoteDevices(self, DeviceList, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddRemoteDevices action.
        """
        arguments = {
            "DeviceList": DeviceList,
            "ID": ID,
        }

        self.call_action("AddRemoteDevices", arguments=arguments, aspects=aspects)

        return

    def action_HeartbeatUpdate(self, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the HeartbeatUpdate action.
        """
        arguments = {
            "ID": ID,
        }

        self.call_action("HeartbeatUpdate", arguments=arguments, aspects=aspects)

        return

    def action_RemoveRemoteDevices(self, DeviceList, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveRemoteDevices action.
        """
        arguments = {
            "DeviceList": DeviceList,
            "ID": ID,
        }

        self.call_action("RemoveRemoteDevices", arguments=arguments, aspects=aspects)

        return

    def action_SetDDDLocation(self, DDDLocation, ID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDDDLocation action.
        """
        arguments = {
            "DDDLocation": DDDLocation,
            "ID": ID,
        }

        self.call_action("SetDDDLocation", arguments=arguments, aspects=aspects)

        return
