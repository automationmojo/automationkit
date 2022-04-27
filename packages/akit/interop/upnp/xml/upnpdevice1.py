"""
.. module:: upnpdevice1
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the XML classes used to process the XML content in a UpnpDevice1
               description document.

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

from typing import List, Optional, Union

import json

from xml.etree.ElementTree import tostring as xml_tostring
from xml.etree.ElementTree import register_namespace
from xml.etree.ElementTree import Element

from akit.exceptions import AKitNotOverloadedError


UPNP_DEVICE1_NAMESPACE = "urn:schemas-upnp-org:device-1-0"
UPNP_DEVICE1_TAG_PREFIX = "{urn:schemas-upnp-org:device-1-0}"


class UpnpDevice1ElementTags:
    """
        Contains constanst for the UpnpDevice1 XML element tag names.
    """
    deviceType = UPNP_DEVICE1_TAG_PREFIX + "deviceType"
    friendlyName = UPNP_DEVICE1_TAG_PREFIX + "friendlyName"
    manufacturer = UPNP_DEVICE1_TAG_PREFIX + "manufacturer"
    manufacturerURL = UPNP_DEVICE1_TAG_PREFIX + "manufacturerURL"
    modelDescription = UPNP_DEVICE1_TAG_PREFIX + "modelDescription"
    modelName = UPNP_DEVICE1_TAG_PREFIX + "modelName"
    modelNumber = UPNP_DEVICE1_TAG_PREFIX + "modelNumber"
    modelURL = UPNP_DEVICE1_TAG_PREFIX + "modelURL"
    serialNumber = UPNP_DEVICE1_TAG_PREFIX + "serialNumber"
    UDN = UPNP_DEVICE1_TAG_PREFIX + "UDN"
    UPC = UPNP_DEVICE1_TAG_PREFIX + "UPC"
    presentationURL = UPNP_DEVICE1_TAG_PREFIX + "presentationURL"
    deviceList = UPNP_DEVICE1_TAG_PREFIX + "deviceList"
    iconList = UPNP_DEVICE1_TAG_PREFIX + "iconList"
    serviceList = UPNP_DEVICE1_TAG_PREFIX + "serviceList"


class UpnpDevice1ElementBase:
    """
        The :class:`UpnpDevice1ElementBase` object provides a place to hang common data and
        methods for elements from the UpnpDevice1 document elements.
    """

    def __init__(self, ref_node: Element, namespaces: Optional[dict] = None):
        """
            Constructs a :class:`UpnpDevice1ElementBase` derived object initializing the
            reference node and namespace dictionary used for XML document processing.

            :param ref_node: The XML :class:`Element` node associated from the device description.
            :param namespaces: A dictionary of namespaces to use when processing the XML elements.
        """
        self._ref_node = ref_node
        self._namespaces = namespaces
        return

    @property
    def xmlNode(self) -> Element:
        """
            The XML node associated with the icon information.
        """
        return self._ref_node

    def to_dict(self, brief=False) -> dict:
        """
            Converts the icon data to a python dictionary.
        """
        # pylint: disable=no-self-use, unused-argument
        raise AKitNotOverloadedError("UpnpDevice1Base.to_dict: Must be overridden by derived classes.") from None

    def to_json(self) -> str:
        """
            Converts the icon data to a dictionary and then converts it to a JSON string.
        """
        dval = self.to_dict()
        json_str = json.dumps(dval, indent=4)
        return json_str

    def _find_value(self, path, namespaces) -> Union[str, None]:
        """
            Lookup a node using the path specified and then get its text value.

            :param path: The path to the node that is being found.
            :param namespaces: A dictionary of namespaces to use when processing the XML elements.

            :returns: The text value of the node associated with the specified path or None.
        """
        # pylint: disable=broad-except
        rtnval = None

        try:
            valNode = self._ref_node.find(path, namespaces=namespaces)
            if valNode is not None:
                rtnval = valNode.text
        except Exception as err:
            print(str(err))
            register_namespace('', None)
            xmlcontent = xml_tostring(self._ref_node)
            print(xmlcontent)
            print("")

        return rtnval



class UpnpDevice1Icon(UpnpDevice1ElementBase):
    """
        The :class:`UpnpDevice1Icon` object is used to process the icon description portion of a device
        description document.

        .. code-block:: xml

            <icon>
                <id>0</id>
                <mimetype>image/png</mimetype>
                <width>48</width>
                <height>48</height>
                <depth>24</depth>
                <url>/img/icon-S18.png</url>
            </icon>

    """

    def __init__(self, iconNode: Element, namespaces: Optional[dict] = None):
        """
            Creates a :class:`UpnpDevice1Icon` object to provide a shell for processing
            `icon` element information from a device description document.

            :param iconNode: The XML :class:`Element` node associated from the icon description.
            :param namespaces: A dictionary of namespaces to use when processing the XML elements.
        """
        super(UpnpDevice1Icon, self).__init__(iconNode, namespaces=namespaces)
        return

    @property
    def depth(self) -> str:
        """
            The color depth in bits of the the icon.
        """
        rtnval = self._find_value("depth", namespaces=self._namespaces)
        return rtnval

    @property
    def height(self) -> str:
        """
            The height of the icon in pixels.
        """
        rtnval = self._find_value("height", namespaces=self._namespaces)
        return rtnval

    @property
    def id(self) -> str:
        """
            The id that is assciated with the icon in the icon list.
        """
        rtnval = self._find_value("id", namespaces=self._namespaces)
        return rtnval

    @property
    def url(self) -> str:
        """
            The full or relative url of the icon.  If the URL does not have a scheme and host then
            it is likely a relative URL.
        """
        rtnval = self._find_value("url", namespaces=self._namespaces)
        return rtnval

    @property
    def mimetype(self) -> str:
        """
            The mime-type of the icon.
        """
        rtnval = self._find_value("mimetype", namespaces=self._namespaces)
        return rtnval

    @property
    def width(self) -> str:
        """
            The width of the icon in pixels.
        """
        rtnval = self._find_value("width", namespaces=self._namespaces)
        return rtnval

    def to_dict(self, brief=False) -> dict:
        """
            Converts the icon data to a python dictionary.
        """
        # pylint: disable=unused-argument
        dval = {
            "depth": self.depth,
            "height": self.height,
            "id": self.id,
            "url": self.url,
            "mimetype": self.mimetype,
            "width": self.width
        }
        return dval


class UpnpDevice1Service(UpnpDevice1ElementBase):
    """
        The :class:`UpnpDevice1Service` object is used to process the service description items in the
        service description list from a device description document.

        .. code-block:: xml

            <service>
                <serviceType>urn:schemas-upnp-org:service:AlarmClock:1</serviceType>
                <serviceId>urn:upnp-org:serviceId:AlarmClock</serviceId>
                <controlURL>/AlarmClock/Control</controlURL>
                <eventSubURL>/AlarmClock/Event</eventSubURL>
                <SCPDURL>/xml/AlarmClock1.xml</SCPDURL>
            </service>

    """
    def __init__(self, svcManufacturer: str, svcNode: Element, namespaces: Optional[dict] = None):
        """
            Creates a :class:`UpnpDevice1Service` object to provide a shell for processing
            `service` element information from a device description document.

            :param svcManufacturer: The manufacturer associated with the device and service descriptions.
            :param svcNode: The XML :class:`Element` node associated from the service description.
            :param namespaces: A dictionary of namespaces to use when processing the XML elements.
        """
        super(UpnpDevice1Service, self).__init__(svcNode, namespaces=namespaces)

        self._svcManufacturer = svcManufacturer
        return

    @property
    def controlURL(self) -> str:
        """
            Returns the control URL which is the URL for action calls.
        """
        rtnval = self._find_value("controlURL", namespaces=self._namespaces)
        return rtnval

    @property
    def eventSubURL(self) -> str:
        """
            Returns the event sub URL which is utilized to subscribe to events.
        """
        rtnval = self._find_value("eventSubURL", namespaces=self._namespaces)
        return rtnval

    @property
    def SCPDURL(self) -> str:
        """
            Returns the service description URL.
        """
        rtnval = self._find_value("SCPDURL", namespaces=self._namespaces)
        return rtnval

    @property
    def serviceId(self) -> str:
        """
            Returns the service ID of the service.
        """
        rtnval = self._find_value("serviceId", namespaces=self._namespaces)
        return rtnval

    @property
    def serviceManufacturer(self) -> str:
        """
            Returns the manufacturer name of the service.
        """
        return self._svcManufacturer

    @property
    def serviceType(self) -> str:
        """
            Returns the service type of the service.
        """
        rtnval = self._find_value("serviceType", namespaces=self._namespaces)
        return rtnval

    def to_dict(self, brief=False) -> dict:
        """
            Converts the icon data to a python dictionary.
        """
        # pylint: disable=unused-argument
        dval = {
            "controlURL": self.controlURL,
            "eventSubURL": self.eventSubURL,
            "SCPDURL": self.SCPDURL,
            "serviceId": self.serviceId,
            "serviceManufacturer": self.serviceManufacturer,
            "serviceType": self.serviceType
        }

        return dval

class UpnpDevice1SpecVersion(UpnpDevice1ElementBase):
    """
        The :class:`UpnpDevice1SpecVersion` object is used to process the service description items in the
        service description list from a device description document.

        .. code-block:: xml

            <specVersion>
                <major>1</major>
                <minor>0</minor>
            </specVersion>

    """
    def __init__(self, verNode: Element, namespaces: Optional[dict] = None):
        """
            Creates a :class:`UpnpDevice1SpecVersion` object to provide a shell for processing
            `specVersion` element information from a device description document.

            :param svcManufacturer: The manufacturer associated with the device and service descriptions.
            :param svcNode: The XML :class:`Element` node associated from the service description.
            :param namespaces: A dictionary of namespaces to use when processing the XML elements.
        """
        super(UpnpDevice1SpecVersion, self).__init__(verNode, namespaces=namespaces)
        return

    @property
    def major(self) -> str:
        """
            Returns the major version of the device description.
        """
        rtnval = self._find_value("major", namespaces=self._namespaces)
        return rtnval

    @property
    def minor(self) -> str:
        """
            Returns the minor version of the device description.
        """
        rtnval = self._find_value("minor", namespaces=self._namespaces)
        return rtnval

    def to_dict(self, brief=False) -> dict:
        """
            Converts the icon data to a python dictionary.
        """
        # pylint: disable=unused-argument
        dval = {
            "major": self.major,
            "minor": self.minor
        }

        return dval


class UpnpDevice1Device(UpnpDevice1ElementBase):
    """
        The UPNP Root device is the base device for the hierarchy that is
        associated with a unique network devices location.  The :class:`RootDevice`
        and its subdevices are linked by thier location url.

        http://www.upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0.pdf

        .. code-block:: xml

            <device>
                <deviceType>urn:schemas-upnp-org:device:deviceType:v</deviceType>
                <friendlyName>short user-friendly title</friendlyName>
                <manufacturer>manufacturer name</manufacturer>
                <manufacturerURL>URL to manufacturer site</manufacturerURL>
                <modelDescription>long user-friendly title</modelDescription>
                <modelName>model name</modelName>
                <modelNumber>model number</modelNumber>
                <modelURL>URL to model site</modelURL>
                <serialNumber>manufacturer's serial number</serialNumber>
                <UDN>uuid:UUID</UDN>
                <UPC>Universal Product Code</UPC>
                <iconList>
                    <icon>
                    <mimetype>image/format</mimetype>
                    <width>horizontal pixels</width>
                    <height>vertical pixels</height>
                    <depth>color depth</depth>
                    <url>URL to icon</url>
                    </icon>
                    XML to declare other icons, if any, go here
                </iconList>
                <serviceList>
                    <service>
                        <serviceType>urn:schemas-upnp-org:service:serviceType:v</serviceType>
                        <serviceId>urn:upnp-org:serviceId:serviceID</serviceId>
                        <SCPDURL>URL to service description</SCPDURL>
                        <controlURL>URL for control</controlURL>
                        <eventSubURL>URL for eventing</eventSubURL>
                    </service>
                    Declarations for other services defined by a UPnP Forum working committee (if any)
                    go here Declarations for other services added by UPnP vendor (if any) go here
                </serviceList>
                <presentationURL>URL for presentation</presentationURL>
            </device>

    """

    def __init__(self, devNode: Element, namespaces: Optional[dict] = None):
        """
            Creates a :class:`UpnpDevice1Device` object to provide a shell for processing
            `device` element information from a device description document.

            :param devNode: The XML :class:`Element` node associated from the service description.
            :param namespaces: A dictionary of namespaces to use when processing the XML elements.
        """
        super(UpnpDevice1Device, self).__init__(devNode, namespaces=namespaces)
        return

    @property
    def deviceList(self) -> List['akit.interop.upnp.xml.upnpdevice1.UpnpDevice1Device']:
        """
            Returns a listing of any embedded device descriptions from the device description.
        """
        resultList = []
        listNode = self._ref_node.find("deviceList", namespaces=self._namespaces)
        if listNode is not None:
            resultList = [ UpnpDevice1Device(child, namespaces=self._namespaces) for child in listNode ]
        return resultList

    @property
    def iconList(self) -> List[UpnpDevice1Icon]:
        """
            Returns a listing of any icon descriptions from the device description.
        """
        resultList = []
        listNode = self._ref_node.find("iconList", namespaces=self._namespaces)
        if listNode is not None:
            resultList = [ UpnpDevice1Icon(child, namespaces=self._namespaces) for child in listNode ]
        return resultList

    @property
    def serviceList(self) -> List[UpnpDevice1Service]:
        """
            Returns a listing of any service descriptions from the device description.
        """
        manufacturer = self.manufacturer
        listNode = self._ref_node.find("serviceList", namespaces=self._namespaces)
        if listNode is not None:
            resultList = [ UpnpDevice1Service(manufacturer, child, namespaces=self._namespaces) for child in listNode ]
        return resultList

    @property
    def deviceType(self) -> str:
        """
            Returns the device type of the device.
        """
        rtnval = self._find_value("deviceType", namespaces=self._namespaces)
        return rtnval

    @property
    def friendlyName(self) -> str:
        """
            Returns the friendly name of the device.
        """
        rtnval = self._find_value("friendlyName", namespaces=self._namespaces)
        return rtnval

    @property
    def MACAddress(self) -> str:
        """
            Returns the MAC address of the device.
        """
        rtnval = self._find_value("MACAddress", namespaces=self._namespaces)
        return rtnval

    @property
    def manufacturer(self) -> str:
        """
            Returns the manufacturer name of the device.
        """
        rtnval = self._find_value("manufacturer", namespaces=self._namespaces)
        return rtnval

    @property
    def manufacturerURL(self) -> str:
        """
            Returns the manufacturer URL of the device.
        """
        rtnval = self._find_value("manufacturerURL", namespaces=self._namespaces)
        return rtnval

    @property
    def modelDescription(self) -> str:
        """
            Returns the model description of the device.
        """
        rtnval = self._find_value("modelDescription", namespaces=self._namespaces)
        return rtnval

    @property
    def modelName(self) -> str:
        """
            Returns the model name of the device.
        """
        rtnval = self._find_value("modelName", namespaces=self._namespaces)
        return rtnval

    @property
    def modelNumber(self) -> str:
        """
            Returns the model number of the device.
        """
        rtnval = self._find_value("modelNumber", namespaces=self._namespaces)
        return rtnval

    @property
    def modelURL(self) -> str:
        """
            Returns the model URL of the device.
        """
        rtnval = self._find_value("modelURL", namespaces=self._namespaces)
        return rtnval

    @property
    def serialNumber(self) -> str:
        """
            Returns the serial number of the device.
        """
        rtnval = self._find_value("serialNumber", namespaces=self._namespaces)
        return rtnval

    @property
    def UDN(self) -> str:
        """
            Returns the UDN of the device.
        """
        rtnval = self._find_value("UDN", namespaces=self._namespaces)
        return rtnval

    @property
    def UPC(self) -> str:
        """
            Returns the UPC of the device.
        """
        rtnval = self._find_value("UPC", namespaces=self._namespaces)
        return rtnval

    @property
    def presentationURL(self) -> str:
        """
            Returns the presentation URL of the device.
        """
        rtnval = self._find_value("presentationURL", namespaces=self._namespaces)
        return rtnval

    def to_dict(self, brief=False) -> dict:
        """
            Converts the icon data to a python dictionary.
        """
        dval = {}

        for nxt_child in self._ref_node:
            # We only use the generic value processing for
            # children that are singular
            if len(nxt_child) == 0:
                nxt_tag_full = nxt_child.tag
                start_index = nxt_tag_full.find("}") + 1
                nxt_tag = nxt_tag_full[start_index:]
                dval[nxt_tag] = nxt_child.text

        firstIcon = None
        if not brief:
            device_list = []
            for dvc in self.deviceList:
                lival = dvc.to_dict()
                device_list.append(lival)
            dval["deviceList"] = device_list

            icon_list = []
            for icon in self.iconList:
                lival = icon.to_dict()
                icon_list.append(lival)
                if firstIcon is None:
                    firstIcon = lival
            dval["iconList"] = icon_list

            service_list = []
            for svc in self.serviceList:
                lsval = svc.to_dict()
                service_list.append(lsval)
            dval["serviceList"] = service_list
        else:
            for icon in self.iconList:
                lival = icon.to_dict()
                if firstIcon is None:
                    firstIcon = lival
                    break

        dval["firstIcon"] = firstIcon

        return dval
