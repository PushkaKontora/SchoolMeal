from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.constants import CASCADE


class Portion(Base):
    __tablename__ = "portions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id", ondelete=CASCADE), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(scale=2, asdecimal=True), nullable=False)
    components: Mapped[str] = mapped_column(String(256), nullable=True)
    weight: Mapped[float | None] = mapped_column(Numeric(scale=2), nullable=True)
    kcal: Mapped[float | None] = mapped_column(Numeric(scale=2), nullable=True)
    protein: Mapped[float | None] = mapped_column(Numeric(scale=2), nullable=True)
    fats: Mapped[float | None] = mapped_column(Numeric(scale=2), nullable=True)
    carbs: Mapped[float | None] = mapped_column(Numeric(scale=2), nullable=True)

    food = relationship("Food", lazy="raise")
