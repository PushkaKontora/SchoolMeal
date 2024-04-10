from uuid import UUID

from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.notification.application import services
from app.notification.application.dao import INotificationRepository
from app.notification.dependencies import NotificationContainer
from app.notification.domain.notification import Body, Mark, Subtitle, Title
from app.shared.domain.user import UserID


@inject
async def notify(
    recipients: set[UUID],
    title: str,
    subtitle: str,
    mark: str,
    body: str,
    notification_repository: INotificationRepository = Provide[NotificationContainer.notification_repository],
) -> Result[UUID, str]:
    try:
        recipients_ = {UserID(recipient) for recipient in recipients}
        title_ = Title(title)
        subtitle_ = Subtitle(subtitle)
        mark_ = Mark(mark)
        body_ = Body(body)
    except ValueError as error:
        return Err(str(error))

    notification = await services.notify(
        recipients=recipients_,
        title=title_,
        subtitle=subtitle_,
        mark=mark_,
        body=body_,
        notification_repository=notification_repository,
    )

    return Ok(notification.id.value)
