from datetime import date
from uuid import UUID

from sqlalchemy import ARRAY, Date, ForeignKey, ForeignKeyConstraint, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.db.base import DictMixin
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import NutritionStatus, Pupil, PupilID
from app.nutrition.domain.request import Declaration, Request, RequestStatus
from app.nutrition.domain.school_class import SchoolClass
from app.nutrition.domain.time import Period, Timeline
from app.shared.domain.school_class import ClassID


class NutritionBase(DeclarativeBase, DictMixin):
    metadata = MetaData(schema="nutrition")


class SchoolClassDB(NutritionBase):
    __tablename__ = "school_class"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    mealtimes: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))

    def __init__(self, id_: UUID, mealtimes: list[int]) -> None:
        super().__init__()

        self.id = id_
        self.mealtimes = mealtimes

    def to_model(self) -> SchoolClass:
        return SchoolClass(
            id=ClassID(self.id),
            mealtimes=set(Mealtime(mealtime) for mealtime in self.mealtimes),
        )

    @classmethod
    def from_model(cls, school_class: SchoolClass) -> "SchoolClassDB":
        return cls(
            id_=school_class.id.value,
            mealtimes=[mealtime.value for mealtime in school_class.mealtimes],
        )


class PupilDB(NutritionBase):
    __tablename__ = "pupil"

    id: Mapped[str] = mapped_column(primary_key=True)
    class_id: Mapped[UUID] = mapped_column(ForeignKey(SchoolClassDB.id))
    mealtimes: Mapped[list[int]] = mapped_column(ARRAY(Integer, dimensions=1))
    preferential_until: Mapped[date | None] = mapped_column()
    cancelled_periods: Mapped[list[tuple[date, date]]] = mapped_column(ARRAY(item_type=Date, dimensions=2))

    def __init__(
        self,
        id_: str,
        class_id: UUID,
        mealtimes: list[int],
        preferential_until: date | None,
        cancelled_periods: list[tuple[date, date]],
    ) -> None:
        super().__init__()

        self.id = id_
        self.class_id = class_id
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
            mealtimes={Mealtime(mealtime) for mealtime in self.mealtimes},
            preferential_until=self.preferential_until,
            cancelled_periods=cancelled_periods,
        )

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilDB":
        return cls(
            id_=pupil.id.value,
            class_id=pupil.class_id.value,
            mealtimes=[mealtime.value for mealtime in pupil.mealtimes],
            preferential_until=pupil.preferential_until,
            cancelled_periods=[(period.start, period.end) for period in pupil.cancelled_periods],
        )


class RequestDB(NutritionBase):
    __tablename__ = "request"

    class_id: Mapped[UUID] = mapped_column(ForeignKey(SchoolClassDB.id), primary_key=True)
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
        ForeignKeyConstraint([request_class_id, request_on_date], [RequestDB.class_id, RequestDB.on_date]),
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
