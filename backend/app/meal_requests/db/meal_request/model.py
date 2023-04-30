from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.database.base import Base
from app.database.constants import CASCADE


class MealRequest(Base):
    __tablename__ = "meal_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), nullable=False)
