from pydantic import BaseModel


class Override(BaseModel):
    pupil_id: str
    breakfast: bool
    dinner: bool
    snacks: bool

    def __hash__(self) -> int:
        return hash(self.pupil_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Override) and self.pupil_id == other.pupil_id
