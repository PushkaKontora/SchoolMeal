from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dependency_injector.wiring import Provide, inject

from app.user_management.application.dao import ISessionRepository
from app.user_management.infrastructure.dependencies import IdentityContainer


scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(IntervalTrigger(hours=1), max_instances=1)
@inject
async def delete_all_expired_session(
    session_repository: ISessionRepository = Provide[IdentityContainer.session_repository],
) -> None:
    now = datetime.now(timezone.utc)

    await session_repository.delete_all_expired(beginning_with=now)
