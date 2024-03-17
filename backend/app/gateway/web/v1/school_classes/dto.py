from uuid import UUID

from pydantic import BaseModel


class GetSchoolClassesParams(BaseModel):
    teacher_id: UUID | None = None
