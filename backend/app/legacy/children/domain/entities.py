from app.legacy.utils.entity import Entity


class ChildIn(Entity):
    child_id: str


class PlanIn(Entity):
    breakfast: bool | None = None
    lunch: bool | None = None
    dinner: bool | None = None


class PlanOut(Entity):
    breakfast: bool
    lunch: bool
    dinner: bool
