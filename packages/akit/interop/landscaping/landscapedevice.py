"""
.. module:: landscapedevice
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`LandscapeDevice` class.

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

from typing import FrozenSet, List, Union, TYPE_CHECKING

import bisect
import os
import threading
import weakref

from datetime import datetime

from akit.exceptions import AKitRuntimeError, AKitSemanticError
from akit.interfaces.icommandrunner import ICommandRunner
from akit.interop.landscaping.featuretag import FeatureTag

from akit.xlogging.foundations import getAutomatonKitLogger

if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape
    from akit.interop.landscaping.landscapedeviceextension import LandscapeDeviceExtension
    from akit.interop.agents.sshagent import SshAgent
    from akit.interop.upnp.devices.upnprootdevice import UpnpRootDevice

class LandscapeDevice:
    """
        The base class for all landscape devices.  The :class:`LandscapeDevice' represents attributes that are common
        to all connected devices and provides attachements points and mechanisms for adding DeviceExtentions to
        the :class:`LandscapeDevice` device.
    """

    # Base landscape devices don't have any feature tags, but we want all devices to have feature
    # tag capability so we can filter all devices based on feature tags, whether they have
    # tags or not.
    FEATURE_TAGS = []

    logger = getAutomatonKitLogger()

    def __init__(self, lscape: "Landscape", keyid: str, device_type: str, device_config: dict):
        self._lscape_ref = weakref.ref(lscape)
        self._keyid = keyid
        self._device_type = device_type
        self._device_config = device_config
        self._device_lock = threading.RLock()

        self._contacted_first = None
        self._contacted_last = None
        self._is_watched = None
        self._is_isolated = None

        self._upnp: "UpnpRootDevice" = None
        self._ssh: "SshAgent" = None
        self._power = None
        self._serial = None

        self._preferred_command_interface = "ssh"
 
        self._feature_tags = []

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
    def contacted_first(self) -> datetime:
        """
            A datetime stamp of when this device was first contacted
        """
        return self._contacted_first

    @property
    def contacted_last(self) -> datetime:
        """
            A datetime stamp of when this device was last contacted
        """
        return self._contacted_last

    @property
    def device_config(self) -> dict:
        """
            A dictionary of the configuration information for this device.
        """
        return self._device_config

    @property
    def device_lock(self) -> threading.RLock:
        """
            Returns the lock for the device.
            
            ..note: Use with caution
        """
        return self._device_lock

    @property
    def device_type(self) -> str:
        """
            A string representing the type of device.
        """
        return self._device_type

    @property
    def feature_tags(self) -> FrozenSet[str]:
        return frozenset(self._feature_tags)

    @property
    def has_ssh_credential(self) -> bool:
        """
            A boolean value indicating whether this device has an SSH credential.
        """
        has_creds = len(self._ssh_credentials) > 0
        return has_creds

    @property
    def ipaddr(self):
        """
            The device IP of the device, if available.
        """
        ipaddr = self._resolve_ipaddress()
        return ipaddr

    @property
    def is_watched(self) -> bool:
        """
            A boolean indicating if this device is a watched device.
        """
        return self._is_watched

    @property
    def keyid(self) -> bool:
        """
            The key identifier for this device, this is generally the identifier provided
            by the coordinator that created the device instance.
        """
        return self._keyid

    @property
    def landscape(self) -> "Landscape":
        """
            Returns a strong reference to the the landscape object
        """
        return self._lscape_ref()

    @property
    def power(self) -> "LandscapeDeviceExtension":
        """
            The power agent associated with this device.
        """
        return self._power

    @property
    def serial(self) -> "LandscapeDeviceExtension":
        """
            The serial agent associated with this device.
        """
        return self._serial

    @property
    def ssh(self) -> "SshAgent":
        """
            The 'SSH' :class:`SshAgent` attached to this device or None.
        """
        return self._ssh

    @property
    def ssh_credentials(self):
        """
            The list of SSH credentials associated with this device
        """
        return self._ssh_credentials

    @property
    def upnp(self) -> "UpnpRootDevice":
        """
            The 'UPnP' :class:`UpnpRootDevice` attached to this device or None.
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

    def extend_features(self, features_to_add: Union[List[FeatureTag], List[str]]):
        """
            Used by derived class and mixins to extend the feature tags associated with
            a devices.
        """

        if len(features_to_add) > 0:
            first_item = features_to_add[0]
            if isinstance(first_item, str):
                # We insert the features into the list sorted so we can make finding
                # features faster.
                for ft in features_to_add:
                    bisect.insort(self._feature_tags, ft)
            elif issubclass(first_item, FeatureTag):
                # We insert the features into the list sorted so we can make finding
                # features faster.
                for ft in features_to_add:
                    bisect.insort(self._feature_tags, ft.ID)
            else:
                errmsg = "The 'features_to_add' parameter must contain items of type 'FeatureTag' or 'str'. item={}".format(
                    repr(first_item)
                )
                raise AKitSemanticError(errmsg)

        return

    def get_preferred_command_runner(self) -> ICommandRunner:
        """
            Gets the preferred command runner interface for this device.
        """
        cmd_runner = None

        if self._preferred_command_interface == "ssh":
            if hasattr(self, "ssh") and self.ssh is not None:
                cmd_runner = self.ssh
            elif hasattr(self, "serial") and self.serial is not None:
                cmd_runner = self.serial
        elif self._preferred_command_interface == "serial":
            if hasattr(self, "serial") and self.serial is not None:
                cmd_runner = self.serial
            elif hasattr(self, "ssh") and self.ssh is not None:
                cmd_runner = self.ssh
        else:
            errmsg = "Unknown command runner interface '{}'".format(self._preferred_command_interface)
            raise AKitRuntimeError(errmsg)

        return cmd_runner

    def has_all_features(self, feature_list: Union[List[FeatureTag], List[str]]):
        has_all = True

        if len(feature_list) == 0:
            errmsg = "has_all_features: 'feature_list' cannot be empty."
            raise AKitSemanticError(errmsg)

        first_item = feature_list[0]
        if isinstance(first_item, str):
            for feature in feature_list:
                fid = feature
                hasfeature = fid in self._feature_tags
                if not hasfeature:
                    has_all = False
                    break
        elif issubclass(first_item, FeatureTag):
            for feature in feature_list:
                fid = feature.ID
                hasfeature = fid in self._feature_tags
                if not hasfeature:
                    has_all = False
                    break
        else:
            errmsg = "The 'feature_list' parameter must contain items of type 'FeatureTag' or 'str'. item={}".format(
                repr(first_item)
            )
            raise AKitSemanticError(errmsg)

        return has_all

    def has_any_feature(self, feature_list: List[FeatureTag]):
        has_any = False

        if len(feature_list) == 0:
            errmsg = "has_all_features: 'feature_list' cannot be empty."
            raise AKitSemanticError(errmsg)

        first_item = feature_list[0]
        if isinstance(first_item, str):
            for feature in feature_list:
                fid = feature

                hasfeature = fid in self._feature_tags
                if hasfeature:
                    has_any = True
                    break
        elif issubclass(first_item, FeatureTag):
            for feature in feature_list:
                fid = feature.ID

                hasfeature = fid in self._feature_tags
                if hasfeature:
                    has_any = True
                    break
        else:
            errmsg = "The 'feature_list' parameter must contain items of type 'FeatureTag' or 'str'. item={}".format(
                repr(first_item)
            )
            raise AKitSemanticError(errmsg)

        return has_any

    def has_feature(self, feature: Union[FeatureTag, str]):
        fid = None

        if isinstance(feature, str):
            fid = feature
        elif issubclass(feature, FeatureTag):
            fid = feature.ID
        else:
            errmsg = "The 'feature' parameter must be of type 'FeatureTag' or 'str'. item={}".format(
                repr(feature)
            )
            raise AKitSemanticError(errmsg)

        hasfeature = fid in self._feature_tags
        return hasfeature

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

    def match_using_params(self, match_type, *match_params) -> bool:
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

    def set_preferred_command_interface(self, ifname: str):
        """
            Sets the name of the interface that is used as the preferred command runner.

            :param ifname: The name of the preferred commandline interface. (ssh, serial, etc.)
        """
        self._preferred_command_interface = ifname
        return

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

    def verify_status(self):
        """
            Verify the status of the specified device.
        """

        status = "Up"
        if self._upnp is not None:
            desc = self._upnp.query_device_description()
            if desc is None:
                status = "Down"

        elif self._ssh:
            cmd_status, _, _ = self._ssh.run_cmd("echo Hello")
            if cmd_status != 0:
                status = "Down"

        return status

    def _intitialize_power(self, power_mapping): # pylint: disable=no-self-use
        """
            Initializes the serial port connectivity for this device.
        """
        self._power = self.landscape.lookup_power_agent(power_mapping)
        return

    def _intitialize_serial(self, serial_mapping): # pylint: disable=no-self-use
        """
            Initializes the serial port connectivity for this device.
        """
        self._serial = self.landscape.lookup_serial_agent(serial_mapping)
        return

    def _resolve_ipaddress(self):
        ipaddr = None
        if self._device_type == "network/upnp" and self.upnp is not None:
            ipaddr = self.upnp.IPAddress
        elif self._device_type == "network/ssh" and self.ssh is not None:
            ipaddr = self.ssh.ipaddr
        return ipaddr

    def _repr_html_(self):
        html_repr_lines = [
            "<h1>LandscapeDevice</h1>",
            "<h2>     type: {}</h2>".format(self._device_type),
            "<h2>    keyid: {}</h2>".format(self._keyid),
            "<h2>       ip: {}</h2>".format(self.ipaddr)
        ]

        html_repr = os.linesep.join(html_repr_lines)

        return html_repr

    def __repr__(self):

        thisType = type(self)

        ipaddr = self.ipaddr
        devstr = "<{} type={} keyid={} ip={} >".format(thisType.__name__, self._device_type, self._keyid, ipaddr)

        return devstr

    def __str__(self):
        devstr = repr(self)
        return devstr