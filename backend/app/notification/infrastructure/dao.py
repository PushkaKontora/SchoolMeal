from typing import AsyncContextManager, AsyncIterator, Callable

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.notification.application.dao import INotificationRepository, IUserRepository
from app.notification.domain.notification import Notification, NotificationID
from app.notification.domain.user import User
from app.notification.infrastructure.db import NotificationDB, UserDB
from app.shared.domain.user import UserID


class AlchemyNotificationRepository(INotificationRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def all(self) -> AsyncIterator[Notification]:
        query = select(NotificationDB)

        async with self._session_factory() as session:
            async for notification_db in await session.stream_scalars(query):
                yield notification_db.to_model()

    async def all_by_ids(self, ids: set[NotificationID]) -> AsyncIterator[Notification]:
        query = select(NotificationDB).where(NotificationDB.id.in_({id_.value for id_ in ids}))

        async with self._session_factory() as session:
            async for notification_db in await session.stream_scalars(query):
                yield notification_db.to_model()

    async def all_by_user_id(self, user_id: UserID) -> AsyncIterator[Notification]:
        query = select(NotificationDB).where(NotificationDB.recipients.contains([user_id.value]))

        async with self._session_factory() as session:
            async for notification_db in await session.stream_scalars(query):
                yield notification_db.to_model()

    async def add(self, notification: Notification) -> None:
        notification_db = NotificationDB.from_model(notification)

        async with self._session_factory() as session:
            session.add(notification_db)
            await session.commit()

    async def delete(self, notification: Notification) -> None:
        query = delete(NotificationDB).where(NotificationDB.id == notification.id.value)

        async with self._session_factory() as session:
            await session.execute(query)


class AlchemyUserRepository(IUserRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get(self, id_: UserID) -> User | None:
        query = select(UserDB).where(UserDB.id == id_.value).limit(1)

        async with self._session_factory() as session:
            user_db = await session.scalar(query)

            return user_db.to_model() if user_db else None

    async def merge(self, user: User) -> None:
        user_db = UserDB.from_model(user).dict()

        query = (
            insert(UserDB)
            .values(user_db)
            .on_conflict_do_update(
                index_elements=[UserDB.id],
                set_=user_db,
            )
        )

        async with self._session_factory() as session:
            await session.execute(query)
            await session.commit()
