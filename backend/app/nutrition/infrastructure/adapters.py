from loguru import logger

from app.notification.api.ipc import notify
from app.nutrition.application.adapters import INotificationAdapter
from app.nutrition.domain.teacher import TeacherID


class NotificationAdapter(INotificationAdapter):
    async def notify_teacher_about_cancellation(
        self, teacher_id: TeacherID, title: str, subtitle: str, mark: str, body: str
    ) -> None:
        result = await notify(
            recipients={teacher_id.value},
            title=title,
            subtitle=subtitle,
            mark=mark,
            body=body,
        )

        if result.is_err():
            logger.error(str(result.unwrap_err()))
