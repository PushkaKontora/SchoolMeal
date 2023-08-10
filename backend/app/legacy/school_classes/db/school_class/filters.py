from app.legacy.db.specifications import FilterSpecification, TQuery
from app.legacy.school_classes.db.school_class.model import SchoolClass
from app.legacy.users.db.user.model import User


class ByOptionTeacherId(FilterSpecification):
    def __init__(self, teacher_id: int | None):
        self._teacher_id = teacher_id

    def __call__(self, query: TQuery) -> TQuery:
        return (
            query.join(SchoolClass.teachers).where(User.id == self._teacher_id)
            if self._teacher_id is not None
            else query
        )
