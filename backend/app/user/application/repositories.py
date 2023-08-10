from abc import ABC, abstractmethod

from app.user.domain.model import Login, User, UserID


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        """
        :raises NotUniqueUserDataError: неуникальные логин, телефон или почта
        """

        raise NotImplementedError

    @abstractmethod
    async def get_by_login(self, login: Login) -> User:
        """
        :raises NotFoundUserError: пользователь не найден
        """

        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UserID) -> User:
        """
        :raises NotFoundUserError: пользователь не найден
        """

        raise NotImplementedError

    @abstractmethod
    async def update_refresh_tokens_at(self, user: User) -> None:
        raise NotImplementedError
