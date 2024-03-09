from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.api import dto as nutrition_dto
from app.nutrition.api.dto import MealtimeDTO, PeriodOut, RequestStatusDTO
from app.structure.api import dto as structure_dto


class PrefilledPupilOut(BaseModel):
    pupil_id: str
    last_name: str
    first_name: str
    patronymic: str | None
    mealtimes: list[MealtimeDTO]
    is_cancelled: bool


class PrefilledRequestOut(BaseModel):
    class_id: UUID
    on_date: date
    is_submitted: bool
    can_be_resubmitted: bool
    mealtimes: list[MealtimeDTO]
    pupils: list[PrefilledPupilOut]

    @classmethod
    def create(
        cls,
        request: nutrition_dto.RequestOut,
        pupils: list[structure_dto.PupilOut],
        nutrition_pupils: list[nutrition_dto.PupilOut],
    ) -> "PrefilledRequestOut":
        pupil_by_id = {pupil.id: pupil for pupil in pupils}
        cancelled_periods_by_id = {pupil.id: pupil.cancelled_periods for pupil in nutrition_pupils}

        prefilled_pupils: list[PrefilledPupilOut] = []
        for declaration in request.declarations:
            if not (info := pupil_by_id.get(declaration.pupil_id)):
                continue

            prefilled_pupils.append(
                PrefilledPupilOut(
                    pupil_id=info.id,
                    last_name=info.name.last,
                    first_name=info.name.first,
                    patronymic=info.name.patronymic,
                    mealtimes=list(declaration.mealtimes),
                    is_cancelled=cls._is_day_included_in_cancelled_periods(
                        day=request.on_date, periods=cancelled_periods_by_id[info.id]
                    )
                    if info.id in cancelled_periods_by_id
                    else False,
                )
            )

        return cls(
            class_id=request.class_id,
            on_date=request.on_date,
            is_submitted=request.status is RequestStatusDTO.SUBMITTED,
            can_be_resubmitted=request.can_be_resubmitted,
            mealtimes=list(request.mealtimes),
            pupils=prefilled_pupils,
        )

    @classmethod
    def _is_day_included_in_cancelled_periods(cls, day: date, periods: list[PeriodOut]) -> bool:
        if not periods:
            return False

        left, right = 0, len(periods)

        while left < right:
            mid = (left + right) // 2
            current = periods[mid]

            if current.start <= day <= current.end:
                return True

            left, right = (mid + 1, right) if day > current.end else (left, mid)

        return False
