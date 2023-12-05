from abc import ABC, abstractmethod
from collections import deque
from types import TracebackType


class ISession(ABC):
    @abstractmethod
    async def begin_nested(self) -> "ISession":
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class IRootSession(ISession, ABC):
    @abstractmethod
    async def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError


class UnitOfWork:
    def __init__(self, session: IRootSession) -> None:
        self._root = session
        self._sessions: deque[ISession] = deque()

    async def __aenter__(self) -> ISession:
        if not self._sessions:
            self._sessions.append(self._root)
            return self._root

        nested = await self._sessions[-1].begin_nested()
        self._sessions.append(nested)

        return nested

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        session = self._sessions.pop()

        if exc_type:
            await session.rollback()

        if not self._sessions:
            await self._root.close()
