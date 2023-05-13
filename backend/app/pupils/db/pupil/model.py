from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.constants import SET_NULL


class Pupil(Base):
    __tablename__ = "pupils"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    class_id: Mapped[int | None] = mapped_column(ForeignKey("school_classes.id", ondelete=SET_NULL), nullable=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    certificate_before_date: Mapped[datetime | None] = mapped_column(nullable=True)
    balance: Mapped[float] = mapped_column(Numeric(scale=2), nullable=False)
    breakfast: Mapped[bool] = mapped_column(default=False, nullable=False)
    lunch: Mapped[bool] = mapped_column(default=False, nullable=False)
    dinner: Mapped[bool] = mapped_column(default=False, nullable=False)

    school_class = relationship("SchoolClass", lazy="raise")
    cancel_meal_periods = relationship("CancelMealPeriod", back_populates="pupil", lazy="raise")
