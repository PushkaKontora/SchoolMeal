from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.nutrition.application.dao import IPupilDAO
from app.nutrition.application.errors import NotFoundPupil
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import PupilID
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

    pupil.cancel_on_mealtime(mealtime)
    await pupils.update(pupil)

    return Ok(None)
