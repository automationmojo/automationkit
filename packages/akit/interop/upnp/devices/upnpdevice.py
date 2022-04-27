"""
.. module:: upnpdevice
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`UpnpDevice` class and associated diagnostic.

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

from typing import Optional, Union, TYPE_CHECKING

import threading
import weakref

from xml.etree.ElementTree import fromstring as xml_fromstring
from xml.etree.ElementTree import Element

import requests

from akit.exceptions import AKitNotOverloadedError, AKitServiceUnAvailableError
from akit.extensible import generate_extension_key
from akit.paths import normalize_name_for_path

from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy
from akit.interop.upnp.xml.upnpdevice1 import UpnpDevice1Device

# Types imported only for type checking purposes
if TYPE_CHECKING:
    from akit.interop.upnp.upnpfactory import UpnpFactory

UPNP_SERVICE1_NAMESPACE = "urn:schemas-upnp-org:service-1-0"

class UpnpDevice:
    """
        The UPNP Root device is the base device for the hierarchy that is
        associated with a unique network devices location.  The :class:`RootDevice`
        and its subdevices are linked by thier location url.

        http://www.upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0.pdf
    """

    MANUFACTURER = "unknown"
    MODEL_NUMBER = "unknown"
    MODEL_DESCRIPTION = "unknown"

    def __init__(self):
        """
            Creates a root device object.
        """
        super(UpnpDevice, self).__init__()

        self._description = None
        self._host = None
        self._urlBase = None

        self._device_lock = threading.RLock()

        self._services_descriptions = {}
        self._services = {}

        return

    @property
    def description(self):
        """
            Returns the device description from the UPNP device.
        """
        return self._description

    @property
    def host(self):
        """
            Returns the host associated with the UPNP device.
        """
        return self._host

    @property
    def services(self):
        """
            Returns a list of service proxies associated with the UPNP device.
        """
        service_list = None

        self._device_lock.acquire()
        try:
            service_list = [svc for svc in self._services.values()]
        finally:
            self._device_lock.release()

        return service_list

    @property
    def services_descriptions(self):
        """
            Returns a table of service descriptions associated with the UPNP device.
        """
        return self._services_descriptions

    @property
    def URLBase(self):
        """
            Returns the base URL for the UPNP device that is used with any relative URLs in devices or service
            description documents.
        """
        return self._urlBase

    def get_service_description(self, service_type) -> Union[dict, None]:
        """
            Gets the service description for the specified service type.

            :param service_type: The service type to lookup the service description for.

            :returns: Returns the description information for the service type if found or None if not found.
        """
        svc_content = None

        devDesc = self.description

        for nxtsvc in devDesc.serviceList:
            if nxtsvc.serviceType == service_type:
                fullurl = self.URLBase.rstrip("/") + "/" + nxtsvc.SCPDURL.lstrip("/")

                resp = requests.get(fullurl)
                if resp.status_code == 200:
                    svc_content = resp.text
                    break

        return svc_content

    def lookup_service(self, serviceManufacturer: str, serviceType: str, allow_none: bool=False, factory: Optional["UpnpFactory"] = None) -> Union[UpnpServiceProxy, None]:
        """
            Looks up a service proxy based on the service manufacturer and service type specified.

            :param serviceManufacturer: The manufacturer associated with the device and service manufacturer.
            :param serviceType: The service type of the service to lookup.
            :param allow_none: If True, this API will not thrown an exception if the service cannot be found.

            :returns: The service proxy associated with the manufacturer and service type provided or None.
        """
        svc = None

        serviceManufacturer = normalize_name_for_path(serviceManufacturer)
        svckey = generate_extension_key(serviceManufacturer, serviceType)

        self._device_lock.acquire()
        try:
            if svckey in self._services:
                svc = self._services[svckey]
            elif factory is not None:
                self._device_lock.release()
                try:
                    svc = factory.create_service_instance(serviceManufacturer, serviceType)
                finally:
                    self._device_lock.acquire()

                if svc is not None:
                    self._services[svckey] = svc
        finally:
            self._device_lock.release()

        if svc is None and not allow_none:
            errmsg = "The service mfg={} serviceType={} was not found or is not available.".format(serviceManufacturer, serviceType)
            raise AKitServiceUnAvailableError(errmsg)

        return svc

    def to_dict(self, brief=False):
        """
            Creates a dictionary description of the device and its sub devices and services.
        """
        dval = None

        self._device_lock.acquire()
        try:
            desc = self._description

            if desc is not None:
                dval = desc.to_dict(brief=brief)

                dval["URLBase"] = self.URLBase

                if not brief:
                    serviceDescList = []
                    serviceList = dval["serviceList"]
                    for svc_info in serviceList:
                        svc_type = svc_info["serviceType"]
                        sdurl = self._urlBase.rstrip("/") + "/" + svc_info["SCPDURL"].lstrip("/")
                        sdesc = self._locked_process_full_service_description(sdurl)
                        sdesc["serviceType"] = svc_type
                        serviceDescList.append(sdesc)

                    dval["serviceDescriptionList"] = serviceDescList
        finally:
            self._device_lock.release()

        return dval

    def to_json(self, brief=False):
        """
            Creates a json description of the device and its sub devices and services.
        """
        json_str = None

        self._device_lock.acquire()
        try:
            desc = self._description

            if desc is not None:
                json_str = self._description.to_json(brief=brief)
        finally:
            self._device_lock.release()

        return json_str

    def _locked_populate_embedded_device_descriptions(self, factory: "UpnpFactory", description: UpnpDevice1Device):
        """
            Takes in a device description and processes it for embedded devices.

            :param factory: The UpnpFactory that has registered exentsion types that is used to instantiate
                            embedded devices when the UPNP device description is processed.
            :param description: The UpnpDevice1Device object that contains information about the device and its embedded devices.
        """
        # pylint: disable=no-self-use,unused-argument
        raise AKitNotOverloadedError("UpnpDevice._populate_embedded_devices: must be overridden.") from None

    def _locked_populate_services_descriptions(self, factory: "UpnpFactory", description: UpnpDevice1Device):
        """
            Takes in a device description and processes it for service descriptions.

            :param factory: The UpnpFactory that has registered exentsion types that is used to instantiate
                            services when the UPNP device description is processed.
            :param description: The UpnpDevice1Device object that contains information about the device and its services.
        """
        # pylint: disable=protected-access
        for serviceInfo in description.serviceList:
            serviceManufacturer = normalize_name_for_path(serviceInfo.serviceManufacturer)
            serviceType = serviceInfo.serviceType

            svckey = generate_extension_key(serviceManufacturer, serviceType)
            if serviceType not in self._services_descriptions:
                self._services_descriptions[svckey] = serviceInfo

                svc_inst = factory.create_service_instance(serviceManufacturer, serviceType)
                if svc_inst is not None:
                    device_ref = weakref.ref(self)
                    svc_inst._proxy_link_service_to_device(device_ref, serviceInfo)
                    self._services[svckey] = svc_inst
            else:
                svc_inst = self._services[svckey]

        return

    def _locked_process_full_service_description(self, sdurl: str):
        """
            Downloads and processes the service description document.

            :param sdurl: The url of the service description document to process.
        """
        svcdesc = None

        resp = requests.get(sdurl)
        if resp.status_code == 200:
            svcdesc = {}

            namespaces = {"": UPNP_SERVICE1_NAMESPACE}

            try:
                xml_content = resp.text
                descDoc = xml_fromstring(xml_content)

                specVersionNode = descDoc.find("specVersion", namespaces=namespaces)
                verInfo = self._locked_process_node_spec_version(specVersionNode, namespaces=namespaces)
                svcdesc["specVersion"] = verInfo

                serviceStateTableNode = descDoc.find("serviceStateTable", namespaces=namespaces)
                variablesTable, typesTable, eventsTable = self._locked_process_node_state_table(serviceStateTableNode, namespaces=namespaces)
                svcdesc["variablesTable"] = variablesTable
                svcdesc["typesTable"] = typesTable
                svcdesc["eventsTable"] = eventsTable

                actionListNode = descDoc.find("actionList", namespaces=namespaces)
                actionsTable = self._locked_process_node_action_list(actionListNode, namespaces=namespaces)
                svcdesc["actionsTable"] = actionsTable
            except:
                print("Service Description Failure: %s" % sdurl)
                raise

        return svcdesc

    def _locked_process_node_action_list(self, actionListNode: Element, namespaces: Optional[dict] = None) -> dict:
        """
            Processes the node action list and creates a dictionary of the actions supported by the service.

            :param actionListNode: The parent node for all the action list node.
            :param namespaces: A dictionary of namespaces to use when processing the XML.
        """
        # pylint: disable=no-self-use
        actionTable = {}

        actionNodeList = actionListNode.findall("action", namespaces=namespaces)
        for actionNode in actionNodeList:
            actionName = actionNode.find("name", namespaces=namespaces).text
            actionArgs = {}

            argumentListNode = actionNode.find("argumentList", namespaces=namespaces)
            if argumentListNode is not None:
                argumentNodeList = argumentListNode.findall("argument", namespaces=namespaces)
                for argumentNode in argumentNodeList:
                    argName = argumentNode.find("name", namespaces=namespaces).text
                    argDirection = argumentNode.find("direction", namespaces=namespaces).text

                    argRelStateVar = None
                    argRelStateNode = argumentNode.find("relatedStateVariable", namespaces=namespaces)
                    if argRelStateNode is not None:
                        argRelStateVar = argRelStateNode.text

                    actionArgs[argName] = {
                        "name": argName,
                        "direction": argDirection,
                        "relatedStateVariable": argRelStateVar
                        }

            actionTable[actionName] = {
                    "name": actionName,
                    "arguments" : actionArgs
                }

        return actionTable

    def _locked_process_node_spec_version(self, specVersionNode: Element, namespaces: Optional[dict] = None) -> dict:
        # pylint: disable=no-self-use
        verInfo = {}

        verInfo["major"] = specVersionNode.find("major", namespaces=namespaces).text
        verInfo["minor"] = specVersionNode.find("minor", namespaces=namespaces).text

        return verInfo

    def _locked_process_node_state_table(self, serviceStateTableNode: Element, namespaces: Optional[dict] = None) -> dict:
        # pylint: disable=no-self-use
        variablesTable = {}
        typesTable = {}
        eventsTable = {}

        stateVariableList = serviceStateTableNode.findall("stateVariable", namespaces=namespaces)
        for stateVariableNode in stateVariableList:
            name = stateVariableNode.find("name", namespaces=namespaces).text
            dataType = stateVariableNode.find("dataType", namespaces=namespaces).text

            varInfo = { "name": name, "dataType": dataType}
            if name.startswith("A_ARG_TYPE_"):
                typesTable[name] = varInfo
            else:
                variablesTable[name] = varInfo

                sendEvents = "no"
                if "sendEvents" in stateVariableNode.attrib:
                    sendEvents = stateVariableNode.attrib["sendEvents"]

                if sendEvents == "yes":
                    eventsTable[name] = varInfo

        return variablesTable, typesTable, eventsTable
