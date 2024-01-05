from datetime import date
from uuid import UUID

from pydantic import BaseModel, validator

from app.nutrition.application.context import NutritionContext
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.unit_of_work.abc import IUnitOfWork


class OverridenPupil(BaseModel):
    id: str
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool


class SubmitRequestCommand(Command):
    school_class_id: UUID
    date_on: date
    overriden_pupil: list[OverridenPupil] = []

    @validator("overriden_pupil")
    def validate_unique_overrides(cls, value: list[OverridenPupil]) -> list[OverridenPupil]:
        if len(set(pupil.id for pupil in value)) < len(value):
            raise ValueError("Неуникальный идентификаторы учеников")

        return value


class SubmitRequestCommandHandler(ICommandHandler[SubmitRequestCommand, None]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: SubmitRequestCommand) -> None:
        pass
