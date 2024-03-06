from datetime import date
from uuid import UUID

from sqlalchemy import ARRAY, Date, ForeignKey, Integer, MetaData, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.db.base import DictMixin
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.parent import Parent, ParentID
from app.nutrition.domain.personal_info import Email, FullName, Phone
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.request import Request, Status
from app.nutrition.domain.school import School, SchoolName
from app.nutrition.domain.school_class import ClassID, Literal, Number, SchoolClass
from app.nutrition.domain.teacher import Teacher, TeacherID
from app.nutrition.domain.times import Period, Timeline


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
    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    patronymic: Mapped[str | None] = mapped_column()

    def __init__(self, id_: UUID, last_name: str, first_name: str, patronymic: str | None) -> None:
        super().__init__()

        self.id = id_
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic

    def to_model(self) -> Teacher:
        return Teacher(
            id=TeacherID(self.id),
            name=FullName.create(last=self.last_name, first=self.first_name, patronymic=self.patronymic),
        )

    @classmethod
    def from_model(cls, teacher: Teacher) -> "TeacherDB":
        return cls(
            id_=teacher.id.value,
            last_name=teacher.name.last.value,
            first_name=teacher.name.first.value,
            patronymic=teacher.name.patronymic.value if teacher.name.patronymic else None,
        )


class SchoolClassDB(NutritionBase):
    __tablename__ = "school_class"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    teacher_id: Mapped[UUID] = mapped_column(ForeignKey(TeacherDB.id))
    number: Mapped[int] = mapped_column()
    literal: Mapped[str] = mapped_column(String(1))
    mealtimes: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))

    def __init__(self, id_: UUID, teacher_id: UUID, number: int, literal: str, mealtimes: list[int]) -> None:
        super().__init__()

        self.id = id_
        self.teacher_id = teacher_id
        self.number = number
        self.literal = literal
        self.mealtimes = mealtimes

    def to_model(self) -> SchoolClass:
        return SchoolClass(
            id=ClassID(self.id),
            teacher_id=TeacherID(self.teacher_id),
            number=Number(self.number),
            literal=Literal(self.literal),
            mealtimes=set(Mealtime(mealtime) for mealtime in self.mealtimes),
        )

    @classmethod
    def from_model(cls, school_class: SchoolClass) -> "SchoolClassDB":
        return cls(
            id_=school_class.id.value,
            teacher_id=school_class.teacher_id.value,
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
    cancellation: Mapped[list[tuple[date, date]]] = mapped_column(ARRAY(item_type=Date, dimensions=2))

    def __init__(
        self,
        id_: str,
        class_id: UUID,
        last_name: str,
        first_name: str,
        patronymic: str | None,
        mealtimes: list[int],
        preferential_until: date | None,
        cancellation: list[tuple[date, date]],
    ) -> None:
        super().__init__()

        self.id = id_
        self.class_id = class_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.mealtimes = mealtimes
        self.preferential_until = preferential_until
        self.cancellation = cancellation

    def to_model(self) -> Pupil:
        cancellation = Timeline()

        for period in self.cancellation:
            cancellation.insert(Period(start=period[0], end=period[1]))

        return Pupil(
            id=PupilID(self.id),
            class_id=ClassID(self.class_id),
            name=FullName.create(last=self.last_name, first=self.first_name, patronymic=self.patronymic),
            mealtimes={Mealtime(mealtime) for mealtime in self.mealtimes},
            preferential_until=self.preferential_until,
            cancellation=cancellation,
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
            cancellation=[(period.start, period.end) for period in pupil.cancellation],
        )


class RequestDB(NutritionBase):
    __tablename__ = "request"

    class_id: Mapped[UUID] = mapped_column(ForeignKey(SchoolClassDB.id), primary_key=True)
    on_date: Mapped[date] = mapped_column(primary_key=True)
    mealtimes: Mapped[dict[int, list[str]]] = mapped_column(JSONB)
    status: Mapped[int] = mapped_column()

    def __init__(self, class_id: UUID, on_date: date, mealtimes: dict[int, list[str]], status: int) -> None:
        super().__init__()

        self.class_id = class_id
        self.on_date = on_date
        self.mealtimes = mealtimes
        self.status = status

    def to_model(self) -> Request:
        return Request(
            class_id=ClassID(self.class_id),
            on_date=self.on_date,
            mealtimes={
                Mealtime(mealtime): {PupilID(id_) for id_ in pupil_ids}
                for mealtime, pupil_ids in self.mealtimes.items()
            },
            status=Status(self.status),
        )

    @classmethod
    def from_model(cls, request: Request) -> "RequestDB":
        return cls(
            class_id=request.class_id.value,
            on_date=request.on_date,
            mealtimes={
                mealtime.value: [id_.value for id_ in pupil_ids] for mealtime, pupil_ids in request.mealtimes.items()
            },
            status=request.status.value,
        )


class ParentDB(NutritionBase):
    __tablename__ = "parent"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    patronymic: Mapped[str | None] = mapped_column()
    email: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    children: Mapped[list[str]] = mapped_column(ARRAY(String, dimensions=1))

    def __init__(
        self,
        id_: UUID,
        last_name: str,
        first_name: str,
        patronymic: str | None,
        email: str,
        phone: str,
        children: list[str],
    ) -> None:
        super().__init__()

        self.id = id_
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.email = email
        self.phone = phone
        self.children = children

    def to_model(self) -> Parent:
        return Parent(
            id=ParentID(self.id),
            name=FullName.create(last=self.last_name, first=self.first_name, patronymic=self.patronymic),
            email=Email(self.email),
            phone=Phone(self.phone),
            children={PupilID(child_id) for child_id in self.children},
        )

    @classmethod
    def from_model(cls, parent: Parent) -> "ParentDB":
        return cls(
            id_=parent.id.value,
            last_name=parent.name.last.value,
            first_name=parent.name.first.value,
            patronymic=parent.name.patronymic.value if parent.name.patronymic else None,
            email=parent.email.value,
            phone=parent.phone.value,
            children=[child.value for child in parent.children],
        )
