from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from result import Result


class Command(BaseModel, ABC):
    pass


TCommand = TypeVar("TCommand")
TError = TypeVar("TError")


class ICommandHandler(Generic[TCommand, TError], ABC):
    @abstractmethod
    async def handle(self, command: TCommand) -> Result[None, TError]:
        raise NotImplementedError
