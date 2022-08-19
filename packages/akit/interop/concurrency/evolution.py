from asyncio import CancelledError, exceptions
from typing import Callable, Dict, Optional, Tuple

import threading

from abc import ABC, abstractmethod
from concurrent import futures

from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Column

from akit.exceptions import AKitNotOverloadedError, AKitSemanticError

from akit.interop.concurrency.procedurecontext import ProcedureContext

class Evolution(ABC):

    def __init__(self, name: str, procedure: Callable, interactive=False, max_workers=5) -> None:
        
        self._name = name
        self._procedure = procedure
        self._interactive = interactive

        self._started = False
        self._completed = False

        self._procedure_contexts: Dict[ProcedureContext] = {}
        self._procedure_futures: Dict[futures.Future] = {}
        
        self._completion_future: futures.Future = None

        self._progress_console: Progress = None

        self._max_workers = max_workers
        self._executor = futures.ThreadPoolExecutor(self._max_workers, thread_name_prefix=self._name)

        self._completed_gate = threading.Event()

        return

    @property
    def completed(self):
        return self._completed

    @property
    def interactive(self):
        return self._interactive

    @property
    def procedure_contexts(self):
        return self._procedure_contexts
    
    @property
    def procedure_futures(self):
        return self._procedure_futures

    @property
    def started(self):
        return self._started

    def aggregate_results(self) -> Tuple[Dict, Dict]:
        """
        """
        
        if not self._started:
            errmsg = "{}: You must call the 'begin' method to start the evolution and wait for the " \
                "evolution to complete before calling the 'aggregate_results' method."
            raise AKitSemanticError(errmsg)
        
        if not self._completed:
            errmsg = "{}: You must call the 'wait_for_completion' to wait for the " \
                "evolution to complete before calling the 'aggregate_results' method."
            raise AKitSemanticError(errmsg)

        rtn_results = {}
        rtn_exceptions = {}

        for pident, pfuture in self._procedure_futures.items():

            try:
                fresult = pfuture.result()
                rtn_results[pident] = fresult
            except (CancelledError, TimeoutError) as ferr:
                rtn_exceptions[pident] = ferr
            except:
                fexc = pfuture.exception()
                rtn_exceptions[pident] = fexc

        return rtn_results, rtn_exceptions

    def begin(self):

        if self._interactive:
            self._progress_console = self._create_rich_progress()

        self._prepare_evolution()

        console_started = False
        
        try:
            self._procedure_contexts = self._create_procedure_contexts()

            if self._progress_console is not None:
                for pcontext in self._procedure_contexts.values():
                    pcontext.attach_to_progress_console(self._progress_console)

                self._progress_console.start()
                console_started = True

                self._setup_evolution()
        except:
            if console_started:
                self._progress_console.stop()
            raise

        self._completed_gate.clear()

        self._completion_future = self._executor.submit(self._perform_evolution)

        self._completion_future.add_done_callback(self._callback_cleanup_evolution)

        self._started = True

        return
    
    def shutdown(self):
        """
            Shutdown the executor.
        """
        self._executor.shutdown()
        return

    def wait_for_completion(self, timeout: Optional[float]=None):

        if not self._started:
            errmsg = "{}: You must call the 'begin' method to start the evolution before calling the 'wait_for_completion' method."
            raise AKitSemanticError(errmsg)
        
        self._completed_gate.wait(timeout=timeout)

        return

    @abstractmethod
    def _create_procedure_contexts(self) -> Dict:
        """
            Overloaded by derived types to create a dictionary of identifiers to :class:`ProcedureContext` objects
            that is used to run the procedures across the landscape.
        """
        errmsg = "The Evolution:_create_procedure_contexts method must be overloaded by derived types."
        raise AKitNotOverloadedError(errmsg)

    def _create_rich_progress(self):

        desc_column = TextColumn("{task.description}", table_column=Column(ratio=1))
        bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
        progress = Progress(desc_column, bar_column, "[progress.percentage]{task.percentage}%", expand=True)

        return progress

    def _prepare_evolution(self):
        """
            Overloaded by derived types to prepare the evolution for execution by gathering any
            information and data contexts that will be needed later in the :method:`_create_procedure_contexts`
            method to create the procedure contexts that will be used to run the procedures.
        """
        return

    def _cleanup_evolution(self):
        """
            Overloaded by derived types to perform any cleanup steps necessary after the performance
            of an evolution.

            ..note: If the setup of the evolution fails, the :method:`_cleanup_evolution` will not be run.
        """
        return

    def _callback_cleanup_evolution(self, future: futures.Future):
        """
            Helper method used to invoke '_cleanup_evolution' as a callback.
        """
        self._cleanup_evolution()

        self._completed = True
        self._completed_gate.set()
        return

    def _perform_evolution(self):
        """
            Perform the steps performance of an evolution across a set of landscape devices by submitting
            a procedure task to the executor for each of the procedure contexts that were created.

            ..note: If the setup of the evolution fails, the :method:`_perform_evolution` will not be run.
        """
        for pident, pcontext in self._procedure_contexts.items():
            pfuture = self._executor.submit(self._procedure, pcontext)
            self._procedure_futures[pident] = pfuture
        
        futures.wait(self._procedure_futures.values())

        if self._progress_console is not None:
            self._progress_console.stop()

        return
    
    def _setup_evolution(self):
        """
            Overloaded by derived types to perform any setup steps necessary before starting the performance
            of the evolution.

            ..note: If the setup of the evolution fails and the performance of the evolution should be cancelled,
                    then this method should raise an exception.  If the setup method raises an exception, the
                    :method:`_perform_evolution` and :method:`_cleanup_evolution` will not be run.
        """
        return

    def __enter__(self):
        """
            Allows for the creation of a ProcedureContext and assignment using 'as' in a 'with' context.
        """
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        """
            Allows for the use of a 'with' context to free up resources being consumed by the executor.
        """
        self.shutdown()
        return False


if __name__ == "__main__":

    import random
    import time

    class TestContext(ProcedureContext):

        def __init__(self, name: str):
            super().__init__(name)

            self.sleep_time = random.choice([5,6,7,8,9])
            return

        def attach_to_progress_console(self, progress_console: Progress):
            return

    def test_procedure(pcontext: TestContext):
        print("{}: sleeping {}".format(pcontext.identifier, pcontext.sleep_time))
        print()

        time.sleep(pcontext.sleep_time)

        print("{}: awake".format(pcontext.identifier))
        print()
        return

    class TestEvolution(Evolution):

        def __init__(self, procedure: Callable):
            super().__init__("test", procedure, max_workers=6)
            return

        def _create_procedure_contexts(self):
            procedure_contexts = {}

            for i in range(1, 6):
                id = str(i)
                procedure_contexts[id] = TestContext(id)

            return procedure_contexts

        def _cleanup_evolution(self):
            print("cleaning up evolution")
            return
 
    with TestEvolution(test_procedure) as evol:
        evol.begin()
        evol.wait_for_completion()
        rtn_results, rtn_exceptions = evol.aggregate_results()

        print(rtn_results)
        print(rtn_exceptions)
