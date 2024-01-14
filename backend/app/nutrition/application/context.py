from dataclasses import dataclass

from app.nutrition.application.repositories import (
    IDraftRequestsRepository,
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
    draft_requests: IDraftRequestsRepository
    requests: IRequestsRepository
