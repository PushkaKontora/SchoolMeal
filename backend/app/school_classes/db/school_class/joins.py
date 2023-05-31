from sqlalchemy.orm import joinedload

from app.db.specifications import Specification, TQuery
from app.school_classes.db.school_class.model import SchoolClass


class WithSchool(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(joinedload(SchoolClass.school))
