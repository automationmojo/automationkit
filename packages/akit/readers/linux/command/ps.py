
from typing import List, Union

from akit.xregex.regexreader import RegExReader, RegExPattern

import re

from collections import namedtuple

class ProcessItem:

    def __init__(self, *, pid, tty, time, cmd):
        self.pid = pid
        self.tty = tty
        self.time = time
        self.cmd = cmd
        return

    def __repr__(self):
        rtnstr = '{ "pid": %r, "tty": %r, "time": %r, "cmd": %r}' % (
            self.pid, self.tty, self.time, self.cmd)
        return rtnstr

    def __str__(self):
        return repr(self)

class CmdReaderPs(RegExReader):
    """
        Reader for processing the output of the 'ps' command.
    """

    EXPECTED_LINES = [
        RegExPattern(r"^[\s]*(?P<hpid>[A-Za-z]+)[\s]+(?P<htty>[A-Za-z]+)[\s]+(?P<htime>[A-Za-z]+)[\s]+(?P<hcmd>[A-Za-z]+)", required=True),
        RegExPattern(r"^[\s]*(?P<pid>[\S]+)[\s]+(?P<tty>[\S]+)[\s]+(?P<time>[\S]+)[\s]+(?P<cmd>[\S]+)", exclass="ProcessItem", repeats=True)
    ]

    def __init__(self, content:Union[List, str], strict=False, consume_whitespace_lines=True):
        self._process_listing = []

        super().__init__(content, strict=strict, consume_whitespace_lines=consume_whitespace_lines)
        return

    @property
    def process_listing(self) -> List[ProcessItem]:
        return self._process_listing

    def _process_matches(self, pattern: RegExPattern, matches: dict):

        if pattern.exclass == "ProcessItem":
            pitem = ProcessItem(**matches)
            self._process_listing.append(pitem)

        return

if __name__ == "__main__":

    cmd_content = """
    PID TTY          TIME CMD
  82785 pts/3    00:00:00 bash
  88819 pts/3    00:00:00 ps
"""

    psrdr = CmdReaderPs(cmd_content)

    for pitem in psrdr.process_listing:
        print(pitem)
