from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.database.sqlalchemy.base import CASCADE, Base


class MealRequest(Base):
    __tablename__ = "meal_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), nullable=False)


class DeclaredPupils(Base):
    __tablename__ = "declared_pupils"

    request_id: Mapped[int] = mapped_column(ForeignKey("meal_requests.id", ondelete=CASCADE), primary_key=True)
    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), primary_key=True)
    breakfast: Mapped[bool] = mapped_column(nullable=False)
    lunch: Mapped[bool] = mapped_column(nullable=False)
    dinner: Mapped[bool] = mapped_column(nullable=False)
    preferential: Mapped[bool] = mapped_column(nullable=False)
