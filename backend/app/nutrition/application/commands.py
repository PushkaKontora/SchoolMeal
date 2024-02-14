from datetime import date

from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.nutrition.application.dao import IPupilDAO, IRequestDAO, ISchoolClassDAO
from app.nutrition.application.errors import NotFoundPupil, NotFoundSchoolClass
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.request import CannotSentRequestAfterDeadline, Request
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import Day, Period
from app.nutrition.infrastructure.dependencies import NutritionContainer


@inject
async def resume_on_day(
    pupil_id: PupilID, day: Day, pupils: IPupilDAO = Provide[NutritionContainer.pupil_dao]
) -> Result[None, NotFoundPupil]:
    pupil = await pupils.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    pupil.resume_on_day(day)
    await pupils.update(pupil)

    return Ok(None)


@inject
async def cancel_for_period(
    pupil_id: PupilID, period: Period, pupils: IPupilDAO = Provide[NutritionContainer.pupil_dao]
) -> Result[None, NotFoundPupil]:
    pupil = await pupils.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    pupil.cancel_for_period(period)
    await pupils.update(pupil)

    return Ok(None)


@inject
async def resume_on_mealtime(
    pupil_id: PupilID, mealtime: Mealtime, pupils: IPupilDAO = Provide[NutritionContainer.pupil_dao]
) -> Result[None, NotFoundPupil]:
    pupil = await pupils.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    pupil.resume_on_mealtime(mealtime)
    await pupils.update(pupil)

    return Ok(None)


@inject
async def cancel_from_mealtime(
    pupil_id: PupilID, mealtime: Mealtime, pupils: IPupilDAO = Provide[NutritionContainer.pupil_dao]
) -> Result[None, NotFoundPupil]:
    pupil = await pupils.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    pupil.cancel_from_mealtime(mealtime)
    await pupils.update(pupil)

    return Ok(None)


@inject
async def submit_request_to_canteen(
    class_id: ClassID,
    on_date: date,
    overrides: dict[PupilID, set[Mealtime]],
    school_class_dao: ISchoolClassDAO = Provide[NutritionContainer.school_class_dao],
    pupil_dao: IPupilDAO = Provide[NutritionContainer.pupil_dao],
    request_dao: IRequestDAO = Provide[NutritionContainer.request_dao],
) -> Result[None, NotFoundSchoolClass | CannotSentRequestAfterDeadline]:
    school_class = await school_class_dao.get_by_id(class_id)

    if not school_class:
        return Err(NotFoundSchoolClass())

    pupils = await pupil_dao.get_all_by_class_id(class_id=school_class.id)
    submitting = Request.submit_to_canteen(school_class, pupils, overrides, on_date)

    if isinstance(submitting, Err):
        return submitting

    await request_dao.upsert(request=submitting.unwrap())

    return Ok(None)
