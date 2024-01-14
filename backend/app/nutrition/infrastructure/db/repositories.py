from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.nutrition.application.repositories import (
    IDraftRequestsRepository,
    IMenusRepository,
    IParentsRepository,
    IPupilsRepository,
    IRequestsRepository,
    ISchoolClassesRepository,
    NotFoundDraftRequest,
    NotFoundMenu,
    NotFoundParent,
    NotFoundPupil,
    NotFoundRequest,
    NotFoundSchoolClass,
)
from app.nutrition.domain.menu import Menu
from app.nutrition.domain.parent import Parent
from app.nutrition.domain.periods import Day
from app.nutrition.domain.pupil import Pupil
from app.nutrition.domain.request import DraftRequest, Request
from app.nutrition.domain.school_class import SchoolClass, SchoolClassType
from app.nutrition.infrastructure.db.models import (
    CancellationPeriodDB,
    ChildDB,
    DraftRequestDB,
    MenuDB,
    ParentDB,
    PupilDB,
    RequestDB,
    SchoolClassDB,
)


class AlchemyPupilsRepository(IPupilsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, pupil_id: str) -> Pupil:
        try:
            query = select(PupilDB).where(PupilDB.id == pupil_id).options(selectinload(PupilDB.cancellation_periods))
            pupil_db: PupilDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundPupil from error

        return pupil_db.to_model()

    async def get_by_class_id(self, class_id: UUID) -> list[Pupil]:
        query = select(PupilDB).where(PupilDB.school_class_id == class_id)
        pupils_db: list[PupilDB] = (await self._session.scalars(query)).all()

        return [pupil_db.to_model() for pupil_db in pupils_db]

    async def update(self, pupil: Pupil) -> None:
        await self._session.execute(
            (
                update(PupilDB)
                .values(
                    last_name=pupil.last_name.value,
                    first_name=pupil.first_name.value,
                    patronymic=pupil.patronymic.value if pupil.patronymic else None,
                    has_breakfast=pupil.meal_plan.breakfast,
                    has_dinner=pupil.meal_plan.dinner,
                    has_snacks=pupil.meal_plan.snacks,
                    preferential_certificate_ends_at=pupil.preferential_certificate.ends_at
                    if pupil.preferential_certificate
                    else None,
                )
                .where(PupilDB.id == pupil.id.value)
            )
        )

        await self._session.execute(delete(CancellationPeriodDB).where(CancellationPeriodDB.pupil_id == pupil.id.value))
        periods = [
            CancellationPeriodDB(
                id_=uuid4(),
                pupil_id=pupil.id.value,
                starts_at=period.starts_at,
                ends_at=period.ends_at,
                reasons=[reason.value for reason in period.reasons],
            )
            for period in pupil.cancellation_periods
        ]
        self._session.add_all(periods)
        await self._session.flush(periods)


class AlchemyParentsRepository(IParentsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, parent_id: UUID) -> Parent:
        try:
            query = select(ParentDB).where(ParentDB.id == parent_id).options(selectinload(ParentDB.children))
            parent_db: ParentDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundParent from error

        return parent_db.to_model()

    async def update(self, parent: Parent) -> None:
        await self._session.execute(
            (
                insert(ChildDB)
                .values([{"parent_id": parent.id, "pupil_id": child_id.value} for child_id in parent.child_ids])
                .on_conflict_do_nothing(index_elements=[ChildDB.parent_id, ChildDB.pupil_id])
            )
        )


class AlchemyMenusRepository(IMenusRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_class_type_and_date(self, school_class_type: SchoolClassType, on_date: date) -> Menu:
        try:
            query = (
                select(MenuDB)
                .where(MenuDB.school_class_type == school_class_type.value)
                .where(MenuDB.on_date == on_date)
                .options(selectinload(MenuDB.breakfast_foods))
                .options(selectinload(MenuDB.dinner_foods))
                .options(selectinload(MenuDB.snacks_foods))
                .limit(1)
            )

            menu_db: MenuDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundMenu from error

        return menu_db.to_model()


class AlchemySchoolClassesRepository(ISchoolClassesRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id_: UUID) -> SchoolClass:
        try:
            query = select(SchoolClassDB).where(SchoolClassDB.id == id_).limit(1)
            class_db: SchoolClassDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundSchoolClass from error

        return class_db.to_model()

    async def get_all_by_teacher_id(self, teacher_id: UUID) -> list[SchoolClass]:
        query = select(SchoolClassDB).where(SchoolClassDB.teacher_id == teacher_id)
        classes_db: list[SchoolClassDB] = (await self._session.scalars(query)).all()

        return [class_db.to_model() for class_db in classes_db]

    async def get_all(self) -> list[SchoolClass]:
        query = select(SchoolClassDB)
        classes_db: list[SchoolClassDB] = (await self._session.scalars(query)).all()

        return [class_db.to_model() for class_db in classes_db]


class AlchemyDraftRequestsRepository(IDraftRequestsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_class_id_and_date(self, class_id: UUID, on_date: Day) -> DraftRequest:
        try:
            query = select(DraftRequestDB).where(
                DraftRequestDB.class_id == class_id, DraftRequestDB.on_date == on_date.date
            )
            request_db: DraftRequestDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundDraftRequest from error

        return request_db.to_model()

    async def upsert(self, request: DraftRequest) -> None:
        request_db = DraftRequestDB.from_model(request)

        query = (
            insert(DraftRequestDB)
            .values(**request_db.dict())
            .on_conflict_do_update(
                index_elements=[DraftRequestDB.class_id, DraftRequestDB.on_date],
                set_=request_db.dict(),
            )
        )
        await self._session.execute(query)


class AlchemyRequestsRepository(IRequestsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, request: Request) -> None:
        request_db = RequestDB.from_model(request)

        self._session.add(request_db)
        await self._session.flush([request_db])

    async def get_by_class_id_and_date(self, class_id: UUID, on_date: Day) -> Request:
        try:
            query = select(RequestDB).where(RequestDB.class_id == class_id, RequestDB.on_date == on_date.date).limit(1)
            request_db: RequestDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundRequest from error

        return request_db.to_model()
