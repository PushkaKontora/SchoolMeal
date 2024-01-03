import asyncio
from abc import ABC, abstractmethod
from typing import NoReturn

from app.shared.event_bus.connectors.abc import FailedSending, IBusConnector
from app.shared.event_bus.outbox import Status
from app.shared.event_bus.unit_of_work import OutboxContext
from app.shared.unit_of_work.abc import IUnitOfWork


class IEventsSendingJob(ABC):
    @abstractmethod
    async def run(self) -> NoReturn:
        raise NotImplementedError


class EventsSendingJob(IEventsSendingJob):
    def __init__(self, unit_of_work: IUnitOfWork[OutboxContext], bus: IBusConnector, delay_seconds: int = 3) -> None:
        self._unit_of_work = unit_of_work
        self._bus = bus
        self._delay_seconds = delay_seconds

    async def run(self) -> NoReturn:
        async with self._bus.sender() as sender:
            while True:
                async with self._unit_of_work as context:
                    if not (outbox := await context.outboxes.get_first_with(status=Status.UNDELIVERED)):
                        continue

                    try:
                        await sender.send(outbox)
                        outbox.deliver()
                    except FailedSending as error:
                        outbox.fail(error=error.message)

                    await context.outboxes.update(outbox)
                    await self._unit_of_work.commit()

                await asyncio.sleep(self._delay_seconds)
