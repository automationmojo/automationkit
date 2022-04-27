
"""
.. module:: akit.interop.upnp.extensions.sonos.zps23
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

from akit.interop.upnp.devices.upnpdevice import UpnpDevice
from akit.interop.upnp.devices.upnprootdevice import UpnpRootDevice
from akit.interop.upnp.xml.upnpdevice1 import UpnpDevice1Device


from akit.interop.upnp.extensions.standard.rootdevices.sonos.sonosdevice import SonosDevice, SonosUpnpDevice1Device

from akit.interop.upnp.extensions.dynamic.services.SonosInc.alarmclock1serviceproxy import AlarmClock1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.audioin1serviceproxy import AudioIn1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.avtransport1serviceproxy import AVTransport1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.connectionmanager1serviceproxy import ConnectionManager1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.contentdirectory1serviceproxy import ContentDirectory1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.deviceproperties1serviceproxy import DeviceProperties1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.groupmanagement1serviceproxy import GroupManagement1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.grouprenderingcontrol1serviceproxy import GroupRenderingControl1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.htcontrol1serviceproxy import HTControl1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.musicservices1serviceproxy import MusicServices1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.qplay1serviceproxy import QPlay1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.queue1serviceproxy import Queue1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.renderingcontrol1serviceproxy import RenderingControl1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.systemproperties1serviceproxy import SystemProperties1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.virtuallinein1serviceproxy import VirtualLineIn1ServiceProxy
from akit.interop.upnp.extensions.dynamic.services.SonosInc.zonegrouptopology1serviceproxy import ZoneGroupTopology1ServiceProxy

class SonosPlayer(SonosDevice):
    """
    """

    SERVICE_NAMES = [
        AlarmClock1ServiceProxy.SERVICE_TYPE,
        AudioIn1ServiceProxy.SERVICE_TYPE,
        AVTransport1ServiceProxy.SERVICE_TYPE,
        ConnectionManager1ServiceProxy.SERVICE_TYPE,
        ContentDirectory1ServiceProxy.SERVICE_TYPE,
        DeviceProperties1ServiceProxy.SERVICE_TYPE,
        GroupManagement1ServiceProxy.SERVICE_TYPE,
        GroupRenderingControl1ServiceProxy.SERVICE_TYPE,
        HTControl1ServiceProxy.SERVICE_TYPE,
        MusicServices1ServiceProxy.SERVICE_TYPE,
        QPlay1ServiceProxy.SERVICE_TYPE,
        Queue1ServiceProxy.SERVICE_TYPE,
        RenderingControl1ServiceProxy.SERVICE_TYPE,
        SystemProperties1ServiceProxy.SERVICE_TYPE,
        VirtualLineIn1ServiceProxy.SERVICE_TYPE,
        ZoneGroupTopology1ServiceProxy.SERVICE_TYPE
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

    def serviceAlarmClock(self, allow_none: bool=False):
        svctype = 'urn:schemas-upnp-org:service:AlarmClock:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype, allow_none=allow_none)
        return svc

    def serviceAVTransport(self, allow_none: bool=False):
        svctype = 'urn:schemas-upnp-org:service:AVTransport:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype, allow_none=allow_none)
        return svc

    def serviceDeviceProperties(self, allow_none: bool=False):
        svctype = 'urn:schemas-upnp-org:service:DeviceProperties:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype, allow_none=allow_none)
        return svc

    def serviceGroupManagement(self, allow_none: bool=False):
        svctype = 'urn:schemas-upnp-org:service:GroupManagement:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype, allow_none=allow_none)
        return svc

    def serviceMusicService(self, allow_none: bool=False):
        svctype = 'urn:schemas-upnp-org:service:MusicService:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype, allow_none=allow_none)
        return svc

    def serviceSystemProperties(self, allow_none: bool=False):
        svctype = 'urn:schemas-upnp-org:service:SystemProperties:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype, allow_none=allow_none)
        return svc

    def serviceQPlay(self, allow_none: bool=False):
        svctype = 'urn:schemas-upnp-org:service:QPlay:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype, allow_none=allow_none)
        return svc

    def serviceZoneTopologyGroup(self, allow_none: bool=False):
        svctype = 'urn:schemas-upnp-org:service:ZoneTopologyGroup:1'
        svc = self.lookup_service(self.MANUFACTURER, svctype, allow_none=allow_none)
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
