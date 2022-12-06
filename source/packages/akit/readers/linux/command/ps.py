
from typing import List, NamedTuple, Union

from akit.xregex.regexreader import RegExReader, RegExPattern

class ProcessItem(NamedTuple):
    pid: int
    tty: str
    time: str
    cmd: str

class CmdReaderPs(RegExReader):
    """
        Reader for processing the output of the 'ps' command.
    """

    EXPECTED_LINES = [
        RegExPattern(
            r"^[\s]*(?P<hpid>[A-Za-z]+)[\s]+(?P<htty>[A-Za-z]+)[\s]+(?P<htime>[A-Za-z]+)[\s]+(?P<hcmd>[A-Za-z]+)",
            consume=True),
        RegExPattern(
            r"^[\s]*(?P<pid>[\S]+)[\s]+(?P<tty>[\S]+)[\s]+(?P<time>[\S]+)[\s]+(?P<cmd>[\S]+)",
            destination="process_listing", match_type=ProcessItem, repeats=True)
    ]

    def __init__(self, content:Union[List, str], strict=False):
        self._process_listing = []

        super().__init__(content, strict=strict)
        return

    @property
    def process_listing(self) -> List[ProcessItem]:
        return self._process_listing


if __name__ == "__main__":

    cmd_content = """
    PID TTY          TIME CMD
  82785 pts/3    00:00:00 bash
  88819 pts/3    00:00:00 ps
"""

    psrdr = CmdReaderPs(cmd_content)

    for pitem in psrdr.process_listing:
        print(pitem)
