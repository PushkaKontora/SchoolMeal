from datetime import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dependency_injector.wiring import Provide, inject

from app.notification.application.dao import INotificationRepository
from app.notification.dependencies import NotificationContainer


scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(CronTrigger(hour=0, minute=0, timezone=timezone.utc))
@inject
async def delete_old_notification(
    notification_repository: INotificationRepository = Provide[NotificationContainer.notification_repository],
) -> None:
    async for notification in notification_repository.all():
        if not notification.is_old:
            continue

        await notification_repository.delete(notification)
