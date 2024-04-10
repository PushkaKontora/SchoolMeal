from datetime import datetime
from uuid import UUID

from app.notification.domain.notification import Notification
from app.notification.domain.user import User
from app.shared.api.schemas import FrontendBody


class NotificationOut(FrontendBody):
    id: UUID
    is_read: bool
    title: str
    subtitle: str
    mark: str
    body: str
    created_at: datetime

    @classmethod
    def from_model(cls, user: User, notification: Notification) -> "NotificationOut":
        return cls(
            id=notification.id.value,
            is_read=user.did_read(notification),
            title=notification.title.value,
            subtitle=notification.subtitle.value,
            mark=notification.mark.value,
            body=notification.body.value,
            created_at=notification.created_at,
        )


class ReadNotificationBody(FrontendBody):
    ids: set[UUID]
