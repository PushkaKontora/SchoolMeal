from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.sqlalchemy.base import CASCADE, Base
from app.meals.db.models import MealType


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete=CASCADE), nullable=False)
    date = Column(Date, nullable=False)
    breakfast_price = Column(Float(precision=2, asdecimal=True), nullable=False)
    lunch_price = Column(Float(precision=2, asdecimal=True), nullable=False)
    dinner_price = Column(Float(precision=2, asdecimal=True), nullable=False)

    menu = relationship("Menu")

    __table_args__ = (UniqueConstraint("class_id", "date", name="unique_class_meal_per_day"),)


class Menu(Base):
    __tablename__ = "menu"

    meal_id = Column(Integer, ForeignKey("meals.id", ondelete=CASCADE), primary_key=True)
    food_id = Column(Integer, ForeignKey("foods.id", ondelete=CASCADE), primary_key=True)
    meal_type = Column(Enum(MealType), nullable=False)
