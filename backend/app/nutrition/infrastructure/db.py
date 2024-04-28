from datetime import date
from uuid import UUID

from sqlalchemy import ARRAY, Date, ForeignKey, ForeignKeyConstraint, Integer, MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.db.base import DictMixin
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.parent import Parent, ParentID
from app.nutrition.domain.pupil import NutritionStatus, Pupil, PupilID
from app.nutrition.domain.request import Declaration, Request, RequestStatus
from app.nutrition.domain.school import School, SchoolName
from app.nutrition.domain.school_class import ClassID, Literal, Number, SchoolClass
from app.nutrition.domain.teacher import Teacher, TeacherID
from app.nutrition.domain.time import Period, Timeline
from app.shared.domain.personal_info import FullName


class NutritionBase(DeclarativeBase, DictMixin):
    metadata = MetaData(schema="nutrition")


class SchoolDB(NutritionBase):
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


class TeacherDB(NutritionBase):
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


class ParentDB(NutritionBase):
    __tablename__ = "parent"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    def __init__(self, id_: UUID) -> None:
        super().__init__()

        self.id = id_

    def to_model(self) -> Parent:
        return Parent(id=ParentID(self.id))

    @classmethod
    def from_model(cls, teacher: Parent) -> "ParentDB":
        return cls(id_=teacher.id.value)


class SchoolClassDB(NutritionBase):
    __tablename__ = "school_class"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    teacher_id: Mapped[UUID | None] = mapped_column(ForeignKey(TeacherDB.id, ondelete="SET NULL"))
    number: Mapped[int] = mapped_column()
    literal: Mapped[str] = mapped_column(String(1))
    mealtimes: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))

    def __init__(self, id_: UUID, teacher_id: UUID | None, number: int, literal: str, mealtimes: list[int]) -> None:
        super().__init__()

        self.id = id_
        self.teacher_id = teacher_id
        self.number = number
        self.literal = literal
        self.mealtimes = mealtimes

    def to_model(self) -> SchoolClass:
        return SchoolClass(
            id=ClassID(self.id),
            teacher_id=TeacherID(self.teacher_id) if self.teacher_id else None,
            number=Number(self.number),
            literal=Literal(self.literal),
            mealtimes=set(Mealtime(mealtime) for mealtime in self.mealtimes),
        )

    @classmethod
    def from_model(cls, school_class: SchoolClass) -> "SchoolClassDB":
        return cls(
            id_=school_class.id.value,
            teacher_id=school_class.teacher_id.value if school_class.teacher_id else None,
            number=school_class.number.value,
            literal=school_class.literal.value,
            mealtimes=[mealtime.value for mealtime in school_class.mealtimes],
        )


class PupilDB(NutritionBase):
    __tablename__ = "pupil"

    id: Mapped[str] = mapped_column(primary_key=True)
    class_id: Mapped[UUID] = mapped_column(ForeignKey(SchoolClassDB.id))
    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    patronymic: Mapped[str | None] = mapped_column()
    mealtimes: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))
    preferential_until: Mapped[date | None] = mapped_column()
    cancelled_periods: Mapped[list[tuple[date, date]]] = mapped_column(ARRAY(item_type=Date, dimensions=2))

    parents: Mapped[list[ParentDB]] = relationship(
        secondary=lambda: PupilParentAssociation.__table__, uselist=True, lazy="selectin"
    )

    def __init__(
        self,
        id_: str,
        class_id: UUID,
        last_name: str,
        first_name: str,
        patronymic: str | None,
        mealtimes: list[int],
        preferential_until: date | None,
        cancelled_periods: list[tuple[date, date]],
    ) -> None:
        super().__init__()

        self.id = id_
        self.class_id = class_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.mealtimes = mealtimes
        self.preferential_until = preferential_until
        self.cancelled_periods = cancelled_periods

    def to_model(self) -> Pupil:
        cancelled_periods = Timeline()

        for period in self.cancelled_periods:
            cancelled_periods.insert(Period(start=period[0], end=period[1]))

        return Pupil(
            id=PupilID(self.id),
            class_id=ClassID(self.class_id),
            parent_ids={ParentID(parent.id) for parent in self.parents},
            name=FullName.create(last=self.last_name, first=self.first_name, patronymic=self.patronymic),
            mealtimes={Mealtime(mealtime) for mealtime in self.mealtimes},
            preferential_until=self.preferential_until,
            cancelled_periods=cancelled_periods,
        )

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilDB":
        return cls(
            id_=pupil.id.value,
            class_id=pupil.class_id.value,
            last_name=pupil.name.last.value,
            first_name=pupil.name.first.value,
            patronymic=pupil.name.patronymic.value if pupil.name.patronymic else None,
            mealtimes=[mealtime.value for mealtime in pupil.mealtimes],
            preferential_until=pupil.preferential_until,
            cancelled_periods=[(period.start, period.end) for period in pupil.cancelled_periods],
        )


class PupilParentAssociation(NutritionBase):
    __tablename__ = "pupil_parent"

    pupil_id: Mapped[str] = mapped_column(ForeignKey(PupilDB.id, ondelete="CASCADE"), primary_key=True)
    parent_id: Mapped[UUID] = mapped_column(ForeignKey(ParentDB.id, ondelete="CASCADE"), primary_key=True)

    def __init__(self, pupil_id: str, parent_id: UUID) -> None:
        super().__init__()

        self.pupil_id = pupil_id
        self.parent_id = parent_id


class RequestDB(NutritionBase):
    __tablename__ = "request"

    class_id: Mapped[UUID] = mapped_column(ForeignKey(SchoolClassDB.id, ondelete="CASCADE"), primary_key=True)
    on_date: Mapped[date] = mapped_column(primary_key=True)
    mealtimes: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))
    status: Mapped[int] = mapped_column()

    declarations: Mapped[list["DeclarationDB"]] = relationship(lazy="selectin")

    def __init__(
        self, class_id: UUID, on_date: date, mealtimes: list[int], status: int, declarations: list["DeclarationDB"]
    ) -> None:
        super().__init__()

        self.class_id = class_id
        self.on_date = on_date
        self.mealtimes = mealtimes
        self.status = status
        self.declarations = declarations

    def to_model(self) -> Request:
        return Request(
            class_id=ClassID(self.class_id),
            on_date=self.on_date,
            mealtimes={Mealtime(mealtime) for mealtime in self.mealtimes},
            declarations={declaration.to_model() for declaration in self.declarations},
            status=RequestStatus(self.status),
        )

    @classmethod
    def from_model(cls, request: Request) -> "RequestDB":
        return cls(
            class_id=request.class_id.value,
            on_date=request.on_date,
            mealtimes=[mealtime.value for mealtime in request.mealtimes],
            declarations=[DeclarationDB.from_model(request, declaration) for declaration in request.declarations],
            status=request.status.value,
        )


class DeclarationDB(NutritionBase):
    __tablename__ = "declaration"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pupil_id: Mapped[str] = mapped_column(ForeignKey(PupilDB.id))
    mealtimes: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))
    nutrition: Mapped[int] = mapped_column()

    request_class_id: Mapped[UUID] = mapped_column()
    request_on_date: Mapped[date] = mapped_column()

    __table_args__ = (
        ForeignKeyConstraint(
            [request_class_id, request_on_date], [RequestDB.class_id, RequestDB.on_date], ondelete="CASCADE"
        ),
    )

    def __init__(
        self, request_class_id: UUID, request_on_date: date, pupil_id: str, mealtimes: list[int], nutrition: int
    ) -> None:
        super().__init__()

        self.request_class_id = request_class_id
        self.request_on_date = request_on_date
        self.pupil_id = pupil_id
        self.mealtimes = mealtimes
        self.nutrition = nutrition

    def to_model(self) -> Declaration:
        return Declaration(
            pupil_id=PupilID(self.pupil_id),
            mealtimes={Mealtime(mealtime) for mealtime in self.mealtimes},
            nutrition=NutritionStatus(self.nutrition),
        )

    @classmethod
    def from_model(cls, request: Request, declaration: Declaration) -> "DeclarationDB":
        return cls(
            pupil_id=declaration.pupil_id.value,
            mealtimes=[mealtime.value for mealtime in declaration.mealtimes],
            nutrition=declaration.nutrition.value,
            request_class_id=request.class_id.value,
            request_on_date=request.on_date,
        )
