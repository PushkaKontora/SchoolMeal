import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.pupils.db.pupil.model import Pupil


CHILDREN_PREFIX = "/children"


def child_prefix(child_id: str) -> str:
    return CHILDREN_PREFIX + f"/{child_id}"
