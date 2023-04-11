from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.database.sqlalchemy import CASCADE, Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete=CASCADE), nullable=False)
    name = Column(String(32), nullable=False)
    photo_path = Column(String(128), nullable=False)
    components = Column(String(256), nullable=False)
    weight = Column(Float(precision=2), nullable=True)
    kcal = Column(Float(precision=2), nullable=True)
    protein = Column(Float(precision=2), nullable=True)
    fats = Column(Float(precision=2), nullable=True)
    carbs = Column(Float(precision=2), nullable=True)
