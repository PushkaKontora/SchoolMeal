from app.utils.entity import Entity


class FoodOut(Entity):
    id: int
    school_id: int
    name: str
    photo_path: str | None


class PortionOut(Entity):
    id: int
    food: FoodOut
    components: str | None
    weight: float | None
    kcal: float | None
    protein: float | None
    fats: float | None
    carbs: float | None
