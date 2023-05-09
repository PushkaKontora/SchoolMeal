from datetime import date

from sqlalchemy import Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constants import CASCADE


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("school_classes.id", ondelete=CASCADE), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    breakfast_price: Mapped[float] = mapped_column(Float(precision=2, asdecimal=True), nullable=False)
    lunch_price: Mapped[float] = mapped_column(Float(precision=2, asdecimal=True), nullable=False)
    dinner_price: Mapped[float] = mapped_column(Float(precision=2, asdecimal=True), nullable=False)

    __table_args__ = (UniqueConstraint("class_id", "date", name="unique_class_meal_per_day"),)
