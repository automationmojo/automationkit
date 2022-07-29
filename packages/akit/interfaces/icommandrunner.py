
from typing import Optional, Sequence, Tuple, Union

from akit.aspects import AspectsCmd
from akit.exceptions import AKitNotImplementedError

import paramiko

class ICommandRunner:
    """
        The ICommandRunner interface is used to provide a common interface for both SSH and Serial command runners.
    """

    def open_session(self, primitive: bool = False, ssh_session: Optional["ICommandRunner"] = None,
                     aspects: Optional[AspectsCmd] = None) -> "ICommandRunner": # pylint: disable=arguments-differ
        """
            Provies a mechanism to create a :class:`SshSession` object with derived settings.  This method allows various parameters for the session
            to be overridden.  This allows for the performing of a series of SSH operations under a particular set of shared settings and or credentials.

            :param primitive: Use primitive mode for FTP operations for the session.
            :param pty_params: The default pty parameters to use to request a PTY when running commands through the session.
            :param interactive: Creates an interactive session which holds open an interactive shell so commands can interact in the shell.
            :param ssh_session: An optional SshSession instance to use.  This allows re-use of sessions.
            :param aspects: The default run aspects to use for the operations performed by the session.
        """
        raise AKitNotImplementedError("The 'ICommandRunner' interface requires the 'open_session' method to be implemented.") from None

    def run_cmd(self, command: str, exp_status: Union[int, Sequence]=0, aspects: Optional[AspectsCmd] = None) -> Tuple[int, str, str]: # pylint: disable=arguments-differ
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
            :param exp_status: An integer or sequence of integers that specify the set of expected status codes from the command.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """
        raise AKitNotImplementedError("The 'ICommandRunner' interface requires the 'run_cmd' method to be implemented.") from None