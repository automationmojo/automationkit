__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Dict, List, Optional

import os

from akit.exceptions import AKitConfigurationError
from akit.interop.credentials.basecredential import BaseCredential

class WifiChoiceCredential(BaseCredential):
    """
        The :class:`WifiChoiceCredential` is a container object for a list of wifi credential choices.

        .. code:: yaml
            identifier: "my-wifi-networks"
            category: "wifi-choice"
            networks:
                - ssid: SOMENETWORK
                  password: BlahBlah!!

    """

    def __init__(self, *, identifier: str, category: str, networks: List[Dict[str, str]], role: Optional[str] = "priv"):
        """
            :param identifier: The identifier that is used to reference this credential.  (required)
            :param category: The category of credential.
            :param networks: List of network credentials.
        """
        super().__init__(identifier=identifier, category=category, role=role)

        if category != "wifi-choice":
            raise ValueError("The WifiChoiceCredential should only be given credentials of category 'basic'.")
        if len(networks) == 0:
            raise ValueError("The WifiChoiceCredential constructor should have at least one network.")

        self._networks = networks
        return

    @property
    def networks(self):
        return self._networks

    @classmethod
    def validate(cls, cred_info: dict):

        errmsg_lines = []

        if "networks" not in cred_info:
            errmsg_lines.append("    * missing 'networks' field on wifi-choice credential.")

        networks = cred_info["networks"]
        if len(networks) == 0:
            errmsg_lines.append("    * empty 'networks' field on wifi-choice credential.")

        for nidx, network_info in enumerate(networks):
            if "ssid" not in network_info:
                errmsg = "    * 'networks' item {} is missing the 'ssid' field on wifi-choice credential.".format(nidx)
                errmsg_lines.append(errmsg)
            
            if "password" not in network_info:
                errmsg = "    * 'networks' item {} is missing the 'password' field on wifi-choice credential.".format(nidx)
                errmsg_lines.append(errmsg)

        if len(errmsg_lines) > 0:
            identifier = "????"
            if "identifier" in cred_info:
                identifier = cred_info["identifier"]
            
            errmsg = "Errors found while validating the '{}' wifi-choice credential:".format(identifier)
            errmsg_lines.insert(0, errmsg)
            errmsg = os.linesep.join(errmsg_lines)

            raise AKitConfigurationError(errmsg) from None

        return
