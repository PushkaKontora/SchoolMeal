from typing import Any
from uuid import UUID

from sqlalchemy import ARRAY, JSON, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from sqlalchemy.orm import Mapped, relationship

from app.children.domain.child import Child, ChildID, FirstName, LastName
from app.children.domain.meal_plan import MealPlan
from app.children.domain.parent import Parent
from app.children.domain.school import School, SchoolName
from app.children.domain.school_class import ClassLiteral, ClassNumber, SchoolClass
from app.shared.db.base import Base


class ChildrenSchemaMixin:
    __table_args__ = {"schema": "children"}


class SchoolDB(Base, ChildrenSchemaMixin):
    __tablename__ = "school"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)

    def to_model(self) -> School:
        return School(
            id=self.id,
            name=SchoolName(self.name),
        )


class SchoolClassDB(Base, ChildrenSchemaMixin):
    __tablename__ = "school_class"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    school_id: Mapped[UUID] = Column(ForeignKey(SchoolDB.id), nullable=False)
    number: Mapped[int] = Column(Integer, nullable=False)
    literal: Mapped[str] = Column(String(length=1), nullable=False)

    school: Mapped[SchoolDB] = relationship(SchoolDB, uselist=False, viewonly=True, lazy="joined")

    def to_model(self) -> SchoolClass:
        return SchoolClass(
            id=self.id,
            school=self.school.to_model(),
            number=ClassNumber(self.number),
            literal=ClassLiteral(self.literal),
        )


class ChildDB(Base, ChildrenSchemaMixin):
    __tablename__ = "child"

    id: Mapped[str] = Column(String, primary_key=True)
    last_name: Mapped[str] = Column(String, nullable=False)
    first_name: Mapped[str] = Column(String, nullable=False)
    school_class_id: Mapped[UUID] = Column(ForeignKey(SchoolClassDB.id), nullable=False)
    meal_plan: Mapped[dict[str, Any]] = Column(JSON, nullable=False)

    school_class: Mapped[SchoolClassDB] = relationship(SchoolClassDB, uselist=False, viewonly=True, lazy="joined")

    def to_model(self) -> Child:
        return Child(
            id=ChildID(self.id),
            last_name=LastName(self.last_name),
            first_name=FirstName(self.first_name),
            school_class=self.school_class.to_model(),
            meal_plan=MealPlan(**self.meal_plan),
        )


class ParentDB(Base, ChildrenSchemaMixin):
    __tablename__ = "parent"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    child_ids: Mapped[list[str]] = Column(ARRAY(String, dimensions=1), nullable=False)  # type: ignore

    def to_model(self) -> "Parent":
        return Parent(id=self.id, child_ids=set(ChildID(child_id) for child_id in self.child_ids))

    @classmethod
    def from_model(cls, parent: Parent) -> "ParentDB":
        return cls(
            id=parent.id,
            child_ids=list(child_id.value for child_id in parent.child_ids),
        )
