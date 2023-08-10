from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.legacy.db.base import Base
from app.legacy.db.constants import CASCADE


class MealRequest(Base):
    __tablename__ = "meal_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), nullable=False)

    declared_pupils = relationship("DeclaredPupil", back_populates="meal_request")
    meal = relationship("Meal", back_populates="request")
