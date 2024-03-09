from collections import defaultdict
from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.api import dto as nutrition_dto
from app.nutrition.api.dto import MealtimeDTO, RequestStatusDTO
from app.structure.api import dto as structure_dto


class PrefilledPupilOut(BaseModel):
    id: str
    last_name: str
    first_name: str
    patronymic: str | None
    mealtimes: list[MealtimeDTO]


class PrefilledRequestOut(BaseModel):
    class_id: UUID
    on_date: date
    is_submitted: bool
    can_be_resubmitted: bool
    mealtimes: list[MealtimeDTO]
    pupils: list[PrefilledPupilOut]

    @classmethod
    def create(cls, request: nutrition_dto.RequestOut, pupils: list[structure_dto.PupilOut]) -> "PrefilledRequestOut":
        pupil_by_id = {pupil.id: pupil for pupil in pupils}
        pupil_mealtimes: defaultdict[str, set[MealtimeDTO]] = defaultdict(set)

        for mealtime, pupil_ids in request.mealtimes.items():
            for pupil_id in pupil_ids:
                if pupil_id not in pupil_by_id:
                    continue

                pupil_mealtimes[pupil_id].add(mealtime)

        pupils_out: list[PrefilledPupilOut] = []
        for pupil_id, mealtimes in pupil_mealtimes.items():
            info = pupil_by_id[pupil_id]
            pupils_out.append(
                PrefilledPupilOut(
                    id=info.id,
                    last_name=info.name.last,
                    first_name=info.name.first,
                    patronymic=info.name.patronymic,
                    mealtimes=list(mealtimes),
                )
            )

        return cls(
            class_id=request.class_id,
            on_date=request.on_date,
            is_submitted=request.status is RequestStatusDTO.SUBMITTED,
            can_be_resubmitted=request.can_be_resubmitted,
            mealtimes=list(request.mealtimes.keys()),
            pupils=pupils_out,
        )
