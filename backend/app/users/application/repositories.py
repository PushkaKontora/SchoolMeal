from abc import ABC, abstractmethod
from uuid import UUID

from app.users.domain.login import Login
from app.users.domain.session import Session
from app.users.domain.user import User


class NotFoundSessionError(Exception):
    pass


class NotUniqueLoginError(Exception):
    pass


class NotFoundUserError(Exception):
    pass


class ISessionsRepository(ABC):
    @abstractmethod
    async def save(self, *sessions: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *sessions: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_jti(self, jti: UUID) -> Session:
        """
        :raise NotFoundSessionError: не найдена сессия для рефреш-токена
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user_id_and_revoked(self, user_id: UUID, revoked: bool) -> list[Session]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user_id_and_device_id_and_revoked(
        self, user_id: UUID, device_id: UUID, revoked: bool
    ) -> list[Session]:
        raise NotImplementedError


class IUsersRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        """
        :raise NotUniqueLoginError: неуникальный логин
        """

        raise NotImplementedError

    @abstractmethod
    async def get_by_login(self, login: Login) -> User:
        """
        :raise NotFoundUserError: не найден пользователь
        """

        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User:
        """
        :raise NotFoundUserError: не найден пользователь
        """

        raise NotImplementedError
