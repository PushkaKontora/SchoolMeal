from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.sqlalchemy.base import CASCADE, Base


class Pupil(Base):
    __tablename__ = "pupils"

    id = Column(String(20), primary_key=True)
    last_name = Column(String(32), nullable=False)
    first_name = Column(String(32), nullable=False)
    certificate_before_date = Column(DateTime, nullable=True)
    balance = Column(Float(precision=2, asdecimal=True), nullable=False)
    breakfast = Column(Boolean, default=False, nullable=False)
    lunch = Column(Boolean, default=False, nullable=False)
    dinner = Column(Boolean, default=False, nullable=False)

    cancel_meal_periods = relationship("CancelMealPeriod", backref="pupil")
    school_class = relationship("SchoolClass", secondary="pupils_classes", back_populates="pupils", uselist=False)
    parents = relationship("User", secondary="children", back_populates="children")


class CancelMealPeriod(Base):
    __tablename__ = "cancel_meal_periods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pupil_id = Column(String, ForeignKey("pupils.id", ondelete=CASCADE), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    comment = Column(String(512), nullable=True)


class Child(Base):
    __tablename__ = "children"

    pupil_id = Column(String, ForeignKey("pupils.id", ondelete=CASCADE), primary_key=True)
    parent_id = Column(Integer, ForeignKey("users.id", ondelete=CASCADE), primary_key=True)
