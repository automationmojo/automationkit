"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class RADASync1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'RADASync1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:RADASync:1'

    SERVICE_EVENT_VARIABLES = {}

    def action_AddRemoteDevices(self, DeviceList, ID):
        """
            Calls the AddRemoteDevices action.
        """
        arguments = {
            "DeviceList": DeviceList,
            "ID": ID,
        }

        self._proxy_call_action("AddRemoteDevices", arguments=arguments)

        return

    def action_HeartbeatUpdate(self, ID):
        """
            Calls the HeartbeatUpdate action.
        """
        arguments = {
            "ID": ID,
        }

        self._proxy_call_action("HeartbeatUpdate", arguments=arguments)

        return

    def action_RemoveRemoteDevices(self, DeviceList, ID):
        """
            Calls the RemoveRemoteDevices action.
        """
        arguments = {
            "DeviceList": DeviceList,
            "ID": ID,
        }

        self._proxy_call_action("RemoveRemoteDevices", arguments=arguments)

        return

    def action_SetDDDLocation(self, DDDLocation, ID):
        """
            Calls the SetDDDLocation action.
        """
        arguments = {
            "DDDLocation": DDDLocation,
            "ID": ID,
        }

        self._proxy_call_action("SetDDDLocation", arguments=arguments)

        return
