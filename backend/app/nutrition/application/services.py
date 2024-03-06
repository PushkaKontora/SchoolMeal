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
from app.nutrition.domain.pupil import CannotCancelAfterDeadline, CannotResumeAfterDeadline, PupilID
from app.nutrition.domain.request import CannotSubmitAfterDeadline, Request, Status
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.time import Day, Period


async def resume_pupil_on_day(
    pupil_id: PupilID, day: Day, pupil_repository: IPupilRepository
) -> Result[None, NotFoundPupil | CannotResumeAfterDeadline]:
    pupil = await pupil_repository.get_by_id(pupil_id)

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
    pupil = await pupil_repository.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    cancelling = pupil.cancel_for_period(period)

    if isinstance(cancelling, Err):
        return cancelling

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
    day: Day,
    overrides: dict[PupilID, set[Mealtime]],
    class_repository: ISchoolClassRepository,
    pupil_repository: IPupilRepository,
    request_repository: IRequestRepository,
) -> Result[None, NotFoundSchoolClass | CannotSubmitAfterDeadline]:
    prefilling = await prefill_request(class_id, day, overrides, class_repository, pupil_repository)
    submitting = prefilling.and_then(lambda request: request.submit_manually())

    if isinstance(submitting, Err):
        return submitting

    await request_repository.merge(submitting.unwrap())

    return Ok(None)


async def prefill_request(
    class_id: ClassID,
    day: Day,
    overrides: dict[PupilID, set[Mealtime]],
    class_repository: ISchoolClassRepository,
    pupil_repository: IPupilRepository,
) -> Result[Request, NotFoundSchoolClass]:
    school_class = await class_repository.get_by_id(class_id)

    if not school_class:
        return Err(NotFoundSchoolClass())

    pupils = await pupil_repository.all_by_class_id(class_id=school_class.id)

    mealtimes: dict[Mealtime, set[PupilID]] = {mealtime_: set() for mealtime_ in school_class.mealtimes}
    for pupil in pupils:
        for mealtime, request_ in mealtimes.items():
            eats = pupil.does_eat(day, mealtime)

            if pupil.id in overrides:
                eats = mealtime in overrides[pupil.id]

            if eats:
                request_.add(pupil.id)

    return Ok(
        Request(
            class_id=school_class.id,
            on_date=day.value,
            mealtimes=mealtimes,
            status=Status.PREFILLED,
        )
    )


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
