from uuid import UUID

from app.nutrition.application.context import NutritionContext
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.unit_of_work.abc import IUnitOfWork


class AttachChildToParentCommand(Command):
    parent_id: UUID
    pupil_id: str


class AttachChildToParentCommandHandler(ICommandHandler[AttachChildToParentCommand, None]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: AttachChildToParentCommand) -> None:
        """
        :raise NotFoundParent: не найден родитель
        :raise NotFoundPupil: не найден ученик
        :raise ChildIsAlreadyAssignedToParent: ученик уже является ребёнком данного родителя
        """

        async with self._unit_of_work as context:
            parent = await context.parents.get_by_id(parent_id=command.parent_id)
            child = await context.pupils.get_by_id(pupil_id=command.pupil_id)

            parent.add_child(child)
            await context.parents.update(parent)

            await self._unit_of_work.commit()
