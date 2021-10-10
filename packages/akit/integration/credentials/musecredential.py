
from typing import Optional

import os

from akit.exceptions import AKitConfigurationError

from akit.integration.credentials.basecredential import BaseCredential

class MuseCredential(BaseCredential):
    """
        The :class:`MuseCredential` is a container object for Muse credentials passed in the landscape
        configuration file.

        .. code:: yaml
            "identifier": "player-muse"
            "category": "muse"
            "username": "myron.sonos@gmail.com"
            "password": "...."
            "apikey": "f72eee9e-0b9f-4444-9c13-4efcecece77e"
            "secret": "bfabfaf8-3fb1-7777-9789-fdcdcdcdcd9d"
    """

    category = "muse"

    def __init__(self, identifier: str = "", category: str = "", role: Optional[str] = "priv", username: Optional[str] = None,
                 password: Optional[str] = None, apikey: Optional[str] = None, secret: Optional[str] = None):
        """
            :param identifier: The identifier that is used to reference this credential.  (required)
            :param category: The category of credential.
            :param role: An optional parameter that identifies the role that the credential is assigned to.
            :param username: The username associated with this credential.
            :param password: The password associated with this credential.  A password is not required if a
                             keyfile parameter is provided or if 'allow_agent' is passed as 'True'.
            :param apikey: The apikey issued by Sonos to be used for authentication for a given registered application.
            :param secret: The shared secret issued by Sonos to be used for authentication for a given registered application.
        """
        BaseCredential.__init__(self, identifier=identifier, category=category)
        if category != "muse":
            raise ValueError("The MuseCredential should only be given credentials of category 'muse'.")
        if len(username) == 0:
            raise ValueError("The MuseCredential constructor requires a 'username' parameter be provided.")

        self._identifier = identifier
        self._category = category
        self._username = username
        self._password = password
        self._apikey = apikey
        self._secret = secret
        return

    @property
    def apikey(self):
        return self._apikey

    @property
    def password(self):
        return self._password

    @property
    def secret(self):
        return self._secret

    @property
    def username(self):
        return self._username

    @classmethod
    def validate(cls, cred_info):

        errmsg_lines = []

        if "identifier" not in cred_info:
            errmsg_lines.append("    * missing 'identifier' parameter")

        if "username" not in cred_info:
            errmsg_lines.append("    * missing 'username' parameter")

        if "password" not in cred_info:
            errmsg_lines.append("    * missing 'password' parameter")

        if "apikey" not in cred_info:
            errmsg_lines.append("    * missing 'apikey' parameter")

        if "secret" not in cred_info:
            errmsg_lines.append("    * missing 'secret' parameter")

        if len(errmsg_lines) > 0:
            identifier = "????"
            if "identifier" in cred_info:
                identifier = cred_info["identifier"]

            errmsg = "Errors found while validating the '{}' Muse credential:".format(identifier)
            errmsg_lines.insert(0, errmsg)
            errmsg = os.linesep.join(errmsg_lines)

            raise AKitConfigurationError(errmsg) from None

        return