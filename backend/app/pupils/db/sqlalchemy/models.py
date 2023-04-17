from datetime import datetime

from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.sqlalchemy.base import CASCADE, Base


class Pupil(Base):
    __tablename__ = "pupils"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    certificate_before_date: Mapped[datetime] = mapped_column(nullable=True)
    balance: Mapped[float] = mapped_column(Float(precision=2, asdecimal=True), nullable=False)
    breakfast: Mapped[bool] = mapped_column(default=False, nullable=False)
    lunch: Mapped[bool] = mapped_column(default=False, nullable=False)
    dinner: Mapped[bool] = mapped_column(default=False, nullable=False)


class CancelMealPeriod(Base):
    __tablename__ = "cancel_meal_periods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), nullable=False)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(512), nullable=True)


class Child(Base):
    __tablename__ = "children"

    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), primary_key=True)
