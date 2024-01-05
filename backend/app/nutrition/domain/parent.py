from uuid import UUID

from pydantic.dataclasses import dataclass

from app.nutrition.domain.pupil import Pupil, PupilID
from app.shared.domain.abc import Entity


class ChildIsAlreadyAttachedToParent(Exception):
    pass


@dataclass
class Parent(Entity):
    id: UUID
    child_ids: set[PupilID]

    def add_child(self, pupil: Pupil) -> None:
        """
        :raise ChildIsAlreadyAttachedToParent: ребёнок уже привязан к родителю
        """

        if pupil.id in self.child_ids:
            raise ChildIsAlreadyAttachedToParent

        self.child_ids.add(pupil.id)
