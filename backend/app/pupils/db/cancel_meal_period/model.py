from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constants import CASCADE


class CancelMealPeriod(Base):
    __tablename__ = "cancel_meal_periods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(512), nullable=True)
