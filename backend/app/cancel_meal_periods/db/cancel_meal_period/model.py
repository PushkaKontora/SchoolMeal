from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.constants import CASCADE


class CancelMealPeriod(Base):
    __tablename__ = "cancel_meal_periods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(512), nullable=True)

    pupil = relationship("Pupil", back_populates="cancel_meal_periods", uselist=False, lazy="raise")
