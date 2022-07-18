

from abc import ABC, abstractmethod

from rich.progress import Progress

from akit.exceptions import AKitNotOverloadedError

class ProcedureContext(ABC):

    def __init__(self, identifier: str):
        self._identifier = identifier
        return

    @property
    def identifier(self):
        return self._identifier

    @abstractmethod
    def attach_to_progress_console(self, progress_console: Progress):
        errmsg = "The ProcedureContext:attach_to_progress_console method must be overloaded by derived types."
        raise AKitNotOverloadedError(errmsg)
