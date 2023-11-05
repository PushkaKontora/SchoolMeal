from abc import ABC, abstractmethod
from uuid import UUID

from app.account.domain.credential import Credential
from app.account.domain.login import Login
from app.account.domain.session import Session
from app.account.domain.user import User


class NotFoundCredentialError(Exception):
    pass


class NotFoundSessionError(Exception):
    pass


class NotUniqueLoginError(Exception):
    pass


class NotFoundUserError(Exception):
    pass


class ICredentialsRepository(ABC):
    @abstractmethod
    async def get_by_login(self, login: Login) -> Credential:
        """
        :raise NotFoundCredentialsError: не найден пользователь с заданным логином
        """

        raise NotImplementedError


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
    async def get_all_by_credential_id_and_revoked(self, credential_id: UUID, revoked: bool) -> list[Session]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_credential_id_and_device_id_and_revoked(
        self, credential_id: UUID, device_id: UUID, revoked: bool
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
    async def get_by_credential_id(self, credential_id: UUID) -> User:
        """
        :raise NotFoundUserError: не найден пользователь
        """

        raise NotImplementedError
