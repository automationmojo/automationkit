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


from typing import TYPE_CHECKING

from akit.exceptions import AKitConfigurationError
from akit.interop.coordinators.coordinatorbase import CoordinatorBase
from akit.interop.credentials.credentialmanager import CredentialManager

from akit.interop.agents.wirelessapagent import WirelessApAgent

if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

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

        self._wireless_agents = {}
        return
    
    def lookup_agent(self, apname: str) -> WirelessApAgent:
        """
            Looks up a serial agent by serial mapping.
        """
        wireless_agent = None

        lscape = self.landscape

        if apname in self.self._wireless_ap_config:
            wireless_mapping = self._wireless_ap_config[apname]

            if apname not in self._wireless_agents:
                host = wireless_mapping["host"]
                credential_name = wireless_mapping["credential"]

                credential = lscape.lookup_credential(credential_name)

                if credential is not None:
                    wireless_agent = WirelessApAgent(host, credential)

                    self._wireless_agents[apname] = wireless_agent
                else:
                    errmsg = "Failure to find credential '{}' specified for wireless apname={}".format(
                        credential_name, apname
                    )
                    raise AKitConfigurationError(errmsg)
            else:
                wireless_agent = self._wireless_agents[apname]
        else:
            errmsg = "Failure to lookup wireless configuration for apname={}.".format(apname)
            raise AKitConfigurationError(errmsg) from None

        return wireless_agent
