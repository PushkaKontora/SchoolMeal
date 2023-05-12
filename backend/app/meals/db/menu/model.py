import enum

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.constants import CASCADE


class MealType(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"


class Menu(Base):
    __tablename__ = "menu"

    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id", ondelete=CASCADE), primary_key=True)
    portion_id: Mapped[int] = mapped_column(ForeignKey("portions.id", ondelete=CASCADE), primary_key=True)
    meal_type: Mapped[MealType] = mapped_column(Enum(MealType), nullable=False, primary_key=True)

    portion = relationship("Portion")
