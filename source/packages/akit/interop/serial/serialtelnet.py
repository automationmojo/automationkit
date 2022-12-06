
import enum
import socket
import struct
import telnetlib

COMMAND_NAMES = {
    telnetlib.BRK: "BRK",
    telnetlib.DM: "DM",
    telnetlib.DO: "DO",
    telnetlib.DONT: "DONT",
    telnetlib.GA: "GA",
    telnetlib.IAC: "IAC",
    telnetlib.NOP: "NOP",
    telnetlib.SB: "SB",
    telnetlib.SE: "SE",
    telnetlib.WILL: "WILL",
    telnetlib.WONT: "WONT"
}

OPTION_NAMES = {
    telnetlib.BINARY: "BINARY",
    telnetlib.ECHO: "ECHO",
    telnetlib.RCP: "RCP",
    telnetlib.SGA: "SGA",
    telnetlib.NAMS: "NAMS",
    telnetlib.STATUS: "STATUS",
    telnetlib.TM: "TM",
    telnetlib.RCTE: "RCTE",
    telnetlib.NAOL: "NAOL",
    telnetlib.NAOP: "NAOP",
    telnetlib.NAOCRD: "NAOCRD",
    telnetlib.NAOHTS: "NAOHTS",
    telnetlib.NAOHTD: "NAOHTD",
    telnetlib.NAOFFD: "NAOFFD",
    telnetlib.NAOVTS: "NAOVTS",
    telnetlib.NAOVTD: "NAOVTD",
    telnetlib.NAOLFD: "NAOLFD",
    telnetlib.XASCII: "XASCII",
    telnetlib.LOGOUT: "LOGOUT",
    telnetlib.BM: "BM",
    telnetlib.DET: "DET",
    telnetlib.SUPDUP: "SUPDUP",
    telnetlib.SUPDUPOUTPUT: "SUPDUPOUTPUT",
    telnetlib.SNDLOC: "SNDLOC",
    telnetlib.TTYPE: "TTYPE",
    telnetlib.EOR: "EOR",
    telnetlib.TUID: "TUID",
    telnetlib.OUTMRK: "OUTMRK",
    telnetlib.TTYLOC: "TTYLOC",
    telnetlib.VT3270REGIME: "VT3270REGIME",
    telnetlib.X3PAD: "X3PAD",
    telnetlib.NAWS: "NAWS",
    telnetlib.TSPEED: "TSPEED",
    telnetlib.LFLOW: "LFLOW",
    telnetlib.LINEMODE: "LINEMODE",
    telnetlib.XDISPLOC: "XDISPLOC",
    telnetlib.OLD_ENVIRON: "OLD_ENVIRON",
    telnetlib.AUTHENTICATION: "AUTHENTICATION",
    telnetlib.ENCRYPT: "ENCRYPT",
    telnetlib.NEW_ENVIRON: "NEW_ENVIRON",
    telnetlib.TN3270E: "TN3270E",
    telnetlib.XAUTH: "XAUTH",
    telnetlib.CHARSET: "CHARSET",
    telnetlib.RSP: "RSP",
    telnetlib.COM_PORT_OPTION: "COM_PORT_OPTION",
    telnetlib.SUPPRESS_LOCAL_ECHO: "SUPPRESS_LOCAL_ECHO",
    telnetlib.TLS: "TLS",
    telnetlib.KERMIT: "KERMIT",
    telnetlib.SEND_URL: "SEND_URL",
    telnetlib.FORWARD_X: "FORWARD_X",
    telnetlib.PRAGMA_LOGON: "PRAGMA_LOGON",
    telnetlib.SSPI_LOGON: "SSPI_LOGON",
    telnetlib.PRAGMA_HEARTBEAT: "PRAGMA_HEARTBEAT"
}

class TelnetOptionState(enum.IntEnum):
    UNSET = 0
    REQUESTED = 1
    ACTIVE = 2
    INACTIVE = 3
    REALLY_INACTIVE = 4


class TelnetOption:
    """
        Manages the state of a telnet option for a telnet session.
    """
    def __init__(self, name, option, send_yes, send_no, ack_yes, ack_no, initial_state, activation_callback=None):
        self._name = name
        self._option = option
        self._send_yes = send_yes
        self._send_no = send_no
        self._ack_yes = ack_yes
        self._ack_no = ack_no
        self._state = initial_state
        self._active = False
        self._activation_callback = activation_callback
        return

    def negotiate_option(self, command):
        """
            A DO/DONT/WILL/WONT was received for this option, update state and answer when needed.
        """
        if command == self._ack_yes:
            pass
        elif command == self._ack_no:
            pass
        return


class SerialTelnet(telnetlib.Telnet):

    def __init__(self, host=None, port=0, baudrate=None, echo=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):

        super(SerialTelnet, self).__init__(host=host, port=port, timeout=timeout)

        self._baudrate = 115200
        if baudrate is not None:
            self._baudrate = baudrate

        self._echo = False
        if echo is not None:
            self._echo = echo

        self.set_option_negotiation_callback(self._callback_negotiate_options)
        return

    def open(self, host, port=0, baudrate=None, echo=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Connect to a host.

        The optional second argument is the port number, which
        defaults to the standard telnet port (23).

        Don't try to reopen an already connected instance.
        """

        if baudrate is not None:
            self._baudrate = baudrate

        if echo is not None:
            self._echo = echo

        super(SerialTelnet, self).open(host=host, port=port, timeout=timeout)

        return

    def negotiate_options(self):
        self._send_option(telnetlib.DONT, telnetlib.ECHO)
        return

    def _send_option(self, action, option):
        pkstr = struct.pack(">ccc", telnetlib.IAC, action, option)
        tsocket = self.get_socket()
        self.sock.sendall(pkstr)
        return

    def _callback_negotiate_options(self, tsocket, command, options):

        cmdstr = COMMAND_NAMES[command]
        optstr = OPTION_NAMES[options]

        print("cmd=%s opt=%s" % (cmdstr, optstr))

        if command == telnetlib.DO:
            if options == telnetlib.TTYPE:
                # Promise we will send a terminal type
                self._send_option(telnetlib.WONT, telnetlib.TTYPE)
            elif options == telnetlib.ECHO:
                # Promise we will echo
                self._send_option(telnetlib.DONT, telnetlib.ECHO)
            elif options == telnetlib.NAWS:
                # Promise we will send our window size
                self._send_option(telnetlib.WONT, telnetlib.NAWS)
            elif options == telnetlib.TSPEED:
                # Promise we will send a terminal speed
                self._send_option(telnetlib.WILL, telnetlib.NAWS)
            elif options == telnetlib.XDISPLOC:
                # Tell the server we will not send the x-display terminal
                self._send_option(telnetlib.WONT, telnetlib.XDISPLOC)
        elif command == telnetlib.SB:
            if options == telnetlib.NEW_ENVIRON:
                print("Asked for environment.")
        # cmd=WILL opt=03
        # cmd=WILL opt=01
        # cmd=DONT opt=01
        # cmd=DO   opt=00
        # cmd=WONT opt=01

        return


if __name__ == "__main__":
    stn = SerialTelnet()
    stn.open(host="192.168.1.17", port=3333)
    stn.read_very_eager()

    stn.negotiate_options()

    stn.read_very_eager()

    stn.interact()

    print("blah")

