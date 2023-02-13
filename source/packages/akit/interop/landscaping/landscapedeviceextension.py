"""
.. module:: landscapedevice
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`LandscapeDeviceExtension` class.

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

from typing import TYPE_CHECKING

import weakref

from akit.xlogging.foundations import getAutomatonKitLogger

if TYPE_CHECKING:
    from akit.interop.landscaping.landscapedevice import LandscapeDevice

class LandscapeDeviceExtension:
    """
        The :class:`LandscapeDeviceExtension` object is the base class object that allows for the
        extension of functionality for a :class:`LandscapeDevice`.  The :class:`LandscapeDeviceExtension`
        is used by the UPnP, SSH and Muse coordinators to extend landscape devices with metadata and
        device connectivity for the UPnp, SSH and Muse protocols.
    """


    def __init__(self):
        """
            Constructor use to create an instance of and to initialize a :class:`LandscapeDeviceExtension`.
        """
        self._coord_ref = None
        self._basedevice_ref = None
        self._configinfo = None
        self._extid = None
        self._location = None

        self._logger = getAutomatonKitLogger()
        return

    @property
    def coordinator(self):
        """
            Returns a reference to the coordinator that created the :class:`LandscapeDeviceExtension`.
        """
        coord = None
        if self._coord_ref is not None:
            coord = self._coord_ref()
        return coord

    @property
    def configuration(self):
        """
            The protocol specific configuration infor for the device.
        """
        return self._configinfo

    @property
    def basedevice(self) -> "LandscapeDevice":
        """
            Returns a reference to the base :class:`LandscapeDevice` that this extension was attached to.
        """
        dev = None
        if self._basedevice_ref is not None:
            dev = self._basedevice_ref()
        return dev

    @property
    def extid(self):
        """
            A unique device identifier created by the coordinator for this device extension.  The identier is
            typically something associated with the protocol.
        """
        return self._extid

    @property
    def location(self):
        """
            A network location the device extension is referenced to.
        """
        return self._location

    def initialize(self, coord_ref: weakref.ReferenceType, basedevice_ref: weakref.ReferenceType, extid: str, location: str, configinfo: dict):
        """
            Initializes the landscape device extension.
        """
        self._coord_ref = coord_ref
        self._basedevice_ref = basedevice_ref
        self._extid = extid
        self._location = location
        self._configinfo = configinfo
        return

    def update_base_device_ref(self, basedevice_ref: weakref.ref):
        """
            Used by derived Landscape classes to update the reference to the base device if the base landscape
            device is swapped out to provide enhanced device functionality.
        """
        self._basedevice_ref = basedevice_ref
        return
