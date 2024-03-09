from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.api import dto as nutrition_dto
from app.nutrition.api.dto import MealtimeDTO, RequestStatusDTO
from app.structure.api import dto as structure_dto


class DeclarationOut(BaseModel):
    pupil_id: str
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
    declarations: list[DeclarationOut]

    @classmethod
    def create(cls, request: nutrition_dto.RequestOut, pupils: list[structure_dto.PupilOut]) -> "PrefilledRequestOut":
        pupil_by_id = {pupil.id: pupil for pupil in pupils}

        declarations: list[DeclarationOut] = []
        for declaration in request.declarations:
            if not (info := pupil_by_id.get(declaration.pupil_id)):
                continue

            declarations.append(
                DeclarationOut(
                    pupil_id=info.id,
                    last_name=info.name.last,
                    first_name=info.name.first,
                    patronymic=info.name.patronymic,
                    mealtimes=list(declaration.mealtimes),
                )
            )

        return cls(
            class_id=request.class_id,
            on_date=request.on_date,
            is_submitted=request.status is RequestStatusDTO.SUBMITTED,
            can_be_resubmitted=request.can_be_resubmitted,
            mealtimes=list(request.mealtimes),
            declarations=declarations,
        )
