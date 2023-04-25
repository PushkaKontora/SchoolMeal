from datetime import date, datetime

from _decimal import Decimal
from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.constants import CASCADE, SET_NULL


class Pupil(Base):
    __tablename__ = "pupils"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    class_id: Mapped[int | None] = mapped_column(ForeignKey("school_classes.id", ondelete=SET_NULL), nullable=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    certificate_before_date: Mapped[datetime | None] = mapped_column(nullable=True)
    balance: Mapped[Decimal] = mapped_column(Float(precision=2, asdecimal=True), nullable=False)
    breakfast: Mapped[bool] = mapped_column(default=False, nullable=False)
    lunch: Mapped[bool] = mapped_column(default=False, nullable=False)
    dinner: Mapped[bool] = mapped_column(default=False, nullable=False)

    school_class = relationship("SchoolClass")
    cancel_meal_periods = relationship("CancelMealPeriod")


class CancelMealPeriod(Base):
    __tablename__ = "cancel_meal_periods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(512), nullable=True)
