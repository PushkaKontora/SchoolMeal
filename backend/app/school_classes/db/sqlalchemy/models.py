from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.sqlalchemy import CASCADE, Base


class SchoolClass(Base):
    __tablename__ = "school_classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete=CASCADE), nullable=False)
    number = Column(Integer, nullable=False)
    letter = Column(String(1), nullable=False)
    has_breakfast = Column(Boolean, nullable=False)
    has_lunch = Column(Boolean, nullable=False)
    has_dinner = Column(Boolean, nullable=False)

    pupils = relationship("Pupil", secondary="pupils_classes", back_populates="school_class")
    teachers = relationship("User", secondary="teachers")

    __table_args__ = (UniqueConstraint("school_id", "number", "letter", name="unique_classes_in_school"),)


class PupilClass(Base):
    __tablename__ = "pupils_classes"

    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete=CASCADE), primary_key=True)
    pupil_id = Column(String, ForeignKey("pupils.id", ondelete=CASCADE), primary_key=True, unique=True)


class Teacher(Base):
    __tablename__ = "teachers"

    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete=CASCADE), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete=CASCADE), primary_key=True)
