from typing import Annotated

from fastapi import Depends

from app.common.api.dependencies.db import SessionDep
from app.nutrition.application.repositories import IPupilsRepository
from app.nutrition.infrastructure.db.repositories import PupilsRepository


def _get_pupils_repository(session: SessionDep) -> IPupilsRepository:
    return PupilsRepository(session)


PupilsRepositoryDep = Annotated[IPupilsRepository, Depends(_get_pupils_repository)]
