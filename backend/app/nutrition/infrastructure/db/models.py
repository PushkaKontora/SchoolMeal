from datetime import date, datetime
from uuid import UUID

from sqlalchemy import ARRAY, Date, DateTime, ForeignKey, Integer, MetaData, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.db.base import DictMixin
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.request import Request
from app.nutrition.domain.school import School, SchoolName
from app.nutrition.domain.school_class import ClassID, Literal, Number, SchoolClass, TeacherID
from app.nutrition.domain.times import Period, Timeline


class NutritionBase(DeclarativeBase, DictMixin):
    metadata = MetaData(schema="nutrition")


class SchoolDB(NutritionBase):
    __tablename__ = "school"

    name: Mapped[str] = mapped_column(primary_key=True)

    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = name

    def to_model(self) -> School:
        return School(name=SchoolName(self.name))


class SchoolClassDB(NutritionBase):
    __tablename__ = "school_class"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    teacher_id: Mapped[UUID | None] = mapped_column()
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
            teacher_id=school_class.teacher_id,
            number=school_class.number.value,
            literal=school_class.literal.value,
            mealtimes=[mealtime.value for mealtime in school_class.mealtimes],
        )


class PupilDB(NutritionBase):
    __tablename__ = "pupil"

    id: Mapped[str] = mapped_column(primary_key=True)
    class_id: Mapped[UUID] = mapped_column(ForeignKey(SchoolClassDB.id))
    mealtimes: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))
    preferential_until: Mapped[date | None] = mapped_column()
    cancellation: Mapped[list[tuple[date, date]]] = mapped_column(ARRAY(item_type=Date, dimensions=2))

    def __init__(
        self,
        id_: str,
        class_id: UUID,
        mealtimes: list[int],
        preferential_until: date | None,
        cancellation: list[tuple[date, date]],
    ) -> None:
        super().__init__()

        self.id = id_
        self.class_id = class_id
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
            mealtimes={Mealtime(mealtime) for mealtime in self.mealtimes},
            preferential_until=self.preferential_until,
            cancellation=cancellation,
        )

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilDB":
        return cls(
            id_=pupil.id.value,
            class_id=pupil.class_id.value,
            mealtimes=[mealtime.value for mealtime in pupil.mealtimes],
            preferential_until=pupil.preferential_until,
            cancellation=[(period.start, period.end) for period in pupil.cancellation],
        )


class RequestDB(NutritionBase):
    __tablename__ = "request"

    class_id: Mapped[UUID] = mapped_column(ForeignKey(SchoolClassDB.id), primary_key=True)
    on_date: Mapped[date] = mapped_column()
    mealtimes: Mapped[dict[int, list[str]]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __init__(self, class_id: UUID, on_date: date, mealtimes: dict[int, list[str]], created_at: datetime) -> None:
        super().__init__()

        self.class_id = class_id
        self.on_date = on_date
        self.mealtimes = mealtimes
        self.created_at = created_at

    def to_model(self) -> Request:
        return Request(
            class_id=ClassID(self.class_id),
            on_date=self.on_date,
            mealtimes={
                Mealtime(mealtime): {PupilID(id_) for id_ in pupil_ids}
                for mealtime, pupil_ids in self.mealtimes.items()
            },
            created_at=self.created_at,
        )

    @classmethod
    def from_model(cls, request: Request) -> "RequestDB":
        return cls(
            class_id=request.class_id.value,
            on_date=request.on_date,
            mealtimes={
                mealtime.value: [id_.value for id_ in pupil_ids] for mealtime, pupil_ids in request.mealtimes.items()
            },
            created_at=request.created_at,
        )
