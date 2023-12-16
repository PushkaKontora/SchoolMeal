from uuid import UUID

from app.children.application.unit_of_work import ChildrenContext
from app.children.domain.child import Child, ChildID
from app.shared.unit_of_work.abc import IUnitOfWork


class ChildrenService:
    def __init__(self, unit_of_work: IUnitOfWork[ChildrenContext]) -> None:
        self._unit_of_work = unit_of_work

    async def attach_child_to_parent(self, parent_id: UUID, child_id: str) -> None:
        """
        :raise NotFoundParent: не найден родитель
        :raise NotFoundPupil: не найден ученик
        :raise PupilIsAlreadyParentsChild: ученик уже является ребёнком данного родителя
        """

        async with self._unit_of_work as context:
            parent = await context.parents.get_by_id(parent_id=parent_id)
            child = await context.children.get_by_id(child_id=ChildID(child_id))

            updated_parent = parent.add_child(child)
            await context.parents.update(updated_parent)

            await self._unit_of_work.commit()

    async def get_children(self, parent_id: UUID) -> list[Child]:
        """
        :raise NotFoundParent: не найден родитель
        """

        async with self._unit_of_work as context:
            parent = await context.parents.get_by_id(parent_id=parent_id)

            return await context.children.get_all_by_ids(ids=parent.child_ids)
