from pydantic.dataclasses import dataclass

from app.shared.domain import ValueObject


@dataclass(eq=True, frozen=True)
class MealPlan(ValueObject):
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool

    @property
    def is_feeding(self) -> bool:
        return any([self.has_breakfast, self.has_dinner, self.has_snacks])
