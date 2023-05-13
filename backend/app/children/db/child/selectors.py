from sqlalchemy.orm import load_only

from app.children.db.child.model import Child
from app.db.specifications import Specification, TQuery


class OnlyPupilId(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(load_only(Child.pupil_id))
