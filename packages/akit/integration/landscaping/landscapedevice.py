"""
.. module:: landscapedevice
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`TestLandscape` class and associated diagnostic.

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


import threading
import weakref

from dlipower import PowerSwitch

from akit.exceptions import AKitConfigurationError
from akit.xlogging.foundations import getAutomatonKitLogger
class LandscapeDevice:
    """
        The base class for all landscape devices.  The :class:`LandscapeDevice' represents attributes that are common
        to all connected devices and provides attachements points and mechanisms for adding DeviceExtentions to
        the :class:`LandscapeDevice` device.
    """

    logger = getAutomatonKitLogger()

    def __init__(self, lscape, keyid, device_type, device_config):
        self._lscape_ref = weakref.ref(lscape)
        self._keyid = keyid
        self._device_type = device_type
        self._device_config = device_config
        self._device_lock = threading.RLock()

        self._contacted_first = None
        self._contacted_last = None
        self._is_watched = None
        self._is_isolated = None

        self._upnp = None
        self._muse = None
        self._ssh = None
        self._power = None
        self._serial = None

        self._match_functions = {}

        self._credentials = {}
        self._ssh_credentials = []
        if "credentials" in device_config:
            lscape_credentials = lscape.credentials
            for cred_key in device_config["credentials"]:
                if cred_key in lscape_credentials:
                    cred_info = lscape_credentials[cred_key]
                    self._credentials[cred_key] = cred_info
                    if cred_info.category == "ssh":
                        self._ssh_credentials.append(cred_info)

        return

    @property
    def contacted_first(self):
        """
            A datetime stamp of when this device was first contacted
        """
        return self._contacted_first

    @property
    def contacted_last(self):
        """
            A datetime stamp of when this device was last contacted
        """
        return self._contacted_last

    @property
    def device_config(self):
        """
            A dictionary of the configuration information for this device.
        """
        return self._device_config

    @property
    def device_lock(self):
        """
            Returns the lock for the device.
        """
        return self._device_lock

    @property
    def device_type(self):
        """
            A string representing the type of device.
        """
        return self._device_type

    @property
    def has_ssh_credential(self):
        """
            A boolean value indicating whether this device has an SSH credential.
        """
        has_creds = len(self._ssh_credentials) > 0
        return has_creds

    @property
    def is_watched(self):
        """
            A boolean indicating if this device is a watched device.
        """
        return self._is_watched

    @property
    def keyid(self):
        """
            The key identifier for this device, this is generally the identifier provided
            by the coordinator that created the device instance.
        """
        return self._keyid

    @property
    def landscape(self):
        """
            Returns a strong reference to the the landscape object
        """
        return self._lscape_ref()

    @property
    def muse(self):
        """
            The 'Muse' :class:`LandscapeDeviceExtension` attached to this device or None.
        """
        return self._muse

    @property
    def power(self):
        """
            The power agent associated with this device.
        """
        return self._power

    @property
    def serial(self):
        """
            The serial agent associated with this device.
        """
        return self._serial

    @property
    def ssh(self):
        """
            The 'SSH' :class:`LandscapeDeviceExtension` attached to this device or None.
        """
        return self._ssh

    @property
    def ssh_credentials(self):
        """
            The list of SSH credentials associated with this device
        """
        return self._ssh_credentials

    @property
    def upnp(self):
        """
            The 'UPnP' :class:`LandscapeDeviceExtension` attached to this device or None.
        """
        return self._upnp

    def attach_extension(self, ext_type, extension):
        """
            Method called by device coordinators to attach a device extension to a :class:`LandscapeDevice`.
        """
        setattr(self, "_" + ext_type, extension)
        return

    def checkout(self):
        """
            Method that makes it convenient to checkout device.
        """
        self.landscape.checkout_device(self)
        return

    def checkin(self):
        """
            Method that makes it convenient to checkin a device.
        """
        self.landscape.checkin_device(self)
        return

    def match_using_params(self, match_type, *match_params):
        """
            Method that allows you to match :class:`LandscapeDevice` objects by providing a match_type and
            parameters.  The match type is mapped to functions that are registered by device coordinators
            and then the function is called with the match parameters to determine if a device is a match.
        """
        matches = False
        match_func = None
        match_self = None

        self._device_lock.acquire()
        try:
            if match_type in self._match_functions:
                dext_attr, match_func = self._match_functions[match_type]
                match_self = None
                if hasattr(self, dext_attr):
                    match_self = getattr(self, dext_attr)
        finally:
            self._device_lock.release()

        if match_self is not None and match_func is not None:
            matches = match_func(match_self, *match_params)

        return matches

    def update_match_table(self, match_table: dict):
        """
            Method called  to update the match functions.
        """
        self._device_lock.acquire()
        try:
            self._match_functions.update(match_table)
        finally:
            self._device_lock.release()

        return

    def initialize_features(self):
        """
            Initializes the features of the device based on the feature declarations and the information
            found in the feature config.
        """
        if "features" in self._device_config:
            feature_info = self._device_config["features"]
            for fkey, fval in feature_info.items():
                if fkey == "isolation":
                    self._is_isolated = fval
                elif fkey == "power":
                    self._intitialize_power(fval)
                elif fkey == "serial":
                    self._intitialize_serial(fval)
                elif fkey == "":
                    pass
        return

    def _intitialize_power(self, power_mapping): # pylint: disable=no-self-use
        """
            Initializes the serial port connectivity for this device.
        """
        lscape = self._lscape_ref()
        self._power = lscape.lookup_power_agent(power_mapping)
        return

    def _intitialize_serial(self, serial_mapping): # pylint: disable=no-self-use
        """
            Initializes the serial port connectivity for this device.
        """
        #lscape = self._lscape_ref()
        #self._serial = lscape.lookup_serial_agent(serial_mapping)
        return
