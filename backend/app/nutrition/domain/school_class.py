from dataclasses import dataclass

from app.nutrition.domain.mealtime import Mealtime
from app.shared.domain.school_class import ClassID


@dataclass
class SchoolClass:
    id: ClassID
    mealtimes: set[Mealtime]
