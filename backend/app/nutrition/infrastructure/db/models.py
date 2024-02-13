from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from sqlalchemy import ARRAY, Boolean, Column, Date, ForeignKey, Integer, Numeric, String, literal
from sqlalchemy.dialects.postgresql import JSONB, UUID as UUID_DB
from sqlalchemy.orm import Mapped, declarative_base, relationship
from sqlalchemy.sql import expression

from app.nutrition.domain.cancellation import CancellationPeriod, ReasonText
from app.nutrition.domain.menu import Food, Menu
from app.nutrition.domain.parent import Parent
from app.nutrition.domain.pupil import MealPlan, Name, PreferentialCertificate, Pupil, PupilID
from app.nutrition.domain.request import DraftRequest, PupilInfo, Request
from app.nutrition.domain.school_class import SchoolClass, SchoolClassInitials, SchoolClassType
from app.nutrition.domain.times import CancellationPeriodSequence, Day
from app.shared.db.base import Base
from app.shared.domain.money import Money


SCHEMA = "nutrition"
NutritionBase = declarative_base(cls=Base)
NutritionBase.__table_args__ = {"schema": SCHEMA}


class SchoolDB(NutritionBase):
    __tablename__ = "school"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)


class TeacherDB(NutritionBase):
    __tablename__ = "teacher"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)


class SchoolClassDB(NutritionBase):
    __tablename__ = "school_class"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    school_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(SchoolDB.id), nullable=False)
    teacher_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(TeacherDB.id), nullable=True)
    breakfast: Mapped[bool] = Column(Boolean, nullable=False, server_default=expression.true())
    dinner: Mapped[bool] = Column(Boolean, nullable=False, server_default=expression.true())
    snacks: Mapped[bool] = Column(Boolean, nullable=False, server_default=expression.true())
    number: Mapped[int] = Column(Integer, nullable=False)
    literal: Mapped[str] = Column(String(1), nullable=False)

    pupils: Mapped[list["PupilDB"]] = relationship("PupilDB", uselist=True, lazy="selectin")
    school: Mapped[SchoolDB] = relationship(SchoolDB, uselist=False, viewonly=True)
    teacher: Mapped[TeacherDB] = relationship(TeacherDB, uselist=False, viewonly=True)

    def to_model(self) -> SchoolClass:
        return SchoolClass(
            id=self.id,
            initials=SchoolClassInitials(literal=self.literal, number=self.number),
            teacher_id=self.teacher_id,
            breakfast=self.breakfast,
            dinner=self.dinner,
            snacks=self.snacks,
            pupils=[pupil_db.to_model() for pupil_db in self.pupils],
        )


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

    cancellation_periods: Mapped[list["CancellationPeriodDB"]] = relationship(
        "CancellationPeriodDB", uselist=True, lazy="selectin"
    )

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
            meal_plan=MealPlan(breakfast=self.has_breakfast, dinner=self.has_dinner, snacks=self.has_snacks),
            preferential_certificate=PreferentialCertificate(ends_at=self.preferential_certificate_ends_at)
            if self.preferential_certificate_ends_at
            else None,
            cancellation=CancellationPeriodSequence(tuple(period.to_model() for period in self.cancellation_periods)),
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
            reasons=frozenset(ReasonText(reason) for reason in self.reasons),
        )


class ParentDB(NutritionBase):
    __tablename__ = "parent"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)

    children: Mapped[list[PupilDB]] = relationship(PupilDB, secondary=f"{SCHEMA}.child", uselist=True, viewonly=True)

    def __init__(self, id_: UUID) -> None:
        super().__init__()

        self.id = id_

    def to_model(self) -> Parent:
        return Parent(id=self.id, child_ids=set(PupilID(child.id) for child in self.children))


class ChildDB(NutritionBase):
    __tablename__ = "child"

    parent_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(ParentDB.id), primary_key=True)
    pupil_id: Mapped[str] = Column(String, ForeignKey(PupilDB.id), primary_key=True)


class FoodDB(NutritionBase):
    __tablename__ = "food"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=False)
    calories: Mapped[Decimal] = Column(Numeric(asdecimal=True, scale=2), nullable=False)
    proteins: Mapped[Decimal] = Column(Numeric(asdecimal=True, scale=2), nullable=False)
    fats: Mapped[Decimal] = Column(Numeric(asdecimal=True, scale=2), nullable=False)
    carbohydrates: Mapped[Decimal] = Column(Numeric(asdecimal=True, scale=2), nullable=False)
    weight: Mapped[Decimal] = Column(Numeric(asdecimal=True, scale=2), nullable=False, server_default=literal(0))
    price: Mapped[Decimal] = Column(Numeric(asdecimal=True, scale=2), nullable=False)
    photo: Mapped[str] = Column(String(1024), nullable=False)

    def to_model(self) -> Food:
        return Food(
            id=self.id,
            name=self.name,
            description=self.description,
            calories=self.calories,
            proteins=self.proteins,
            fats=self.fats,
            carbohydrates=self.carbohydrates,
            weight=self.weight,
            price=Money(self.price),
            photo=Path(self.photo),
        )


class MenuDB(NutritionBase):
    __tablename__ = "menu"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    school_class_type: Mapped[int] = Column(Integer, nullable=False)
    on_date: Mapped[date] = Column(Date, nullable=False)

    breakfast_foods: Mapped[list[FoodDB]] = relationship(FoodDB, secondary=f"{SCHEMA}.breakfast_food", uselist=True)
    dinner_foods: Mapped[list[FoodDB]] = relationship(FoodDB, secondary=f"{SCHEMA}.dinner_food", uselist=True)
    snacks_foods: Mapped[list[FoodDB]] = relationship(FoodDB, secondary=f"{SCHEMA}.snacks_food", uselist=True)

    def to_model(self) -> Menu:
        return Menu(
            id=self.id,
            school_class_type=SchoolClassType(self.school_class_type),
            on_date=self.on_date,
            breakfast_foods=[food_db.to_model() for food_db in self.breakfast_foods],
            dinner_foods=[food_db.to_model() for food_db in self.dinner_foods],
            snacks_foods=[food_db.to_model() for food_db in self.snacks_foods],
        )


class BreakfastFoodDB(NutritionBase):
    __tablename__ = "breakfast_food"

    menu_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(MenuDB.id), primary_key=True)
    food_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(FoodDB.id), primary_key=True)


class DinnerFoodDB(NutritionBase):
    __tablename__ = "dinner_food"

    menu_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(MenuDB.id), primary_key=True)
    food_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(FoodDB.id), primary_key=True)


class SnacksFoodDB(NutritionBase):
    __tablename__ = "snacks_food"

    menu_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(MenuDB.id), primary_key=True)
    food_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(FoodDB.id), primary_key=True)


class DraftRequestDB(NutritionBase):
    __tablename__ = "draft_request"

    class_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(SchoolClassDB.id), primary_key=True)
    on_date: Mapped[date] = Column(Date, primary_key=True)
    pupils: Mapped[dict[str, tuple[bool, bool, bool]]] = Column(JSONB, nullable=False)

    def __init__(self, class_id: UUID, on_date: date, pupils: dict[str, tuple[bool, bool, bool]]) -> None:
        super().__init__()

        self.class_id = class_id
        self.on_date = on_date
        self.pupils = pupils

    def to_model(self) -> DraftRequest:
        return DraftRequest(
            class_id=self.class_id,
            on_date=Day(self.on_date),
            pupils={
                PupilID(pupil_id): MealPlan(breakfast=mealtimes[0], dinner=mealtimes[1], snacks=mealtimes[2])
                for pupil_id, mealtimes in self.pupils.items()
            },
        )

    @classmethod
    def from_model(cls, request: DraftRequest) -> "DraftRequestDB":
        return cls(
            class_id=request.class_id,
            on_date=request.on_date.date,
            pupils={
                pupil_id.value: (meal_plan.breakfast, meal_plan.dinner, meal_plan.snacks)
                for pupil_id, meal_plan in request.pupils.items()
            },
        )


class RequestDB(NutritionBase):
    __tablename__ = "request"

    class_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), ForeignKey(SchoolClassDB.id), primary_key=True)
    on_date: Mapped[date] = Column(Date, primary_key=True)
    pupils: Mapped[list[tuple[str, bool, bool, bool, bool]]] = Column(JSONB, nullable=False)

    def __init__(self, class_id: UUID, on_date: date, pupils: list[tuple[str, bool, bool, bool, bool]]) -> None:
        super().__init__()

        self.class_id = class_id
        self.on_date = on_date
        self.pupils = pupils

    def to_model(self) -> Request:
        return Request(
            class_id=self.class_id,
            on_date=Day(self.on_date),
            pupils=[
                PupilInfo(
                    id=PupilID(pupil[0]),
                    plan=MealPlan(breakfast=pupil[1], dinner=pupil[2], snacks=pupil[3]),
                    preferential=pupil[4],
                )
                for pupil in self.pupils
            ],
        )

    @classmethod
    def from_model(cls, request: Request) -> "RequestDB":
        return cls(
            class_id=request.class_id,
            on_date=request.on_date.date,
            pupils=[
                (pupil.id.value, pupil.plan.breakfast, pupil.plan.dinner, pupil.plan.snacks, pupil.preferential)
                for pupil in request.pupils
            ],
        )
