from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constants import CASCADE


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id", ondelete=CASCADE), nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    photo_path: Mapped[str] = mapped_column(String(128), nullable=False)
    components: Mapped[str] = mapped_column(String(256), nullable=False)
    weight: Mapped[float | None] = mapped_column(Float(precision=2), nullable=True)
    kcal: Mapped[float | None] = mapped_column(Float(precision=2), nullable=True)
    protein: Mapped[float | None] = mapped_column(Float(precision=2), nullable=True)
    fats: Mapped[float | None] = mapped_column(Float(precision=2), nullable=True)
    carbs: Mapped[float | None] = mapped_column(Float(precision=2), nullable=True)
