from datetime import date

from result import Err, Ok, Result

from app.nutrition.application.dao import IPupilDAO, IRequestDAO, ISchoolClassDAO
from app.nutrition.application.errors import NotFoundPupil, NotFoundSchoolClass
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.request import CannotSentRequestAfterDeadline, Request
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import Day, Period


async def resume_on_day(pupil_id: PupilID, day: Day, pupil_dao: IPupilDAO) -> Result[None, NotFoundPupil]:
    pupil = await pupil_dao.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    pupil.resume_on_day(day)
    await pupil_dao.update(pupil)

    return Ok(None)


async def cancel_for_period(pupil_id: PupilID, period: Period, pupil_dao: IPupilDAO) -> Result[None, NotFoundPupil]:
    pupil = await pupil_dao.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    pupil.cancel_for_period(period)
    await pupil_dao.update(pupil)

    return Ok(None)


async def resume_or_cancel_mealtimes_at_pupil(
    pupil_id: PupilID, mealtimes: dict[Mealtime, bool], pupil_dao: IPupilDAO
) -> Result[None, NotFoundPupil]:
    pupil = await pupil_dao.get_by_id(pupil_id)

    if not pupil:
        return Err(NotFoundPupil())

    for mealtime, resumed in mealtimes.items():
        (pupil.resume_on_mealtime if resumed else pupil.cancel_from_mealtime)(mealtime)

    await pupil_dao.update(pupil)

    return Ok(None)


async def submit_request_to_canteen(
    class_id: ClassID,
    on_date: date,
    overrides: dict[PupilID, set[Mealtime]],
    school_class_dao: ISchoolClassDAO,
    pupil_dao: IPupilDAO,
    request_dao: IRequestDAO,
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