from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.sqlalchemy.base import CASCADE, Base


class SchoolClass(Base):
    __tablename__ = "school_classes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id", ondelete=CASCADE), nullable=False)
    number: Mapped[int] = mapped_column(nullable=False)
    letter: Mapped[str] = mapped_column(String(1), nullable=False)
    has_breakfast: Mapped[bool] = mapped_column(nullable=False)
    has_lunch: Mapped[bool] = mapped_column(nullable=False)
    has_dinner: Mapped[bool] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint("school_id", "number", "letter", name="unique_classes_in_school"),)


class PupilClass(Base):
    __tablename__ = "pupils_classes"

    class_id: Mapped[int] = mapped_column(ForeignKey("school_classes.id", ondelete=CASCADE), primary_key=True)
    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), primary_key=True, unique=True)


class Teacher(Base):
    __tablename__ = "teachers"

    class_id: Mapped[int] = mapped_column(ForeignKey("school_classes.id", ondelete=CASCADE), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), primary_key=True)
