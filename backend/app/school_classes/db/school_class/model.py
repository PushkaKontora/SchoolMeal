from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.constants import CASCADE


class SchoolClass(Base):
    __tablename__ = "school_classes"
    __table_args__ = (UniqueConstraint("school_id", "number", "letter", name="unique_classes_in_school"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id", ondelete=CASCADE), nullable=False)
    number: Mapped[int] = mapped_column(nullable=False)
    letter: Mapped[str] = mapped_column(String(1), nullable=False)
    has_breakfast: Mapped[bool] = mapped_column(nullable=False)
    has_lunch: Mapped[bool] = mapped_column(nullable=False)
    has_dinner: Mapped[bool] = mapped_column(nullable=False)

    teachers = relationship("User", secondary="teachers")
    pupils = relationship("Pupil", back_populates="school_class")
    school = relationship("School", uselist=False)
