
from typing import Optional, Sequence, Tuple, Union

from akit.aspects import Aspects
from akit.exceptions import AKitNotImplementedError

import paramiko

class ICommandRunner:
    def run_cmd(self, command: str, exp_status: Union[int, Sequence]=0, user: str = None, pty_params: dict = None, aspects: Optional[Aspects] = None, ssh_client: Optional[paramiko.SSHClient]=None) -> Tuple[int, str, str]: # pylint: disable=arguments-differ
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
            :param exp_status: An integer or sequence of integers that specify the set of expected status codes from the command.
            :param user: The registered name of the user role to use to lookup the credentials for running the command.
            :param pty_params: The pty parameters to use to request a PTY when running the command.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """
        raise AKitNotImplementedError("The 'ICommandRunner' interface requires the 'run_cmd' method to be implemented.") from None