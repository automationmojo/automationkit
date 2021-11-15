
import os

from akit.exceptions import AKitUCIRequestError

from akit.integration.agents.sshagent import SshAgent
from akit.integration.wireless.constants import (
    DeAuthenticationReason, MfpMode, WirelessEncryption)

from akit.aspects import Aspects, DEFAULT_ASPECTS
from akit.integration.credentials.sshcredential import SshCredential

class WirelessApAgent:
    """
        The :class:`WirelessApAgent` provides an implementation of a administrative
        interface for devices that are running the OpenWRT wireless router software.
    """

    def __init__(self, ap_host: str, admin_credential: SshCredential, port: int=22, aspects: Aspects=DEFAULT_ASPECTS):
        self._ap_host = ap_host
        self._admin_credential = admin_credential
        self._port = port
        self._aspects = aspects

        self._ssh_agent = SshAgent(self._ap_host, self._admin_credential, aspects=aspects)
        return

    def uci_delete(self, prop_name: str, aspects: Aspects=None):

        if aspects is None:
            aspects = self._aspects

        command = "uci delete {}".format(prop_name)
        status, stdout, stderr = self._ssh_agent.run_cmd(command, aspects=aspects)
        if status != 0:
            errmsg_lines = [
                "Error deleting router configuration property name={}.",
                "COMMAND: {}".format(command),
                "STDOUT: {}".format(stdout),
                "STDERR: {}".format(stderr)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitUCIRequestError(errmsg)

        return

    def uci_get(self, prop_name: str, aspects: Aspects=None) -> str:

        if aspects is None:
            aspects = self._aspects

        command = "uci get {}".format(prop_name)
        
        status, stdout, stderr = self._ssh_agent.run_cmd(command, aspects=aspects)
        if status != 0:
            errmsg_lines = [
                "Error getting router configuration property name={}.",
                "COMMAND: {}".format(command),
                "STDOUT: {}".format(stdout),
                "STDERR: {}".format(stderr)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitUCIRequestError(errmsg)


        return stdout

    def uci_set(self, prop_name: str, prop_value: str, aspects: Aspects=None):

        if aspects is None:
            aspects = self._aspects

        command = "uci set {} {}".format(prop_name, prop_value)
        status, stdout, stderr = self._ssh_agent.run_cmd(command, aspects=aspects)
        if status != 0:
            errmsg_lines = [
                "Error getting router configuration property name={}.",
                "COMMAND: {}".format(command),
                "STDOUT: {}".format(stdout),
                "STDERR: {}".format(stderr)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitUCIRequestError(errmsg)

        return
