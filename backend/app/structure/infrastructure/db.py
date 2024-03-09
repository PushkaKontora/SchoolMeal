from uuid import UUID

from sqlalchemy import ForeignKey, MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.db.base import DictMixin
from app.shared.domain.personal_info import FullName
from app.shared.domain.pupil import PupilID
from app.structure.domain.parent import Parent, ParentID
from app.structure.domain.pupil import Pupil
from app.structure.domain.school import School, SchoolName
from app.structure.domain.school_class import ClassID, Literal, Number, SchoolClass
from app.structure.domain.teacher import Teacher, TeacherID


class StructureBase(DeclarativeBase, DictMixin):
    metadata = MetaData(schema="structure")


class SchoolDB(StructureBase):
    __tablename__ = "school"

    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    name: Mapped[str] = mapped_column()

    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = name

    def to_model(self) -> School:
        return School(name=SchoolName(self.name))

    @classmethod
    def from_model(cls, school: School) -> "SchoolDB":
        return cls(name=school.name.value)


class TeacherDB(StructureBase):
    __tablename__ = "teacher"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    def __init__(self, id_: UUID) -> None:
        super().__init__()

        self.id = id_

    def to_model(self) -> Teacher:
        return Teacher(id=TeacherID(self.id))

    @classmethod
    def from_model(cls, teacher: Teacher) -> "TeacherDB":
        return cls(id_=teacher.id.value)


class SchoolClassDB(StructureBase):
    __tablename__ = "school_class"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    teacher_id: Mapped[UUID] = mapped_column(ForeignKey(TeacherDB.id))
    number: Mapped[int] = mapped_column()
    literal: Mapped[str] = mapped_column(String(1))

    def __init__(self, id_: UUID, teacher_id: UUID, number: int, literal: str) -> None:
        super().__init__()

        self.id = id_
        self.teacher_id = teacher_id
        self.number = number
        self.literal = literal

    def to_model(self) -> SchoolClass:
        return SchoolClass(
            id=ClassID(self.id),
            teacher_id=TeacherID(self.teacher_id),
            number=Number(self.number),
            literal=Literal(self.literal),
        )

    @classmethod
    def from_model(cls, school_class: SchoolClass) -> "SchoolClassDB":
        return cls(
            id_=school_class.id.value,
            teacher_id=school_class.teacher_id.value,
            number=school_class.number.value,
            literal=school_class.literal.value,
        )


class PupilDB(StructureBase):
    __tablename__ = "pupil"

    id: Mapped[str] = mapped_column(primary_key=True)
    class_id: Mapped[UUID] = mapped_column(ForeignKey(SchoolClassDB.id))
    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    patronymic: Mapped[str | None] = mapped_column()

    parents: Mapped[list["ParentDB"]] = relationship(
        secondary=lambda: PupilParentAssociation.__table__, lazy="selectin"
    )

    def __init__(self, id_: str, class_id: UUID, last_name: str, first_name: str, patronymic: str | None) -> None:
        super().__init__()

        self.id = id_
        self.class_id = class_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic

    def to_model(self) -> Pupil:
        return Pupil(
            id=PupilID(self.id),
            class_id=ClassID(self.class_id),
            name=FullName.create(last=self.last_name, first=self.first_name, patronymic=self.patronymic),
            parent_ids={ParentID(parent.id) for parent in self.parents},
        )

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilDB":
        return cls(
            id_=pupil.id.value,
            class_id=pupil.class_id.value,
            last_name=pupil.name.last.value,
            first_name=pupil.name.first.value,
            patronymic=pupil.name.patronymic.value if pupil.name.patronymic else None,
        )


class ParentDB(StructureBase):
    __tablename__ = "parent"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    def __init__(self, id_: UUID) -> None:
        super().__init__()

        self.id = id_

    def to_model(self) -> Parent:
        return Parent(id=ParentID(self.id))

    @classmethod
    def from_model(cls, parent: Parent) -> "ParentDB":
        return cls(id_=parent.id.value)


class PupilParentAssociation(StructureBase):
    __tablename__ = "pupil_parent"

    pupil_id: Mapped[str] = mapped_column(ForeignKey(PupilDB.id), primary_key=True)
    parent_id: Mapped[UUID] = mapped_column(ForeignKey(ParentDB.id), primary_key=True)

    def __init__(self, pupil_id: str, parent_id: UUID) -> None:
        super().__init__()

        self.pupil_id = pupil_id
        self.parent_id = parent_id

    @classmethod
    def from_model(cls, pupil: Pupil) -> list["PupilParentAssociation"]:
        return [cls(pupil_id=pupil.id.value, parent_id=parent_id.value) for parent_id in pupil.parent_ids]
