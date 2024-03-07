from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dependency_injector.wiring import Provide, inject

from app.nutrition.application.dao import IPupilRepository, IRequestRepository, ISchoolClassRepository
from app.nutrition.domain.services import prefill_request
from app.nutrition.domain.time import SUBMITTING_DEADLINE, now
from app.nutrition.infrastructure.dependencies import NutritionContainer


scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(
    CronTrigger(
        hour=SUBMITTING_DEADLINE.hour,
        minute=SUBMITTING_DEADLINE.minute,
        timezone=SUBMITTING_DEADLINE.tzinfo,
    )
)
@inject
async def save_drafts_of_requests_everyday(
    class_repository: ISchoolClassRepository = Provide[NutritionContainer.class_repository],
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
    request_repository: IRequestRepository = Provide[NutritionContainer.request_repository],
) -> None:
    today = now().date()

    for school_class in await class_repository.all():
        if await request_repository.exists_by_class_id_and_date(class_id=school_class.id, on_date=today):
            continue

        pupils = await pupil_repository.all_by_class_id(class_id=school_class.id)

        request = prefill_request(school_class, pupils, on_date=today, overrides={})
        await request_repository.add(request)
