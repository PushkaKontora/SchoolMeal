import sys
from abc import ABC, abstractmethod
from asyncio import Task, create_task

from app.shared.processes.abc import Process
from app.shared.processes.errors import ProcessHasAlreadyStarted, ProcessHasNotStartedYet


class AsyncProcess(Process, ABC):
    def __init__(self, exit_on_error: bool = True) -> None:
        super().__init__()
        self._exit_on_error = exit_on_error
        self._running_task: Task[None] | None = None

    def start(self) -> None:
        if self._running_task:
            raise ProcessHasAlreadyStarted

        self._running_task = create_task(self._run())
        self._running_task.add_done_callback(self._on_complete)

    def stop(self) -> None:
        if not self._running_task:
            raise ProcessHasNotStartedYet

        self._running_task.cancel()

    @abstractmethod
    async def _run(self) -> None:
        raise NotImplementedError

    def _on_complete(self, task: Task[None]) -> None:
        if task.cancelled():
            return

        error = task.exception()
        if error is not None:
            if self._exit_on_error:
                sys.exit(str(error))
