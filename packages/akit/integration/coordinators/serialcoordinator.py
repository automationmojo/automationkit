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


from typing import Union

import weakref

from akit.exceptions import AKitConfigurationError
from akit.integration.agents.serialagents import TcpSerialAgent

class SerialCoordinator:

    def __init__(self, lscape, serial_config):
        self._lscape_ref = weakref.ref(lscape)
        self._serial_config = {}
        for scfg in serial_config:
            cfgname = scfg["name"]
            self._serial_config[cfgname] = scfg

        self._serial_agent = {}
        return

    def lookup_agent(self, serial_mapping: str):
        """
            Looks up a serial agent by serial mapping.
        """
        serial_agent = None

        interface_name = serial_mapping["name"]
        attachment_point = serial_mapping["port"]

        lscape = self._lscape_ref()

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
        else:
            errmsg = "Failure to lookup serial interface %r." % interface_name
            raise AKitConfigurationError(errmsg) from None

        return serial_agent
