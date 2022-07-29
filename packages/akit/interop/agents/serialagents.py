
from typing import Optional, Tuple
from types import TracebackType

import telnetlib

from akit.aspects import AspectsCmd
from akit.compat import bytes_cast, str_cast

from akit.interfaces.icommandrunner import ICommandRunner

from akit.aspects import ActionPattern, AspectsCmd, LoggingPattern, DEFAULT_CMD_ASPECTS

class TcpSerialBase(ICommandRunner):

    def __init__(self, host: str, port: int=22, aspects: AspectsCmd=DEFAULT_CMD_ASPECTS):
        self._host = host
        self._port = port
        self._aspects = aspects
        return
    
    def _create_connection(self) -> telnetlib.Telnet:

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

    def _restore_prompt(self, tnconn: telnetlib.Telnet):
        tnconn.write(b"echo $PS1\n")
        ps1_out = tnconn.read_until(self.NORMAL_PROMPT)
        return

class TcpSerialSession(TcpSerialBase):

    def __init__(self, host: str, port:int=22, session_basis: Optional["TcpSerialSession"]=None, aspects: AspectsCmd=DEFAULT_CMD_ASPECTS):
        super().__init__(host, port=port, aspects=aspects)
        self._session_basis = session_basis
        self._telnet_conn = None
        return

    def __enter__(self):
        """
            Method that implements the __enter__ symantics used for 'with' statements.
        """
        self._telnet_conn = self._create_connection()

        return self

    def __exit__(self, ex_type: type, ex_val: Exception, ex_tb: TracebackType) -> bool:
        """
            Method that implements the __exit__ symantics used for 'with' statements.

            :returns: Returns false indicating that exceptions are not handled.
        """
        self.close()
        handled = False
        return handled

    def close(self):
        """
            Closes the SSH session and the assocatied SSH connection.
        """
        # Only close the client if this session owns the client
        if self._session_basis is None:
            self._telnet_conn.close()
        return

    def open_session(self, session_basis: Optional["ICommandRunner"] = None,
                     aspects: Optional[AspectsCmd] = None) -> "ICommandRunner": # pylint: disable=arguments-differ
        """
            Provies a mechanism to create a :class:`TcpSerialSession` object with derived settings.  This method allows various
            parameters for the session to be overridden.  This allows for the performing of a series of TCP Serial operations under
            a particular set of shared settings or command behaviors.

            :param session_basis: An optional existing TcpSerialSession instance to use as a basis for the new session.
            :param aspects: The default run aspects to use for the operations performed by the session.
        """

        session_aspects = None
        if aspects is None:
            session_aspects = self._aspects

        session = None
        if session_basis is not None:
            session = TcpSerialSession(session_basis._host, port=session_basis._port, session_basis=session_basis, aspects=session_aspects)
        else:
            session = TcpSerialSession(self._host, port=self._port, aspects=session_aspects)

        return session

    
    def _create_connection(self) -> telnetlib.Telnet:
        """
            Create an Telnet connection if one is not already open and available.

            :returns: An :class:`telnetlib.Telnet` object connected to the remote Tcp Serial concentrator.
        """
        tnconn = None

        if self._session_basis is not None:
            tnconn = self._session_basis._telnet_conn
        else:
            tnconn = TcpSerialBase._create_connection(self)

        return tnconn

class TcpSerialAgent(TcpSerialBase):
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

    def __init__(self, host, port:int=22, aspects: AspectsCmd=DEFAULT_CMD_ASPECTS):
        super().__init__(host, port=port, aspects=aspects)
        return

    def open_session(self, session_basis: Optional["ICommandRunner"] = None,
                     aspects: Optional[AspectsCmd] = None) -> "ICommandRunner": # pylint: disable=arguments-differ
        """
            Provies a mechanism to create a :class:`TcpSerialSession` object with derived settings.  This method allows various
            parameters for the session to be overridden.  This allows for the performing of a series of TCP Serial operations under
            a particular set of shared settings or command behaviors.

            :param session_basis: An optional existing TcpSerialSession instance to use as a basis for the new session.
            :param aspects: The default run aspects to use for the operations performed by the session.
        """

        session_aspects = None
        if aspects is None:
            session_aspects = self._aspects

        session = None
        if session_basis is not None:
            session = TcpSerialSession(session_basis._host, port=session_basis._port, session_basis=session_basis, aspects=session_aspects)
        else:
            session = TcpSerialSession(self._host, port=self._port, aspects=session_aspects)

        return session

    def run_cmd(self, command: str, aspects: Optional[AspectsCmd] = None) -> Tuple[int, str, str]:
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
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

    


if __name__ == "__main__":
    sagent = TcpSerialAgent("192.168.1.40", 3333)
    
    status, stdout, stderr = sagent.run_cmd("ls /jffs")

    print("STATUS:\n%s\n" % status)
    print("STDOUT:\n%s\n" % stdout)
    print("STDERR:\n%s\n" % stderr)