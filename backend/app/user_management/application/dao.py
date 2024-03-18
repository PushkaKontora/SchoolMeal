from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.shared.domain.user import UserID
from app.user_management.domain.credentials import Login
from app.user_management.domain.jwt import Session
from app.user_management.domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: UserID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_login(self, login: Login) -> User | None:
        raise NotImplementedError


class ISessionRepository(ABC):
    @abstractmethod
    async def add(self, session: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    async def pop(self, id_: UUID) -> Session | None:
        raise NotImplementedError

    @abstractmethod
    async def count_by_user_id(self, user_id: UserID) -> int:
        raise NotImplementedError

    @abstractmethod
    async def remove_all_by_user_id(self, user_id: UserID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_all_expired(self, beginning_with: datetime) -> None:
        raise NotImplementedError
