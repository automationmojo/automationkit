
from typing import Optional

import os

from akit.exceptions import AKitConfigurationError
from akit.interop.credentials.basecredential import BaseCredential

class SshCredential(BaseCredential):
    """
        The :class:`SshCredential` is a container object for SSH credentials passed in the landscape
        configuration file.

        .. code:: yaml
            "identifier": "straw-node"
            "scheme": "ssh"
            "username": "ubuntu"
            "password": "@@&_@@&_LetMeComeIn"
            "keyfile": "~/.ssh/id_blah_rsa"
            "keypasswd": "@@&_@@&_LetMeComeIn"
            "allow_agent": False
    """

    def __init__(self, identifier: str = "", category: str = "", role: Optional[str] = "priv", username: str = "",
                 password: Optional[str] = None, keyfile: Optional[str] = None, keypasswd: Optional[str] = None,
                 allow_agent: bool = False, primitive: bool=False):
        """
            :param identifier: The identifier that is used to reference this credential.  (required)
            :param category: The category of credential.
            :param role: An optional parameter that identifies the role that the credential is assigned to.
            :param username: The username associated with this credential.
            :param password: The password associated with this credential.  A password is not required if a
                             keyfile parameter is provided or if 'allow_agent' is passed as 'True'.
            :param keyfile: The private key file to use for authentication with this credential.  A keyfile
                            is not required if a password was passed or if 'allow_agent' is passed as 'True'.
            :param keypasswd: The password to decrypt the keyfile if required by the keyfile.
            :param allow_agent: Indicates if the SSH Agent can be used to authenticate connections.
            :param primitive: When True, simulate file transfers and directory services with ssh commands.
        """
        BaseCredential.__init__(self, identifier=identifier, category=category, role=role)

        if category != "ssh":
            raise ValueError("The SshCredential should only be given credentials of category 'ssh'.")
        if len(username) == 0:
            raise ValueError("The SshCredential constructor requires a 'username' parameter be provided.")
        if password is None and keyfile is None and not allow_agent:
            raise ValueError("The SshCredential constructor requires one of: 'password is not None', 'keyfile is not None', 'allow_agent == True'.")

        self._identifier = identifier
        self._category = category
        self._username = username
        self._password = password
        self._keyfile = keyfile
        self._keypasswd = keypasswd
        self._allow_agent = allow_agent
        self._primitive = primitive
        return

    @property
    def allow_agent(self):
        return self._allow_agent

    @property
    def identifier(self):
        return self._identifier

    @property
    def keyfile(self):
        return self._keyfile

    @property
    def keypasswd(self):
        return self._keypasswd

    @property
    def password(self):
        return self._password

    @property
    def primitive(self):
        return self._primitive

    @property
    def username(self):
        return self._username

    @classmethod
    def validate(cls, cred_info):

        errmsg_lines = []

        allow_agent = False
        if "allow_agent" in cred_info:
            allow_agent = cred_info["allow_agent"]

        if "identifier" not in cred_info:
            errmsg_lines.append("    * missing 'identifier' parameter")

        if "username" not in cred_info:
            errmsg_lines.append("    * missing 'username' parameter")

        if "password" not in cred_info and "keyfile" not in cred_info and not allow_agent:
                errmsg_lines.append("    * missing 'password' or 'keyfile' when allow_agent is 'False'")

        if "keyfile" in cred_info:
            keyfile = os.path.abspath(os.path.expandvars(os.path.expanduser(cred_info["keyfile"])))
            if not os.path.exists(keyfile):
                errmsg_lines.append("    * specified 'keyfile={}' not found.".format(keyfile))

        if len(errmsg_lines) > 0:
            identifier = "????"
            if "identifier" in cred_info:
                identifier = cred_info["identifier"]

            errmsg = "Errors found while validating the '{}' SSH credential:".format(identifier)
            errmsg_lines.insert(0, errmsg)
            errmsg = os.linesep.join(errmsg_lines)

            raise AKitConfigurationError(errmsg) from None

        return
