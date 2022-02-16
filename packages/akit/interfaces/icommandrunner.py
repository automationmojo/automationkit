
from typing import Optional, Sequence, Tuple, Union

from akit.aspects import AspectsCmd
from akit.exceptions import AKitNotImplementedError

import paramiko

class ICommandRunner:

    def run_cmd(self, command: str, aspects: Optional[AspectsCmd] = None) -> Tuple[int, str, str]: # pylint: disable=arguments-differ
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """
        raise AKitNotImplementedError("The 'ICommandRunner' interface requires the 'run_cmd' method to be implemented.") from None