from dataclasses import dataclass

from app.nutrition.application.repositories import (
    IMenusRepository,
    IParentsRepository,
    IPupilsRepository,
    IRequestsRepository,
    ISchoolClassesRepository,
)
from app.shared.unit_of_work.abc import Context


@dataclass(frozen=True)
class NutritionContext(Context):
    pupils: IPupilsRepository
    parents: IParentsRepository
    menus: IMenusRepository
    school_classes: ISchoolClassesRepository
    requests: IRequestsRepository
