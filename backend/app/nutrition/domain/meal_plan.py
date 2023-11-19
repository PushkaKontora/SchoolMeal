from pydantic.dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class MealPlan:
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool

    def as_tuple(self) -> tuple[bool, bool, bool]:
        return self.has_breakfast, self.has_dinner, self.has_snacks
