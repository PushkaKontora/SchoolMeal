from typing import Annotated

from fastapi import Depends

from app.shared.db.session import AlchemySession
from app.shared.fastapi.dependencies.db import SessionDep
from app.shared.unit_of_work import UnitOfWork


def _get_unit_of_work(session: SessionDep) -> UnitOfWork:
    return UnitOfWork(session=AlchemySession(session))


UnitOfWorkDep = Annotated[UnitOfWork, Depends(_get_unit_of_work)]
