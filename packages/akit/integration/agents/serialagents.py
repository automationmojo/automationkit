
from typing import Optional, Sequence, Tuple, Union

import telnetlib

from akit.aspects import Aspects
from akit.compat import bytes_cast, str_cast

class TcpSerialAgent:
    """
        The :class:`TcpSerialAgent` provides access to serial port hosted on a TCP/IP network.  The
        remote endpoint might be a host and port for a serial port hosted on a serial concentrator.
        It could be the host and port of a serial port hosted on a linux box via USB and ser2net.

        ..note:
            An example ser2net configuration might look like the configuration below.

            BANNER:banner:\r\nser2net port \p device \d [\s] (Debian GNU/Linux)\r\n\r\n

            3333:telnet:0:/dev/ttyUSB0:115200 8DATABITS NONE 1STOPBIT banner

            
    """

    SERIAL_PROMPT=b"@@@&@@@&"
    NORMAL_PROMPT=b"#"

    def __init__(self, host, port):
        self._host = host
        self._port = port
        return

    def run_cmd(self, command: str, exp_status: Union[int, Sequence]=0, aspects: Optional[Aspects] = None) -> Tuple[int, str, str]:
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
            :param exp_status: An integer or sequence of integers that specify the set of expected status codes from the command.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """
        status = None
        stdout = None
        stderr = None

        command = bytes_cast("%s 2> $TNSTDERR\n" % command)

        tnconn = self._create_connection()
        try:
            tnconn.write(b"export TNSTDERR=/tmp/tnstderr\n")
            cmdout = tnconn.read_until(self.SERIAL_PROMPT, timeout=5)

            tnconn.write(command)
            stdout_raw = tnconn.read_until(self.SERIAL_PROMPT, timeout=5)

            tnconn.write(b"echo $?\n")
            status_raw = tnconn.read_until(self.SERIAL_PROMPT, timeout=5)
            status_bytes = status_raw.splitlines(False)[1]

            tnconn.write(b"cat $TNSTDERR\n")
            stderr_raw = tnconn.read_until(self.SERIAL_PROMPT)

            stdout = "\n".join(str_cast(stdout_raw).splitlines(False)[1:-1])
            stderr = "\n".join(str_cast(stderr_raw).splitlines(False)[1:-1])
            status = int(status_bytes)
        finally:
            if tnconn is not None:
                self._restore_prompt(tnconn)
            tnconn.close()

        return status, stdout, stderr

    def _create_connection(self):

        tnconn = telnetlib.Telnet(host=self._host, port=self._port)

        cmd_out = tnconn.read_until(self.NORMAL_PROMPT, 1)

        tnconn.write(b"\n")
        cmd_out = tnconn.read_until(self.NORMAL_PROMPT)

        tnconn.write(b"echo $PS1\n")
        ps1_out = tnconn.read_until(self.NORMAL_PROMPT)
        self.NORMAL_PROMPT = ps1_out.splitlines(False)[1]

        tnconn.write(b"export PS1=\"%s\"\n" % self.SERIAL_PROMPT)

        cmd_out = tnconn.read_until(self.SERIAL_PROMPT)
        cmd_out = tnconn.read_until(self.SERIAL_PROMPT)
        return tnconn

    def _restore_prompt(self, tnconn):
        tnconn.write(b"echo $PS1\n")
        ps1_out = tnconn.read_until(self.NORMAL_PROMPT)
        return


if __name__ == "__main__":
    sagent = TcpSerialAgent("192.168.1.40", 3333)
    
    status, stdout, stderr = sagent.run_cmd("ls /jffs")

    print("STATUS:\n%s\n" % status)
    print("STDOUT:\n%s\n" % stdout)
    print("STDERR:\n%s\n" % stderr)