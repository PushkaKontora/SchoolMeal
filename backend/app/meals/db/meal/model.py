from datetime import date

from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.constants import CASCADE


class Meal(Base):
    __tablename__ = "meals"
    __table_args__ = (UniqueConstraint("class_id", "date", name="unique_class_meal_per_day"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("school_classes.id", ondelete=CASCADE), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    menus = relationship("Menu", lazy="raise")
    school_class = relationship("SchoolClass", uselist=False, lazy="raise")
