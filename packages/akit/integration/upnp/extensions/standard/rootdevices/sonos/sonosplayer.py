
"""
.. module:: akit.integration.upnp.extensions.sonos.zps23
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the a Upnp device for a Sonos Zps23.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from akit.integration.upnp.devices.upnpdevice import UpnpDevice
from akit.integration.upnp.devices.upnprootdevice import UpnpRootDevice
from akit.integration.upnp.xml.upnpdevice1 import UpnpDevice1Device


from akit.integration.upnp.extensions.standard.rootdevices.sonos.sonosdevice import SonosDevice, SonosUpnpDevice1Device


class SonosPlayer(SonosDevice):
    """
    """

    SERVICE_NAME_ALARM_CLOCK = "urn:schemas-upnp-org:service:AlarmClock:1"
    SERVICE_NAME_DEVICE_PROPERTIES = "urn:schemas-upnp-org:service:DeviceProperties:1"
    SERVICE_NAME_GROUP_MANAGEMENT = "urn:schemas-upnp-org:service:GroupManagement:1"
    SERVICE_NAME_MUSIC_SERVICE = "urn:schemas-upnp-org:service:MusicService:1"
    SERVICE_NAME_SYSTEM_PROPERTIES = "urn:schemas-upnp-org:service:SystemProperties:1"
    SERVICE_NAME_QPLAY = "urn:schemas-upnp-org:service:QPlay:1"
    SERVICE_NAME_ZONE_TOPOLOGY_GROUP = "urn:schemas-upnp-org:service:ZoneTopologyGroup:1"

    SERVICE_NAMES = [
        SERVICE_NAME_ALARM_CLOCK,
        SERVICE_NAME_DEVICE_PROPERTIES,
        SERVICE_NAME_GROUP_MANAGEMENT,
        SERVICE_NAME_MUSIC_SERVICE,
        SERVICE_NAME_SYSTEM_PROPERTIES,
        SERVICE_NAME_QPLAY,
        SERVICE_NAME_ZONE_TOPOLOGY_GROUP
    ]

    def __init__(self, manufacturer: str, modelNumber: str, modelDescription: str):
        super(SonosPlayer, self).__init__(manufacturer, modelNumber, modelDescription)

        self._bood_id = None
        self._boot_seq = None
        self._household = None
        self._smart_speaker = None
        self._variant = None
        self._wifimode = None
        return

    @property
    def bootId(self):
        return self._bood_id

    @property
    def bootSeq(self):
        return self._boot_seq

    @property
    def household(self):
        return self._household

    @property
    def smartSpeaker(self):
        return self._smart_speaker

    @property
    def variant(self):
        return self._variant

    @property
    def wifiMode(self):
        return self._wifimode

    def deviceMediaRenderer(self):
        return

    def deviceMediaServer(self):
        return

    def getLedState(self):
        devprops = self.serviceDeviceProperties()
        rtnval = devprops.action_GetLEDState()
        return rtnval

    def serviceAlarmClock(self):
        svctype = 'urn:schemas-upnp-org:service:AlarmClock:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype)
        return svc

    def serviceDeviceProperties(self):
        svctype = 'urn:schemas-upnp-org:service:DeviceProperties:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype)
        return svc

    def serviceGroupManagement(self):
        svctype = 'urn:schemas-upnp-org:service:GroupManagement:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype)
        return svc

    def serviceMusicService(self):
        svctype = 'urn:schemas-upnp-org:service:MusicService:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype)
        return svc

    def serviceSystemProperties(self):
        svctype = 'urn:schemas-upnp-org:service:SystemProperties:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype)
        return svc

    def serviceQPlay(self):
        svctype = 'urn:schemas-upnp-org:service:QPlay:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype)
        return svc

    def serviceZoneTopologyGroup(self):
        svctype = 'urn:schemas-upnp-org:service:ZoneTopologyGroup:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype)
        return svc

    def _consume_upnp_extra(self, extrainfo):

        if "BOOTID.UPNP.ORG" in extrainfo:
            self._bood_id = extrainfo.pop("BOOTID.UPNP.ORG")
        if "X-RINCON-BOOTSEQ" in extrainfo:
            self._boot_seq = extrainfo.pop("X-RINCON-BOOTSEQ")
        if "X-RINCON-HOUSEHOLD" in extrainfo:
            self._household = extrainfo.pop("X-RINCON-HOUSEHOLD")
        if "HOUSEHOLD.SMARTSPEAKER.AUDIO" in extrainfo:
            self._smart_speaker = extrainfo.pop("HOUSEHOLD.SMARTSPEAKER.AUDIO")
        if "X-RINCON-VARIANT" in extrainfo:
            self._variant = extrainfo.pop("X-RINCON-VARIANT")
        if "X-RINCON-WIFIMODE" in extrainfo:
            self._wifimode = extrainfo.pop("X-RINCON-WIFIMODE")

        self._extra = extrainfo
        return

    def _create_device_description_node(self, devNode, namespaces=None):
        dev_desc_node = SonosUpnpDevice1Device(devNode, namespaces=namespaces)
        return dev_desc_node

    def _process_embedded_device_node(self, devNode, namespaces=None):
        dev = UpnpDevice1Device(devNode, namespaces=namespaces)
        return dev

    def _process_other_node(self, otherNode, namespaces=None):
        return

    def _process_servicelist_node(self, listNode, namespaces=None):
        super(SonosPlayer, self)._process_servicelist_node(listNode, namespaces=namespaces)
        return

    def to_dict(self, brief=False):
        dval = super(SonosPlayer, self).to_dict(brief=brief)

        dval["bootId"] = self.bootId
        dval["bootSeq"] = self.bootSeq
        dval["household"] = self.household
        dval["smartSpeaker"] = self.smartSpeaker
        dval["variant"] = self.variant
        dval["wifiMode"] = self.wifiMode

        return dval
