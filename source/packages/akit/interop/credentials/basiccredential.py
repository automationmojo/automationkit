
from typing import Optional

import os

from akit.exceptions import AKitConfigurationError
from akit.interop.credentials.basecredential import BaseCredential

class BasicCredential(BaseCredential):
    """
        The :class:`BasicCredential` is a container object for a basic username and password based credential.

        .. code:: yaml
            "identifier": "basic-login"
            "category": "basic"
            "username": "ubuntu"
            "password": "@@&_@@&_LetMeComeIn"

    """

    def __init__(self, identifier: str = "", category: str = "", username: str = "", password: str = ""):
        """
            :param identifier: The identifier that is used to reference this credential.  (required)
            :param category: The category of credential.
            :param username: The username associated with this credential.
            :param password: The password associated with this credential.  A password is not required if a
                             keyfile parameter is provided or if 'allow_agent' is passed as 'True'.
        """
        BaseCredential.__init__(self, identifier=identifier, category=category)

        if category != "basic":
            raise ValueError("The BasicCredential should only be given credentials of category 'basic'.")
        if len(username) == 0:
            raise ValueError("The BasicCredential constructor requires a 'username' parameter be provided.")
        if len(password) == 0:
            raise ValueError("The BasicCredential constructor requires one of: 'password is not None'.")

        self._identifier = identifier
        self._category = category
        self._username = username
        self._password = password
        return

    @property
    def identifier(self):
        return self._identifier

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username

    @classmethod
    def validate(cls, cred_info):

        errmsg_lines = []

        if "password" not in cred_info:
                errmsg_lines.append("    * missing 'password' in basic credential.")

        if "username" not in cred_info:
                errmsg_lines.append("    * missing 'username' in basic credential.")

        if len(errmsg_lines) > 0:
            identifier = "????"
            if "identifier" in cred_info:
                identifier = cred_info["identifier"]

            errmsg = "Errors found while validating the '{}' basic credential:".format(identifier)
            errmsg_lines.insert(0, errmsg)
            errmsg = os.linesep.join(errmsg_lines)

            raise AKitConfigurationError(errmsg) from None

        return
