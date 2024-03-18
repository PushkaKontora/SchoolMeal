from datetime import date

from result import Err, Ok, Result

from app.nutrition.application.dao.pupils import IPupilRepository, PupilByClassID
from app.nutrition.application.dao.requests import IRequestRepository
from app.nutrition.application.dao.school_classes import ISchoolClassRepository
from app.nutrition.application.errors import NotFoundPupil, NotFoundSchoolClass
from app.nutrition.domain import services
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import CannotCancelAfterDeadline, CannotResumeAfterDeadline, PupilID
from app.nutrition.domain.request import CannotSubmitAfterDeadline, Request
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.time import Day, Period


async def resume_pupil_on_day(
    pupil_id: PupilID, day: Day, pupil_repository: IPupilRepository
) -> Result[None, NotFoundPupil | CannotResumeAfterDeadline]:
    pupil = await pupil_repository.get(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    resuming = pupil.resume_on_day(day)

    if isinstance(resuming, Err):
        return resuming

    await pupil_repository.merge(resuming.unwrap())

    return Ok(None)


async def cancel_pupil_for_period(
    pupil_id: PupilID, period: Period, pupil_repository: IPupilRepository
) -> Result[None, NotFoundPupil | CannotCancelAfterDeadline]:
    pupil = await pupil_repository.get(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    cancelling = pupil.cancel_for_period(period)

    if isinstance(cancelling, Err):
        return cancelling

    await pupil_repository.merge(cancelling.unwrap())

    return Ok(None)


async def resume_or_cancel_mealtimes_at_pupil(
    pupil_id: PupilID,
    mealtimes: dict[Mealtime, bool],
    pupil_repository: IPupilRepository,
) -> Result[None, NotFoundPupil]:
    pupil = await pupil_repository.get(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    for mealtime, resumed in mealtimes.items():
        (pupil.resume_on_mealtime if resumed else pupil.cancel_from_mealtime)(mealtime)

    await pupil_repository.merge(pupil)

    return Ok(None)


async def submit_request_to_canteen(
    class_id: ClassID,
    on_date: date,
    overrides: dict[PupilID, set[Mealtime]],
    class_repository: ISchoolClassRepository,
    pupil_repository: IPupilRepository,
    request_repository: IRequestRepository,
) -> Result[None, NotFoundSchoolClass | CannotSubmitAfterDeadline]:
    submitting = (await prefill_request(class_id, on_date, overrides, class_repository, pupil_repository)).and_then(
        lambda x: x.submit_manually()
    )

    if isinstance(submitting, Err):
        return submitting

    await request_repository.merge(submitting.unwrap())

    return Ok(None)


async def prefill_request(
    class_id: ClassID,
    on_date: date,
    overrides: dict[PupilID, set[Mealtime]],
    class_repository: ISchoolClassRepository,
    pupil_repository: IPupilRepository,
) -> Result[Request, NotFoundSchoolClass]:
    school_class = await class_repository.get(class_id)

    if not school_class:
        return Err(NotFoundSchoolClass())

    pupils = await pupil_repository.all(PupilByClassID(school_class.id))

    return Ok(services.prefill_request(school_class, pupils, on_date, overrides))
