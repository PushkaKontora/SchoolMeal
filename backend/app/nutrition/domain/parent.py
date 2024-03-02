from dataclasses import dataclass
from uuid import UUID, uuid4

from result import Err, Ok, Result

from app.nutrition.domain.personal_info import Email, FullName, Phone
from app.nutrition.domain.pupil import Pupil, PupilID


class PupilIsAlreadyAttached:
    pass


@dataclass(frozen=True, eq=True)
class ParentID:
    value: UUID

    @classmethod
    def generate(cls) -> "ParentID":
        return cls(uuid4())


@dataclass
class Parent:
    id: ParentID
    name: FullName
    email: Email
    phone: Phone
    children: set[PupilID]

    def attach_child(self, pupil: Pupil) -> Result[None, PupilIsAlreadyAttached]:
        if pupil.id in self.children:
            return Err(PupilIsAlreadyAttached())

        self.children.add(pupil.id)

        return Ok(None)
