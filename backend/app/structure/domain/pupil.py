from dataclasses import dataclass

from result import Err, Ok, Result

from app.shared.domain.personal_info import FullName
from app.shared.domain.pupil import PupilID
from app.structure.domain.parent import Parent, ParentID
from app.structure.domain.school_class import ClassID


class ParentIsAlreadyAttached:
    pass


@dataclass
class Pupil:
    id: PupilID
    name: FullName
    class_id: ClassID
    parents: set[ParentID]

    def attach_to_parent(self, parent: Parent) -> Result["Pupil", ParentIsAlreadyAttached]:
        if parent.id in self.parents:
            return Err(ParentIsAlreadyAttached())

        self.parents.add(parent.id)

        return Ok(self)
