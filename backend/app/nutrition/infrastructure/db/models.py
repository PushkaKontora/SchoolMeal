from datetime import date
from uuid import UUID

from sqlalchemy import ARRAY, Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from sqlalchemy.orm import Mapped, declarative_base, relationship

from app.nutrition.domain.parent import Parent
from app.nutrition.domain.periods import CancellationPeriod, CancellationPeriodSequence, Reason
from app.nutrition.domain.pupil import Name, PreferentialCertificate, Pupil, PupilID
from app.shared.db.base import Base


SCHEMA = "nutrition"
NutritionBase = declarative_base(cls=Base)
NutritionBase.__table_args__ = {"schema": SCHEMA}


class SchoolDB(NutritionBase):
    __tablename__ = "school"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)


class SchoolClassDB(NutritionBase):
    __tablename__ = "school_class"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    school_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(SchoolDB.id), nullable=False)
    number: Mapped[int] = Column(Integer, nullable=False)
    literal: Mapped[str] = Column(String(1), nullable=False)

    school: Mapped[SchoolDB] = relationship(SchoolDB, uselist=False, viewonly=True)


class PupilDB(NutritionBase):
    __tablename__ = "pupil"

    id: Mapped[str] = Column(String, primary_key=True)
    last_name: Mapped[str] = Column(String, nullable=False)
    first_name: Mapped[str] = Column(String, nullable=False)
    patronymic: Mapped[str | None] = Column(String, nullable=True)
    has_breakfast: Mapped[bool] = Column(Boolean, nullable=False)
    has_dinner: Mapped[bool] = Column(Boolean, nullable=False)
    has_snacks: Mapped[bool] = Column(Boolean, nullable=False)
    preferential_certificate_ends_at: Mapped[date | None] = Column(Date, nullable=True)
    school_class_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(SchoolClassDB.id), nullable=False)

    cancellation_periods: Mapped[list["CancellationPeriodDB"]] = relationship("CancellationPeriodDB", uselist=True)

    parents: Mapped[list["ParentDB"]] = relationship(
        "ParentDB", secondary=f"{SCHEMA}.child", uselist=True, viewonly=True
    )
    school_class: Mapped[SchoolClassDB] = relationship(SchoolClassDB, uselist=False, viewonly=True)

    def __init__(
        self,
        id_: str,
        last_name: str,
        first_name: str,
        patronymic: str | None,
        has_breakfast: bool,
        has_dinner: bool,
        has_snacks: bool,
        preferential_certificate_ends_at: date | None,
        cancellation_periods: list["CancellationPeriodDB"],
    ) -> None:
        super().__init__()

        self.id = id_
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.has_breakfast = has_breakfast
        self.has_dinner = has_dinner
        self.has_snacks = has_snacks
        self.preferential_certificate_ends_at = preferential_certificate_ends_at
        self.cancellation_periods = cancellation_periods

    def to_model(self) -> Pupil:
        return Pupil(
            id=PupilID(self.id),
            first_name=Name(self.first_name),
            last_name=Name(self.last_name),
            patronymic=Name(self.patronymic) if self.patronymic else None,
            has_breakfast=self.has_breakfast,
            has_dinner=self.has_dinner,
            has_snacks=self.has_snacks,
            preferential_certificate=PreferentialCertificate(ends_at=self.preferential_certificate_ends_at)
            if self.preferential_certificate_ends_at
            else None,
            cancellation_periods=CancellationPeriodSequence(
                tuple(period.to_model() for period in self.cancellation_periods)
            ),
        )


class CancellationPeriodDB(NutritionBase):
    __tablename__ = "cancellation_period"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    pupil_id: Mapped[str] = Column(String, ForeignKey(PupilDB.id), nullable=False)
    starts_at: Mapped[date] = Column(Date, nullable=False)
    ends_at: Mapped[date] = Column(Date, nullable=False)
    reasons: Mapped[list[str]] = Column(ARRAY(String, dimensions=1), nullable=False)  # type: ignore

    def __init__(self, id_: UUID, pupil_id: str, starts_at: date, ends_at: date, reasons: list[str]) -> None:
        super().__init__()

        self.id = id_
        self.pupil_id = pupil_id
        self.starts_at = starts_at
        self.ends_at = ends_at
        self.reasons = reasons

    def to_model(self) -> CancellationPeriod:
        return CancellationPeriod(
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            reasons=frozenset(Reason(reason) for reason in self.reasons),
        )


class ParentDB(NutritionBase):
    __tablename__ = "parent"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)

    children: Mapped[PupilDB] = relationship(PupilDB, secondary=f"{SCHEMA}.child", uselist=True, viewonly=True)

    def __init__(self, id_: UUID) -> None:
        super().__init__()

        self.id = id_

    def to_model(self) -> Parent:
        return Parent(id=self.id, child_ids=set(PupilID(child.id) for child in self.children))


class ChildDB(NutritionBase):
    __tablename__ = "child"

    parent_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(ParentDB.id), primary_key=True)
    pupil_id: Mapped[str] = Column(String, ForeignKey(PupilDB.id), primary_key=True)
