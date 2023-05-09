import enum

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constants import CASCADE


class MealType(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"


class Menu(Base):
    __tablename__ = "menu"

    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id", ondelete=CASCADE), primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id", ondelete=CASCADE), primary_key=True)
    meal_type: Mapped[MealType] = mapped_column(Enum(MealType), nullable=False)
