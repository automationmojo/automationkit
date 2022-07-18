from typing import Callable, List

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

        self._procedure_contexts: List[ProcedureContext] = []
        self._procedure_futures: List[futures.Future] = []
        
        self._completion_future: futures.Future = None

        self._progress_console: Progress = None

        self._max_workers = max_workers
        self._executor = futures.ThreadPoolExecutor(self._max_workers, thread_name_prefix=self._name)

        return

    @property
    def interactive(self):
        return self._interactive

    def begin(self):

        if self._interactive:
            self._progress_console = self._create_rich_progress()

        self._prepare_evolution()

        console_started = False
        
        try:
            self._procedure_contexts = self._create_procedure_contexts()

            if self._progress_console is not None:
                for pcontext in self._procedure_contexts:
                    pcontext.attach_to_progress_console(self._progress_console)

                self._progress_console.start()
                console_started = False

                self._setup_evolution()
        except:
            if console_started:
                self._progress_console.stop()
            raise

        self._completion_future = self._executor.submit(self._perform_evolution)

        self._completion_future.add_done_callback(self._callback_cleanup_evolution)

        self._started = True

        return
    
    def wait_for_completion(self, timeout: float=20):
        if not self._started:
            errmsg = "{}: You must call the 'begin' method to start the evolution before calling the 'wait_for_completion' method."
            raise AKitSemanticError(errmsg)
        
        futures.wait([self._completion_future], timeout)

        return

    @abstractmethod
    def _create_procedure_contexts(self):
        errmsg = "The Evolution:_create_procedure_contexts method must be overloaded by derived types."
        raise AKitNotOverloadedError(errmsg)

    def _create_rich_progress(self):

        desc_column = TextColumn("{task.description}", table_column=Column(ratio=1))
        bar_column = BarColumn(bar_width=None, table_column=Column(ration=2))
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

    def _callback_cleanup_evolution(self, future):
        """
            Helper method used to invoke '_cleanup_evolution' as a callback.
        """
        self._cleanup_evolution()
        return

    def _perform_evolution(self):
        """
            Perform the steps performance of an evolution across a set of landscape devices by submitting
            a procedure task to the executor for each of the procedure contexts that were created.

            ..note: If the setup of the evolution fails, the :method:`_perform_evolution` will not be run.
        """
        for pcontext in self._procedure_contexts:
            pfuture = self._executor.submit(self._procedure, pcontext)
            self._procedure_futures.append(pfuture)
        
        futures.wait(self._procedure_futures)

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


if __name__ == "__main__":

    import random
    import time

    class TestContext(ProcedureContext):

        def __init__(self, index):
            super().__init__()

            self.index = index
            self.sleep_time = random.choice([5,6,7,8,9])
            return

        def attach_to_progress_console(self, progress_console: Progress):
            return

    def test_procedure(pcontext: TestContext):
        print("{}: sleeping {}".format(pcontext.index, pcontext.sleep_time))
        print()

        time.sleep(pcontext.sleep_time)

        print("{}: awake".format(pcontext.index))
        print()
        return

    class TestEvolution(Evolution):

        def __init__(self, procedure: Callable):
            super().__init__("test", procedure, max_workers=6)
            return

        def _create_procedure_contexts(self):
            procedure_contexts = []

            for i in range(1, 6):
                procedure_contexts.append(TestContext(i))

            return procedure_contexts

        def _cleanup_evolution(self):
            print("cleaning up evolution")
            return
 
    evol = TestEvolution(test_procedure)
    evol.begin()
    evol.wait_for_completion()