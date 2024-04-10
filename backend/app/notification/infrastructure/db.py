import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, MetaData
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.db.base import DictMixin
from app.notification.domain.notification import Body, Mark, Notification, NotificationID, Subtitle, Title
from app.notification.domain.user import User
from app.shared.domain.user import UserID


class NotificationBase(DeclarativeBase, DictMixin):
    metadata = MetaData(schema="notification")


class NotificationDB(NotificationBase):
    __tablename__ = "notification"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    recipients: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID, dimensions=1))
    title: Mapped[str] = mapped_column()
    subtitle: Mapped[str] = mapped_column()
    mark: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __init__(
        self,
        id_: uuid.UUID,
        recipients: list[uuid.UUID],
        title: str,
        subtitle: str,
        mark: str,
        body: str,
        created_at: datetime,
    ) -> None:
        super().__init__()

        self.id = id_
        self.recipients = recipients
        self.title = title
        self.subtitle = subtitle
        self.mark = mark
        self.body = body
        self.created_at = created_at

    def to_model(self) -> Notification:
        return Notification(
            id=NotificationID(self.id),
            recipients={UserID(recipient) for recipient in self.recipients},
            title=Title(self.title),
            subtitle=Subtitle(self.subtitle),
            mark=Mark(self.mark),
            body=Body(self.body),
            created_at=self.created_at,
        )

    @classmethod
    def from_model(cls, notification: Notification) -> "NotificationDB":
        return cls(
            id_=notification.id.value,
            recipients=[recipient.value for recipient in notification.recipients],
            title=notification.title.value,
            subtitle=notification.subtitle.value,
            mark=notification.mark.value,
            body=notification.body.value,
            created_at=notification.created_at,
        )


class UserDB(NotificationBase):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    read_notification_ids: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID, dimensions=1))

    def to_model(self) -> User:
        return User(
            id=UserID(self.id),
            read_notification_ids={NotificationID(id_) for id_ in self.read_notification_ids},
        )

    @classmethod
    def from_model(cls, user: User) -> "UserDB":
        return cls(
            id=user.id.value,
            read_notification_ids=[notification_id.value for notification_id in user.read_notification_ids],
        )
