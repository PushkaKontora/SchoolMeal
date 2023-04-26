from abc import ABC

from app.database.base import Repository
from app.pupils.db.pupil.model import Pupil


class BasePupilsRepository(Repository[Pupil], ABC):
    pass
