from datetime import datetime, timezone

from result import Err, Ok, Result

from app.notification.application.dao import INotificationRepository, IUserRepository
from app.notification.application.errors import NotFoundUser
from app.notification.domain.notification import Body, Mark, Notification, NotificationID, Subtitle, Title
from app.shared.domain.user import UserID


async def notify(
    recipients: set[UserID],
    title: Title,
    subtitle: Subtitle,
    mark: Mark,
    body: Body,
    notification_repository: INotificationRepository,
) -> Notification:
    notification = Notification(
        id=NotificationID.generate(),
        recipients=recipients,
        title=title,
        subtitle=subtitle,
        mark=mark,
        body=body,
        created_at=datetime.now(timezone.utc),
    )

    await notification_repository.add(notification)

    return notification


async def read_notifications(
    user_id: UserID,
    notification_ids: set[NotificationID],
    user_repository: IUserRepository,
    notification_repository: INotificationRepository,
) -> Result[list[Notification], NotFoundUser]:
    user = await user_repository.get(user_id)

    if not user:
        return Err(NotFoundUser(user_id))

    read: list[Notification] = []

    async for notification in notification_repository.all_by_ids(notification_ids):
        read += [notification] if user.read(notification) else []

    await user_repository.merge(user)

    return Ok(read)
