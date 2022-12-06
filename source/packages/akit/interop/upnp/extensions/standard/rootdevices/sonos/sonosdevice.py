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

from akit.interop.upnp.devices.upnprootdevice import UpnpRootDevice

from akit.interop.upnp.xml.upnpdevice1 import UpnpDevice1Device

class SonosUpnpDevice1Device(UpnpDevice1Device):
    """
    """

    @property
    def ampOnTime(self):
        rtnval = self._find_value("ampOnTime", namespaces=self._namespaces)
        return rtnval

    @property
    def apiVersion(self):
        rtnval = self._find_value("apiVersion", namespaces=self._namespaces)
        return rtnval

    @property
    def bassExtension(self):
        rtnval = self._find_value("bassExtension", namespaces=self._namespaces)
        return rtnval

    @property
    def displayName(self):
        rtnval = self._find_value("displayName", namespaces=self._namespaces)
        return rtnval

    @property
    def displayVersion(self):
        rtnval = self._find_value("displayVersion", namespaces=self._namespaces)
        return rtnval

    @property
    def extraVersion(self):
        rtnval = self._find_value("extraVersion", namespaces=self._namespaces)
        return rtnval

    @property
    def feature1(self):
        rtnval = self._find_value("feature1", namespaces=self._namespaces)
        return rtnval

    @property
    def feature2(self):
        rtnval = self._find_value("feature2", namespaces=self._namespaces)
        return rtnval

    @property
    def feature3(self):
        rtnval = self._find_value("feature3", namespaces=self._namespaces)
        return rtnval

    @property
    def flash(self):
        rtnval = self._find_value("flash", namespaces=self._namespaces)
        return rtnval

    @property
    def hardwareVersion(self):
        rtnval = self._find_value("hardwareVersion", namespaces=self._namespaces)
        return rtnval

    @property
    def internalSpeakerSize(self):
        rtnval = self._find_value("internalSpeakerSize", namespaces=self._namespaces)
        return rtnval

    @property
    def legacyCompatibleVersion(self):
        rtnval = self._find_value("legacyCompatibleVersion", namespaces=self._namespaces)
        return rtnval

    @property
    def memory(self):
        rtnval = self._find_value("memory", namespaces=self._namespaces)
        return rtnval

    @property
    def minApiVersion(self):
        rtnval = self._find_value("minApiVersion", namespaces=self._namespaces)
        return rtnval

    @property
    def minCompatibleVersion(self):
        rtnval = self._find_value("minCompatibleVersion", namespaces=self._namespaces)
        return rtnval

    @property
    def retailMode(self):
        rtnval = self._find_value("retailMode", namespaces=self._namespaces)
        return rtnval

    @property
    def roomName(self):
        rtnval = self._find_value("roomName", namespaces=self._namespaces)
        return rtnval

    @property
    def satGainOffset(self):
        rtnval = self._find_value("satGainOffset", namespaces=self._namespaces)
        return rtnval

    @property
    def seriesid(self):
        rtnval = self._find_value("seriesid", namespaces=self._namespaces)
        return rtnval

    @property
    def softwareVersion(self):
        rtnval = self._find_value("softwareVersion", namespaces=self._namespaces)
        return rtnval

    @property
    def swGen(self):
        rtnval = self._find_value("swGen", namespaces=self._namespaces)
        return rtnval

    @property
    def variant(self):
        rtnval = self._find_value("variant", namespaces=self._namespaces)
        return rtnval

    @property
    def zoneType(self):
        rtnval = self._find_value("zoneType", namespaces=self._namespaces)
        return rtnval


class SonosDevice(UpnpRootDevice):
    """
    """

    MANUFACTURER = "SonosInc"

    def __init__(self, manufacturer: str, modelNumber: str, modelDescription: str):
        super(SonosDevice, self).__init__(manufacturer, modelNumber, modelDescription)
        return


