"""
.. module:: coordinatorbase
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the CoordinatorBase which is the base object for coordinators to derive from and establishes
               patterns for coordinators which help to make them threadsafe.

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

from typing import List, Optional, TYPE_CHECKING

import threading
import weakref

from akit.exceptions import AKitNotOverloadedError
from akit.interop.landscaping.landscapedevice import LandscapeDevice
from akit.interop.landscaping.landscapedeviceextension import LandscapeDeviceExtension

from akit.xlogging.foundations import getAutomatonKitLogger

EMPTY_LIST = []

if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

class CoordinatorBase:
    """
        The CoordinatorBase utilizes the expected device declarations of type such as 'network/upnp' to establish and maintain
        connectivity and interoperability with a class of devices.  A derived coordinator will scan the medium such as a network
        for the devices declared in the landscape description.  The coordinator will also create the threads necessary to maintain
        communicates with the external devices over the medium.
    """

    instance = None
    initialized = False

    def __new__(cls, *_args, **_kwargs):
        """
            Constructs new instances of the :class:`UpnpCoordinator` object. The
            :class:`UpnpCoordinator` object is a singleton so following instantiations
            of the object will reference the existing singleton
        """

        if cls.instance is None:
            cls.instance = super(CoordinatorBase, cls).__new__(cls)
        return cls.instance

    def __init__(self, lscape: "Landscape", *args, coord_config=None, **kwargs):
        """
            Constructs an instance of a derived :class:`CoordinatorBase` object.

            :param lscape: The :class:`Landscape` singleton instance.
            :param *args: A pass through for other positional args.
            :param **kwargs: A pass through for the other keyword args.
        """
        this_type = type(self)
        if not this_type.initialized:
            this_type.initialized = True

            self._logger = getAutomatonKitLogger()

            # If the landscape is in interactive mode, then all the coordinators should
            # default to using interactive mode
            self._interactive_mode = lscape.interactive_mode

            self._lscape_ref = weakref.ref(lscape)

            self._coord_lock = threading.RLock()

            self._cl_children = {}

            self._found_devices = []
            self._available_devices = []
            self._unavailable_devices = []

            self._coord_config = coord_config

            self._initialize(*args, **kwargs)
        return

    def _initialize(self, *_args, **_kwargs):
        """
            Called by the CoordinatorBase constructor to perform the one time initialization of the coordinator Singleton
            of a given type.
        """
        # pylint: disable=no-self-use
        raise AKitNotOverloadedError("_initialize: must be overloaded by derived coordinator classes") from None

    @property
    def available_devices(self):
        """
            The devices that the coordinator found to be available during startup.
        """
        return self._available_devices

    @property
    def children(self) -> List[LandscapeDevice]:
        """
            Returns a list of the devices created by the coordinator and registered by the coordinator with the Landscape object.
        """
        chlist = EMPTY_LIST

        self._coord_lock.acquire()
        try:
            chlist = [c.basedevice for c in self._cl_children.values()]
        finally:
            self._coord_lock.release()

        return chlist

    @property
    def children_as_extension(self) -> List[LandscapeDeviceExtension]:
        """
            Returns a list of the device protocol extensions created by this coordinator that have been attached to a landscape device.
        """
        chlist = EMPTY_LIST

        self._coord_lock.acquire()
        try:
            chlist = [c for c in self._cl_children.values()]
        finally:
            self._coord_lock.release()

        return chlist

    @property
    def coord_config(self):
        """
            The dedicated coordinator configuration for coordinators that have a dedicated
            configuration section in the landscape file.  Example: power, serial, wireless
        """

    @property
    def landscape(self):
        """
            Returns a hard reference to the Landscape singleton instance.
        """
        lscape = self._lscape_ref()
        return lscape

    @property
    def found_devices(self):
        """
            The devices that were dynamically discovery by the coordinators discovery protocol.
        """
        return self._found_devices

    @property
    def unavailable_devices(self):
        """
            The devices that the coordinator found to be unavailable during startup.
        """
        return self._unavailable_devices

    def establish_presence(self):
        """
            Implemented by derived coordinator classes to establish a specific presence in the
            landscape.
        """
        return

    def lookup_device_by_key(self, key) -> LandscapeDevice:
        """
            Looks up a device from the list of children by key in a thread safe way.
        """

        found = None

        self._coord_lock.acquire()
        try:
            if key in self._cl_children:
                found = self._cl_children[key].basedevice
        finally:
            self._coord_lock.release()

        return found

    def verify_connectivity(self, cmd: str = "echo 'It Works'", user: Optional[str] = None, raiseerror: bool = True):
        """
            Loops through the nodes in the coordinators pool in order to verify connectivity with the remote node.

            :param cmd: A command to run on the remote machine in order to verify that connectivity can be establish.
            :param user: The name of the user credentials to use for connectivity.
                         If the 'user' parameter is not provided, then the credentials
                         of the default or priviledged user will be used.
            :param raiseerror: A boolean value indicating if this API should raise an Exception on failure.

            :returns: A list of errors encountered when verifying connectivity with the devices managed or watched by the coordinator.
        """
        # pylint: disable=no-self-use
        raise AKitNotOverloadedError("verify_connectivity: must be overloaded by derived coordinator classes") from None
