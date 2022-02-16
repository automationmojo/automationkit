
class BaseCredential:
    """
        The :class:`BaseCredential` is the base container object for credentials passed in the landscape
        configuration file.

        .. code:: yaml
            "identifier": "player-ssh"
            "category": "(category)"
    """
    def __init__(self, identifier: str = "", category: str = "", role: str = "priv"):
        """
            :param identifier: The identifier that is used to reference this credential.  (required)
            :param category: The category of credential.
        """
        if len(identifier) == 0:
            raise ValueError("The MuseCredential constructor requires a 'identifier' parameter be provided.")
        if len(category) == 0:
            raise ValueError("The MuseCredential constructor requires a 'category' parameter be provided.")

        self._identifier = identifier
        self._category = category
        self._role = role
        return

    @property
    def category(self):
        return self._category

    @property
    def identifier(self):
        return self._identifier

    @property
    def role(self):
        return self._role
