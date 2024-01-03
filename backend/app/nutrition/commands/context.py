from dataclasses import dataclass

from app.nutrition.commands.repositories import IParentsRepository, IPupilsRepository
from app.shared.unit_of_work.abc import Context


@dataclass(frozen=True)
class NutritionContext(Context):
    pupils: IPupilsRepository
    parents: IParentsRepository
