from uuid import UUID

from app.children.application.repositories import IChildrenRepository, IParentsRepository
from app.children.domain.child import Child, ChildID
from app.shared.unit_of_work import UnitOfWork


class ChildrenService:
    def __init__(
        self, unit_of_work: UnitOfWork, parents_repository: IParentsRepository, children_repository: IChildrenRepository
    ) -> None:
        self._unit_of_work = unit_of_work
        self._parents = parents_repository
        self._children = children_repository

    async def attach_child_to_parent(self, parent_id: UUID, child_id: str) -> None:
        """
        :raise NotFoundParent: не найден родитель
        :raise NotFoundPupil: не найден ученик
        :raise PupilIsAlreadyParentsChild: ученик уже является ребёнком данного родителя
        """

        async with self._unit_of_work as session:
            parent = await self._parents.get_by_id(parent_id=parent_id)
            child = await self._children.get_by_id(child_id=ChildID(child_id))

            updated_parent = parent.add_child(child)
            await self._parents.update(updated_parent)

            await session.commit()

    async def get_children(self, parent_id: UUID) -> list[Child]:
        """
        :raise NotFoundParent: не найден родитель
        """

        parent = await self._parents.get_by_id(parent_id=parent_id)

        return await self._children.get_all_by_ids(ids=parent.child_ids)
