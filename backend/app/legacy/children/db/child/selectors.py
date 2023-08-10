from sqlalchemy.orm import load_only

from app.legacy.children.db.child.model import Child
from app.legacy.db.specifications import Specification, TQuery


class OnlyPupilId(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(load_only(Child.pupil_id))
