from app.base_entity import BaseEntity


class FoodOut(BaseEntity):
    id: int
    school_id: int
    name: str
    photo_path: str | None


class PortionOut(BaseEntity):
    id: int
    food: FoodOut
    components: str | None
    weight: float | None
    kcal: float | None
    protein: float | None
    fats: float | None
    carbs: float | None
