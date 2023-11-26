from uuid import UUID

from app.children.application.repositories import IChildrenRepository, IParentsRepository
from app.children.domain.child import Child, ChildID


async def add_child_to_parent(
    parent_id: UUID,
    child_id: str,
    parents_repository: IParentsRepository,
    children_repository: IChildrenRepository,
) -> None:
    """
    :raise NotFoundParent:
    :raise NotFoundPupil:
    :raise PupilIsAlreadyParentsChild: ученик уже является ребёнком данного родителя
    """

    parent = await parents_repository.get_by_id(parent_id=parent_id)
    child = await children_repository.get_by_id(child_id=ChildID(child_id))

    updated_parent = parent.add_child(child)
    await parents_repository.update(updated_parent)


async def get_children(
    parent_id: UUID, parents_repository: IParentsRepository, children_repository: IChildrenRepository
) -> list[Child]:
    """
    :raise NotFoundParent:
    """

    parent = await parents_repository.get_by_id(parent_id=parent_id)

    return await children_repository.get_all_by_ids(ids=parent.child_ids)
