"""
.. module:: wirelessapcoordinator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the WirelessAPCoordinator which is used for managing wireless access points.

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
from akit.integration.coordinators.coordinatorbase import CoordinatorBase

from akit.integration.agents.poweragents import DliPowerAgent

import dlipower

if TYPE_CHECKING:
    from akit.integration.landscaping.landscape import Landscape

class WirelessAPCoordinator(CoordinatorBase):

    def __init__(self, lscape: "Landscape", *args, **kwargs):
        super(WirelessAPCoordinator, self).__init__(lscape, *args, **kwargs)
        return

    def _initialize(self, *_args, **_kwargs):
        """
            Called by the CoordinatorBase constructor to perform the one time initialization of the coordinator Singleton
            of a given type.
        """
        self._wireless_ap_config = {}
        for apcfg in self._coord_config:
            cfgname = apcfg["name"]
            self._wireless_ap_config[cfgname] = apcfg

        return
