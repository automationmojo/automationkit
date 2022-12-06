

from abc import ABC, abstractmethod

from rich.progress import Progress

from akit.exceptions import AKitNotOverloadedError

class ProcedureContext(ABC):

    def __init__(self, identifier: str):
        self._identifier = identifier
        self._progress_console = None
        return

    @property
    def identifier(self):
        return self._identifier

    @property
    def progress_console(self):
        return self._progress_console

    @abstractmethod
    def attach_to_progress_console(self, progress_console: Progress):
        errmsg = "The ProcedureContext:attach_to_progress_console method must be overloaded by derived types."
        raise AKitNotOverloadedError(errmsg)
