from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.nutrition.application.repositories import (
    IMenusRepository,
    IParentsRepository,
    IPupilsRepository,
    NotFoundParent,
    NotFoundPupil,
)
from app.nutrition.domain.menu import Menu
from app.nutrition.domain.parent import Parent
from app.nutrition.domain.pupil import Pupil
from app.nutrition.domain.school_class import SchoolClassType
from app.nutrition.infrastructure.db.models import CancellationPeriodDB, ChildDB, MenuDB, ParentDB, PupilDB


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

    async def update(self, pupil: Pupil) -> None:
        await self._session.execute(
            (
                update(PupilDB)
                .values(
                    last_name=pupil.last_name.value,
                    first_name=pupil.first_name.value,
                    patronymic=pupil.patronymic.value if pupil.patronymic else None,
                    has_breakfast=pupil.has_breakfast,
                    has_dinner=pupil.has_dinner,
                    has_snacks=pupil.has_snacks,
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

    async def get_all_by_class_type_and_date(self, school_class_type: SchoolClassType, on_date: date) -> list[Menu]:
        query = (
            select(MenuDB)
            .where(MenuDB.school_class_type == school_class_type.value)
            .where(MenuDB.on_date == on_date)
            .options(selectinload(MenuDB.breakfast_foods))
            .options(selectinload(MenuDB.dinner_foods))
            .options(selectinload(MenuDB.snacks_foods))
        )

        menus_db: list[MenuDB] = (await self._session.scalars(query)).all()

        return [menu_db.to_model() for menu_db in menus_db]
