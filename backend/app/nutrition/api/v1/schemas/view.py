from collections import Counter
from datetime import date
from enum import Enum, unique
from typing import Iterable
from uuid import UUID

from app.nutrition.api.v1.schemas.enums import MealtimeDTO, NutritionStatusDTO
from app.nutrition.domain.pupil import NutritionStatus, Pupil
from app.nutrition.domain.request import Declaration, Request, RequestStatus
from app.nutrition.domain.school_class import SchoolClass
from app.nutrition.domain.time import Period
from app.shared.api.schemas import FrontendBody
from app.shared.domain.personal_info import FullName


@unique
class RequestStatusOut(Enum):
    PREFILLED = "prefilled"
    SUBMITTED = "submitted"

    @classmethod
    def from_model(cls, status: RequestStatus) -> "RequestStatusOut":
        return {
            RequestStatus.PREFILLED: cls.PREFILLED,
            RequestStatus.SUBMITTED: cls.SUBMITTED,
        }[status]


class PeriodOut(FrontendBody):
    start: date
    end: date

    @classmethod
    def from_model(cls, period: Period) -> "PeriodOut":
        return cls(start=period.start, end=period.end)


class PupilOut(FrontendBody):
    id: str
    class_id: UUID
    parent_ids: list[UUID]
    last_name: str
    first_name: str
    patronymic: str | None
    mealtimes: list[MealtimeDTO]
    preferential_until: date | None
    cancelled_periods: list[PeriodOut]
    nutrition: NutritionStatusDTO

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilOut":
        return cls(
            id=pupil.id.value,
            class_id=pupil.class_id.value,
            parent_ids=[parent_id.value for parent_id in pupil.parent_ids],
            last_name=pupil.name.last.value,
            first_name=pupil.name.first.value,
            patronymic=pupil.name.patronymic.value if pupil.name.patronymic else None,
            mealtimes=[MealtimeDTO.from_model(mealtime) for mealtime in pupil.mealtimes],
            preferential_until=pupil.preferential_until,
            cancelled_periods=[PeriodOut.from_model(period) for period in pupil.cancelled_periods],
            nutrition=NutritionStatusDTO.from_model(pupil.nutrition),
        )


class SchoolClassOut(FrontendBody):
    id: UUID
    teacher_id: UUID | None
    number: int
    literal: str
    mealtimes: list[MealtimeDTO]

    @classmethod
    def from_model(cls, school_class: SchoolClass) -> "SchoolClassOut":
        return cls(
            id=school_class.id.value,
            teacher_id=school_class.teacher_id.value if school_class.teacher_id else None,
            number=school_class.number.value,
            literal=school_class.literal.value,
            mealtimes=[MealtimeDTO.from_model(mealtime) for mealtime in school_class.mealtimes],
        )


class DeclarationOut(FrontendBody):
    id: str
    last_name: str
    first_name: str
    patronymic: str | None
    mealtimes: list[MealtimeDTO]
    nutrition: NutritionStatusDTO

    @classmethod
    def from_model(cls, declaration: Declaration, name: FullName) -> "DeclarationOut":
        return cls(
            id=declaration.pupil_id.value,
            last_name=name.last.value,
            first_name=name.first.value,
            patronymic=name.patronymic.value if name.patronymic else None,
            mealtimes=[MealtimeDTO.from_model(mealtime) for mealtime in declaration.mealtimes],
            nutrition=NutritionStatusDTO.from_model(declaration.nutrition),
        )


class RequestOut(FrontendBody):
    class_id: UUID
    on_date: date
    status: RequestStatusOut
    mealtimes: list[MealtimeDTO]
    pupils: list[DeclarationOut]

    @classmethod
    def from_models(cls, request: Request, pupils: Iterable[Pupil]) -> "RequestOut":
        pupil_by_id = {pupil.id: pupil for pupil in pupils}

        declarations_out: list[DeclarationOut] = []
        for declaration in request.declarations:
            if not (pupil := pupil_by_id.get(declaration.pupil_id)):
                continue

            declarations_out.append(DeclarationOut.from_model(declaration, name=pupil.name))

        return cls(
            class_id=request.class_id.value,
            on_date=request.on_date,
            status=RequestStatusOut.from_model(request.status),
            mealtimes=[MealtimeDTO.from_model(mealtime) for mealtime in request.mealtimes],
            pupils=declarations_out,
        )


class PortionsOut(FrontendBody):
    paid: int
    preferential: int
    total: int

    @classmethod
    def create(cls, paid: int, preferential: int) -> "PortionsOut":
        return cls(paid=paid, preferential=preferential, total=paid + preferential)


class ClassPortionsOut(FrontendBody):
    id: UUID
    number: int
    literal: str
    portions: dict[MealtimeDTO, PortionsOut]

    @classmethod
    def create(cls, school_class: SchoolClass, request: Request | None) -> "ClassPortionsOut":
        portions: dict[MealtimeDTO, PortionsOut] = {}

        if request:
            totals = {mealtime: Counter[NutritionStatus]() for mealtime in request.mealtimes}

            for declaration in request.declarations:
                for mealtime in declaration.mealtimes:
                    totals[mealtime][declaration.nutrition] += 1

            portions = {
                MealtimeDTO.from_model(mealtime): PortionsOut.create(
                    paid=totals[mealtime][NutritionStatus.PAID],
                    preferential=totals[mealtime][NutritionStatus.PREFERENTIAL],
                )
                for mealtime in request.mealtimes
            }

        return cls(
            id=school_class.id.value,
            number=school_class.number.value,
            literal=school_class.literal.value,
            portions=portions,
        )


class PortionsReportOut(FrontendBody):
    school_classes: list[ClassPortionsOut]
    totals: dict[MealtimeDTO, PortionsOut]

    @classmethod
    def create(cls, school_classes: Iterable[SchoolClass], requests: Iterable[Request]) -> "PortionsReportOut":
        reports: list[ClassPortionsOut] = []
        totals: dict[MealtimeDTO, Counter[NutritionStatus]] = {mealtime: Counter() for mealtime in MealtimeDTO}

        request_by_class_id = {request.class_id: request for request in requests}

        for school_class in school_classes:
            report = ClassPortionsOut.create(school_class, request=request_by_class_id.get(school_class.id))

            for mealtime, portions in report.portions.items():
                totals[mealtime][NutritionStatus.PAID] += portions.paid
                totals[mealtime][NutritionStatus.PREFERENTIAL] += portions.preferential

            reports.append(report)

        return cls(
            school_classes=reports,
            totals={
                mealtime: PortionsOut.create(
                    paid=totals[mealtime][NutritionStatus.PAID],
                    preferential=totals[mealtime][NutritionStatus.PREFERENTIAL],
                )
                for mealtime in MealtimeDTO
            },
        )
