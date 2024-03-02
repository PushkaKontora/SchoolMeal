from datetime import date
from uuid import UUID

from result import Err, Ok, Result

from app.ipc.nutrition.api import INutritionAPI
from app.ipc.nutrition.dto import Override
from app.nutrition.application.dao import (
    IParentRepository,
    IPupilRepository,
    IRequestRepository,
    ISchoolClassRepository,
)
from app.nutrition.application.errors import NotFoundParent, NotFoundPupil, NotFoundSchoolClass
from app.nutrition.application.services import (
    attach_child_to_parent,
    cancel_for_period,
    resume_on_day,
    resume_or_cancel_mealtimes_at_pupil,
    submit_request_to_canteen,
)
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.parent import ParentID, PupilIsAlreadyAttached
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.request import CannotSentRequestAfterDeadline
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import Day, Period


class NutritionAPI(INutritionAPI):
    def __init__(
        self,
        pupil_repository: IPupilRepository,
        school_class_repository: ISchoolClassRepository,
        request_repository: IRequestRepository,
        parent_repository: IParentRepository,
    ) -> None:
        self._pupil_repository = pupil_repository
        self._school_class_repository = school_class_repository
        self._request_repository = request_repository
        self._parent_repository = parent_repository

    async def resume_pupil_on_day(self, pupil_id: str, day: date) -> Result[None, str]:
        resuming = await resume_on_day(pupil_id=PupilID(pupil_id), day=Day(day), pupil_dao=self._pupil_repository)

        match resuming:
            case Err(NotFoundPupil()):
                return Err(f"Не найден ученик с id={pupil_id}")

        return Ok(resuming.unwrap())

    async def cancel_pupil_for_period(self, pupil_id: str, start: date, end: date) -> Result[None, str]:
        try:
            period = Period(start=start, end=end)
        except ValueError as error:
            return Err(str(error))

        cancelling = await cancel_for_period(
            pupil_id=PupilID(pupil_id), period=period, pupil_dao=self._pupil_repository
        )

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
            pupil_id=PupilID(pupil_id), mealtimes=mealtimes, pupil_dao=self._pupil_repository
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
            school_class_dao=self._school_class_repository,
            pupil_dao=self._pupil_repository,
            request_dao=self._request_repository,
        )

        match submitting:
            case Err(NotFoundSchoolClass()):
                return Err(f"Не найден класс с id={class_id}")

            case Err(CannotSentRequestAfterDeadline(deadline=deadline)):
                return Err(f"Невозможно отправить заявку на {on_date} после {deadline.isoformat()}")

        return Ok(submitting.unwrap())

    async def attach_pupil_to_parent(self, parent_id: UUID, pupil_id: str) -> Result[None, str]:
        attaching = await attach_child_to_parent(
            parent_id=ParentID(parent_id),
            pupil_id=PupilID(pupil_id),
            parent_repository=self._parent_repository,
            pupil_repository=self._pupil_repository,
        )

        match attaching:
            case Err(NotFoundParent()):
                return Err(f"Не найден родитель с id={parent_id}")

            case Err(NotFoundPupil()):
                return Err(f"Не найден ученик с id={pupil_id}")

            case Err(PupilIsAlreadyAttached()):
                return Err("Ребёнок уже привязан к родителю")

        return Ok(attaching.unwrap())
