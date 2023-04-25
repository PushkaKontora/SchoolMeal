from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constants import CASCADE


class DeclaredPupils(Base):
    __tablename__ = "declared_pupils"

    request_id: Mapped[int] = mapped_column(ForeignKey("meal_requests.id", ondelete=CASCADE), primary_key=True)
    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), primary_key=True)
    breakfast: Mapped[bool] = mapped_column(nullable=False)
    lunch: Mapped[bool] = mapped_column(nullable=False)
    dinner: Mapped[bool] = mapped_column(nullable=False)
    preferential: Mapped[bool] = mapped_column(nullable=False)
