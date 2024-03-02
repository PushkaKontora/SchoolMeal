from datetime import date
from uuid import UUID

from result import Err, Ok, Result

from app.ipc.nutrition.api import INutritionAPI
from app.ipc.nutrition.dto import Override
from app.nutrition.application.dao import IPupilDAO, IRequestDAO, ISchoolClassDAO
from app.nutrition.application.errors import NotFoundPupil, NotFoundSchoolClass
from app.nutrition.application.services import (
    cancel_for_period,
    resume_on_day,
    resume_or_cancel_mealtimes_at_pupil,
    submit_request_to_canteen,
)
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.request import CannotSentRequestAfterDeadline
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import Day, Period


class NutritionAPI(INutritionAPI):
    def __init__(self, pupil_dao: IPupilDAO, school_class_dao: ISchoolClassDAO, request_dao: IRequestDAO) -> None:
        self._pupil_dao = pupil_dao
        self._school_class_dao = school_class_dao
        self._request_dao = request_dao

    async def resume_pupil_on_day(self, pupil_id: str, day: date) -> Result[None, str]:
        resuming = await resume_on_day(pupil_id=PupilID(pupil_id), day=Day(day), pupil_dao=self._pupil_dao)

        match resuming:
            case Err(NotFoundPupil()):
                return Err(f"Не найден ученик с id={pupil_id}")

        return Ok(resuming.unwrap())

    async def cancel_pupil_for_period(self, pupil_id: str, start: date, end: date) -> Result[None, str]:
        try:
            period = Period(start=start, end=end)
        except ValueError as error:
            return Err(str(error))

        cancelling = await cancel_for_period(pupil_id=PupilID(pupil_id), period=period, pupil_dao=self._pupil_dao)

        match cancelling:
            case Err(NotFoundPupil()):
                return Err(f"Не найден ученик с id={pupil_id}")

        return Ok(cancelling.unwrap())

    async def update_mealtimes_at_pupil(
        self, pupil_id: str, breakfast: bool | None = None, dinner: bool | None = None, snacks: bool | None = None
    ) -> Result[None, str]:
        mealtimes = {
            mealtime: toggle
            for mealtime, toggle in [
                (Mealtime.BREAKFAST, breakfast),
                (Mealtime.DINNER, dinner),
                (Mealtime.SNACKS, snacks),
            ]
            if toggle is not None
        }

        result = await resume_or_cancel_mealtimes_at_pupil(
            pupil_id=PupilID(pupil_id), mealtimes=mealtimes, pupil_dao=self._pupil_dao
        )

        match result:
            case Err(NotFoundPupil()):
                return Err(f"Не найден ученик с id={pupil_id}")

        return Ok(result.unwrap())

    async def submit_request_to_canteen(
        self, class_id: UUID, on_date: date, overrides: set[Override]
    ) -> Result[None, str]:
        overrides_ = {
            PupilID(override.pupil_id): {
                mealtime
                for mealtime, value in [
                    (Mealtime.BREAKFAST, override.breakfast),
                    (Mealtime.DINNER, override.dinner),
                    (Mealtime.SNACKS, override.snacks),
                ]
                if value
            }
            for override in overrides
        }

        submitting = await submit_request_to_canteen(
            class_id=ClassID(class_id),
            on_date=on_date,
            overrides=overrides_,
            school_class_dao=self._school_class_dao,
            pupil_dao=self._pupil_dao,
            request_dao=self._request_dao,
        )

        match submitting:
            case Err(NotFoundSchoolClass()):
                return Err(f"Не найден класс с id={class_id}")

            case Err(CannotSentRequestAfterDeadline(deadline=deadline)):
                return Err(f"Невозможно отправить заявку на {on_date} после {deadline.isoformat()}")

        return Ok(submitting.unwrap())
