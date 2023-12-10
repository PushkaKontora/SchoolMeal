from pydantic.dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class MealPlan:
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool

    @property
    def is_feeding(self) -> bool:
        return any([self.has_breakfast, self.has_dinner, self.has_snacks])
