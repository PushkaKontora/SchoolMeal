from datetime import date

from result import Err, Ok, Result

from app.nutrition.application.dao import (
    IParentRepository,
    IPupilRepository,
    IRequestRepository,
    ISchoolClassRepository,
)
from app.nutrition.application.errors import NotFoundParent, NotFoundPupil, NotFoundSchoolClass
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.parent import ParentID, PupilIsAlreadyAttached
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.request import CannotSentRequestAfterDeadline, Request
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import Day, Period


async def resume_pupil_on_day(
    pupil_id: PupilID, day: Day, pupil_repository: IPupilRepository
) -> Result[None, NotFoundPupil]:
    pupil = await pupil_repository.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    resuming = pupil.resume_on_day(day)
    await pupil_repository.merge(resuming.unwrap())

    return Ok(None)


async def cancel_pupil_for_period(
    pupil_id: PupilID, period: Period, pupil_repository: IPupilRepository
) -> Result[None, NotFoundPupil]:
    pupil = await pupil_repository.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    cancelling = pupil.cancel_for_period(period)
    await pupil_repository.merge(cancelling.unwrap())

    return Ok(None)


async def resume_or_cancel_mealtimes_at_pupil(
    pupil_id: PupilID, mealtimes: dict[Mealtime, bool], pupil_repository: IPupilRepository
) -> Result[None, NotFoundPupil]:
    pupil = await pupil_repository.get_by_id(pupil_id)

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
) -> Result[None, NotFoundSchoolClass | CannotSentRequestAfterDeadline]:
    school_class = await class_repository.get_by_id(class_id)

    if not school_class:
        return Err(NotFoundSchoolClass())

    pupils = await pupil_repository.all_by_class_id(class_id=school_class.id)
    submitting = Request.submit_to_canteen(school_class, pupils, overrides, on_date)

    if isinstance(submitting, Err):
        return submitting

    await request_repository.merge(request=submitting.unwrap())

    return Ok(None)


async def attach_child_to_parent(
    parent_id: ParentID, pupil_id: PupilID, parent_repository: IParentRepository, pupil_repository: IPupilRepository
) -> Result[None, NotFoundParent | NotFoundPupil | PupilIsAlreadyAttached]:
    if not (parent := await parent_repository.get_by_id(id_=parent_id)):
        return Err(NotFoundParent())

    if not (pupil := await pupil_repository.get_by_id(id_=pupil_id)):
        return Err(NotFoundPupil())

    attaching = parent.attach_child(pupil)

    if isinstance(attaching, Err):
        return attaching

    await parent_repository.merge(parent)

    return Ok(attaching.unwrap())
