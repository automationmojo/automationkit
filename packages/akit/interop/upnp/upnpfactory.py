"""
.. module:: upnpfactory
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`UpnpFactory` class and associated diagnostic.

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

from typing import Union

from akit.exceptions import AKitSemanticError
from akit.extensible import generate_extension_key
from akit.compat import import_by_name

from akit.environment.variables import AKIT_VARIABLES

from akit.interop.upnp.devices.upnpembeddeddevice import UpnpEmbeddedDevice
from akit.interop.upnp.devices.upnprootdevice import UpnpRootDevice
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

from akit.interop.upnp.extensions import standard as standard_extensions

from akit.extensible import collect_extensions_under_code_container, collect_extensions_under_folder

class UpnpFactory:
    """
        The :class:`UpnpFactory` object is a singleton object that manages the cataloging and instantiation
        of code generated UPnP device and service extensions.  We utilize code generated device classes and
        service proxy classes because that makes each class of device and each method on those classes
        individually isolatable and debugable.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """
            Constructs new instances of the UpnpFactory object from the :class:`UpnpDeviceFactory`.
            This is a singlton object that is used to register and instantiate UPNP devices based on
            their devicetype id.
        """
        if cls._instance is None:
            cls._instance = super(UpnpFactory, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
            Initializes the Singleton initializer class
        """
        thisType = type(self)
        if not thisType._initialized:
            thisType._initialized = True

            self._dyn_embedded_device_registry = {}
            self._dyn_root_device_registry = {}
            self._dyn_service_registry = {}
            self._std_embedded_device_registry = {}
            self._std_root_device_registry = {}
            self._std_service_registry = {}

            dyn_ext_module = None
            dyn_ext_module_name = AKIT_VARIABLES.AKIT_UPNP_DYN_EXTENSIONS_MODULE
            if dyn_ext_module_name is not None:
                dyn_ext_module = import_by_name(dyn_ext_module_name)

            dyn_ext_folder = AKIT_VARIABLES.AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE

            if dyn_ext_module is not None:
                self._scan_for_device_extensions_under_code_container(dyn_ext_module, self._dyn_root_device_registry)
                self._scan_for_service_extensions_under_code_container(dyn_ext_module, self._dyn_service_registry)
            elif dyn_ext_folder is not None:
                self._scan_for_device_extensions_under_folder(dyn_ext_folder, self._dyn_root_device_registry)
                self._scan_for_service_extensions_under_folder(dyn_ext_folder, self._dyn_service_registry)
            
            self._scan_for_device_extensions_under_code_container(standard_extensions, self._std_root_device_registry)
            self._scan_for_service_extensions_under_code_container(standard_extensions, self._std_service_registry)
        return

    def create_embedded_device_instance(self, manufacturer:str, modelNumber: str, modelDescription: str) -> UpnpEmbeddedDevice:
        """
            Method that is called to create an instance of an extension for a specific UPnP embedded device. If an
            embedded device extension is not found matching the specified parameters then a generic UpnpEmbeddedDevice
            instance is created and returned.

            :param manufacturer: The manufacturer associated with the embedded device.
            :param modelNumber: The model number associated with the embedded device.
            :param modelDescription: The model description associated with the embedded device.

            :returns: An instance of an embedded device extension of a specific manaufacturer or a default generic
                      UpnpEmbeddedDevice.
        """
        deviceClass = UpnpEmbeddedDevice
        extkey = generate_extension_key(manufacturer, modelNumber, modelDescription)
        if extkey in self._dyn_embedded_device_registry:
            deviceClass = self._dyn_embedded_device_registry[extkey]
        elif extkey in self._std_embedded_device_registry:
            deviceClass = self._std_embedded_device_registry[extkey]
        return deviceClass()

    def create_root_device_instance(self, manufacturer:str, modelNumber: str, modelDescription: str) -> UpnpRootDevice:
        """
            Method that is called to create an instance of an extension for a specific UPnP root device.  If a device
            extension is not found matching the specified parameters then a generic UpnpRootDevice instance is
            created and returned.

            :param manufacturer: The manufacturer associated with the root device.
            :param modelNumber: The model number associated with the root device.
            :param modelDescription: The model description associated with the root device.

            :returns: An instance of an root device extension of a specific manaufacturer or a default generic
                      UpnpRootDevice.
        """
        deviceClass = UpnpRootDevice

        if manufacturer is not None and modelNumber is not None and modelDescription is not None:
            extkey = generate_extension_key(manufacturer, modelNumber, modelDescription)
            if extkey in self._dyn_root_device_registry:
                deviceClass = self._dyn_root_device_registry[extkey]
            elif extkey in self._std_root_device_registry:
                deviceClass = self._std_root_device_registry[extkey]

        dev_inst = deviceClass(manufacturer, modelNumber, modelDescription)
        return dev_inst

    def create_service_instance(self, serviceManufacturer, serviceType) -> Union[UpnpServiceProxy, None]:
        """
            Method that is called to create an instance of an extension for a specific UPnP service proxy.  If a
            service proxy extension is not found matching the specified parameters then None is returned.

            :param manufacturer: The manufacturer associated with the root device.
            :param modelNumber: The model number associated with the root device.
            :param modelDescription: The model description associated with the root device.

            :returns: An instance of an root device extension of a specific manaufacturer or a default generic
                      UpnpRootDevice.
        """
        serviceInst = None
        if serviceType is not None:
            extkey = generate_extension_key(serviceManufacturer, serviceType)
            if extkey in self._dyn_service_registry:
                serviceClass = self._dyn_service_registry[extkey]
                serviceInst = serviceClass()
            elif extkey in self._std_service_registry:
                serviceClass = self._std_service_registry[extkey]
                serviceInst = serviceClass()
        return serviceInst

    def _register_root_device(self, extkey, extcls, device_table):
        """
            Method that registers the extension class of a specific type of root device.
        """
        if extkey not in device_table:
            device_table[extkey] = extcls
        else:
            raise AKitSemanticError("A root device extension with the key=%r was already registered. (%s)" % (extkey, extcls)) from None
        return

    def _register_service(self, extkey, extcls, service_table):
        """
            Method that registers the extension class of a specific type of service proxy.
        """
        if extkey not in service_table:
            service_table[extkey] = extcls
        else:
            service_table[extkey] = extcls
        return

    def _scan_for_device_extensions_under_code_container(self, container, device_table):
        """
            Method that scans a code container and its descendants for UpnpRootDevice objects.
        """
        extcoll = collect_extensions_under_code_container(container, UpnpRootDevice)
        for _, extcls in extcoll:
            if hasattr(extcls, "MANUFACTURER") and hasattr(extcls, "MODEL_NUMBER") and hasattr(extcls, "MODEL_DESCRIPTION"):
                extkey = generate_extension_key(getattr(extcls, "MANUFACTURER"),
                    getattr(extcls, "MODEL_NUMBER"), getattr(extcls, "MODEL_DESCRIPTION"))
                self._register_root_device(extkey, extcls, device_table)
        return

    def _scan_for_service_extensions_under_code_container(self, container, service_table):
        """
            Method that scans a code container and its descendants for UpnpServiceProxy objects.
        """
        extcoll = collect_extensions_under_code_container(container, UpnpServiceProxy)
        for _, extcls in extcoll:
            if (hasattr(extcls, "SERVICE_MANUFACTURER") and hasattr(extcls, "SERVICE_TYPE")):
                svc_manufacturer = getattr(extcls, "SERVICE_MANUFACTURER")
                svc_type = getattr(extcls, "SERVICE_TYPE")
                extkey = generate_extension_key(svc_manufacturer, svc_type)
                self._register_service(extkey, extcls, service_table)
        return
    
    def _scan_for_device_extensions_under_folder(self, directory, device_table):
        """
            Method that scans a code container and its descendants for UpnpRootDevice objects.
        """
        extcoll = collect_extensions_under_folder(directory, UpnpRootDevice)
        for _, extcls in extcoll:
            if hasattr(extcls, "MANUFACTURER") and hasattr(extcls, "MODEL_NUMBER") and hasattr(extcls, "MODEL_DESCRIPTION"):
                extkey = generate_extension_key(getattr(extcls, "MANUFACTURER"),
                    getattr(extcls, "MODEL_NUMBER"), getattr(extcls, "MODEL_DESCRIPTION"))
                self._register_root_device(extkey, extcls, device_table)
        return

    def _scan_for_service_extensions_under_folder(self, directory, service_table):
        """
            Method that scans a code container and its descendants for UpnpServiceProxy objects.
        """
        extcoll = collect_extensions_under_folder(directory, UpnpServiceProxy)
        for _, extcls in extcoll:
            if (hasattr(extcls, "SERVICE_MANUFACTURER") and hasattr(extcls, "SERVICE_TYPE")):
                svc_manufacturer = getattr(extcls, "SERVICE_MANUFACTURER")
                svc_type = getattr(extcls, "SERVICE_TYPE")
                extkey = generate_extension_key(svc_manufacturer, svc_type)
                self._register_service(extkey, extcls, service_table)
        return
