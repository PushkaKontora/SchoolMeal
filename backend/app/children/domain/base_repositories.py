from abc import ABC

from app.children.db.models import Child
from app.database.base import Repository


class BaseChildrenRepository(Repository[Child], ABC):
    pass
