"""
.. module:: powercoordinator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the PowerCoordinator which is used for managing power activity services.

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


from typing import Union, TYPE_CHECKING

from akit.exceptions import AKitConfigurationError
from akit.interop.coordinators.coordinatorbase import CoordinatorBase

from akit.interop.agents.poweragents import DliPowerAgent

import dlipower

if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

class PowerCoordinator(CoordinatorBase):

    def __init__(self, lscape: "Landscape", *args, **kwargs):
        super(PowerCoordinator, self).__init__(lscape, *args, **kwargs)
        return

    def _initialize(self, *_args, **_kwargs):
        """
            Called by the CoordinatorBase constructor to perform the one time initialization of the coordinator Singleton
            of a given type.
        """
        self._power_config = {}
        for pcfg in self._coord_config:
            cfgname = pcfg["name"]
            self._power_config[cfgname] = pcfg

        self._power_interfaces = {}
        return

    def lookup_agent(self, power_mapping: dict) -> Union[DliPowerAgent, None]:
        """
            Looks up a power agent by power mapping.
        """
        power_agent = None

        pname = power_mapping["name"]
        pswitch = power_mapping["switch"]

        power_iface = self._lookup_power_interface(pname)
        if power_iface is not None:
            power_agent = DliPowerAgent(power_iface, pswitch)
        else:
            errmsg = "Failure to find power interface %r." % pname
            raise AKitConfigurationError(errmsg) from None

        return power_agent

    def _lookup_power_interface(self, interface_name: str) -> Union[dict, None]:
        """
            Looks up a power interface by power interface name.
        """
        power_iface = None

        if interface_name in self._power_interfaces:
            power_iface = self._power_interfaces[interface_name]
        else:
            lscape = self.landscape
            interface_config = self._power_config[interface_name]
            
            powerType = interface_config["powerType"]

            if powerType == "DliPowerSwitch":
                model = interface_config["model"]
                host = interface_config["host"]

                credential_name = interface_config["credential"]
                credobj = lscape.lookup_credential(credential_name)

                power_iface = dlipower.PowerSwitch(userid=credobj.username, password=credobj.password, hostname=host)

                self._power_interfaces[interface_name] = power_iface
            else:
                errmsg = "Un-Support power interface type={}.".format(powerType)
                raise AKitConfigurationError(errmsg) from None

        return power_iface