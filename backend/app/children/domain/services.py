from dependency_injector.wiring import Provide, inject

from app.children.db.filters.child import ChildById, ParentById
from app.children.db.models import Child
from app.children.domain.exceptions import NotFoundChildException, NotFoundParentException, NotUniqueChildException
from app.database.container import Database
from app.database.unit_of_work import UnitOfWork
from app.pupils.db.filters.pupil import ById as PupilById
from app.users.db.filters.user import ById as UserById


class ChildService:
    @inject
    async def add_child(self, parent_id: int, child_id: str, uow: UnitOfWork = Provide[Database.unit_of_work]) -> None:
        async with uow:
            if not await uow.users_repo.exists(UserById(parent_id)):
                raise NotFoundParentException

            if not await uow.pupils_repo.exists(PupilById(child_id)):
                raise NotFoundChildException

            if await uow.children_repo.exists(ParentById(parent_id) & ChildById(child_id)):
                raise NotUniqueChildException

            uow.children_repo.save(Child(parent_id=parent_id, pupil_id=child_id))
            await uow.commit()
