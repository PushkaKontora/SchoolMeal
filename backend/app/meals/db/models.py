import enum
from datetime import datetime

from sqlalchemy import Date, Enum, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constants import CASCADE


class MealType(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("school_classes.id", ondelete=CASCADE), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    breakfast_price: Mapped[float] = mapped_column(Float(precision=2, asdecimal=True), nullable=False)
    lunch_price: Mapped[float] = mapped_column(Float(precision=2, asdecimal=True), nullable=False)
    dinner_price: Mapped[float] = mapped_column(Float(precision=2, asdecimal=True), nullable=False)

    __table_args__ = (UniqueConstraint("class_id", "date", name="unique_class_meal_per_day"),)


class Menu(Base):
    __tablename__ = "menu"

    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id", ondelete=CASCADE), primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id", ondelete=CASCADE), primary_key=True)
    meal_type: Mapped[MealType] = mapped_column(Enum(MealType), nullable=False)
