from abc import ABC, abstractmethod
from typing import AsyncIterator

from app.notification.domain.notification import Notification, NotificationID
from app.notification.domain.user import User
from app.shared.domain.user import UserID


class INotificationRepository(ABC):
    @abstractmethod
    def all(self) -> AsyncIterator[Notification]:
        raise NotImplementedError

    @abstractmethod
    def all_by_ids(self, ids: set[NotificationID]) -> AsyncIterator[Notification]:
        raise NotImplementedError

    @abstractmethod
    def all_by_user_id(self, user_id: UserID) -> AsyncIterator[Notification]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, notification: Notification) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, notification: Notification) -> None:
        raise NotImplementedError


class IUserRepository(ABC):
    @abstractmethod
    async def get(self, id_: UserID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def merge(self, user: User) -> None:
        raise NotImplementedError
