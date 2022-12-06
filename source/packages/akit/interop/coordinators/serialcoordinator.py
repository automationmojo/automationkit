"""
.. module:: serialcoordinator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the SerialCoordinator which is used for managing serial activity services.

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

from akit.exceptions import AKitConfigurationError
from akit.interop.coordinators.coordinatorbase import CoordinatorBase

from akit.interop.agents.serialagents import TcpSerialAgent

if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

class SerialCoordinator(CoordinatorBase):

    def __init__(self, lscape: "Landscape", *args, **kwargs):
        super(SerialCoordinator, self).__init__(lscape, *args, **kwargs)
        return

    def _initialize(self, *_args, **_kwargs):
        """
            Called by the CoordinatorBase constructor to perform the one time initialization
            of the coordinator Singleton of a given type.
        """
        self._serial_config = {}
        for scfg in self._coord_config:
            cfgname = scfg["name"]
            self._serial_config[cfgname] = scfg

        self._serial_agent = {}
        return

    def lookup_agent(self, serial_mapping: dict) -> TcpSerialAgent:
        """
            Looks up a serial agent by serial mapping.
        """
        serial_agent = None

        interface_name = serial_mapping["name"]
        attachment_point = serial_mapping["port"]

        lscape = self.landscape

        if interface_name in self._serial_config:
            serial_config = self._serial_config[interface_name]
            serialType = serial_config["serialType"]
            if serialType == "network/tcp":
                host = serial_config["host"]
                ports_table = serial_config["ports"]
                port = ports_table[attachment_point]

                serial_agent = TcpSerialAgent(host, port)

                self._serial_agent[serial_mapping] = serial_agent
            else:
                errmsg = "Invalid serialType=%s for serial interface %r." % (serialType, interface_name)
                raise AKitConfigurationError(errmsg) from None
        else:
            errmsg = "Failure to lookup serial interface %r." % interface_name
            raise AKitConfigurationError(errmsg) from None

        return serial_agent
