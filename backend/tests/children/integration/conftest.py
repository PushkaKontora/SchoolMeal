import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.pupils.db.models import Pupil


CHILDREN_PREFIX = "/children"


@pytest.fixture
async def child(session: AsyncSession) -> Pupil:
    child = Pupil(
        id="b1goimpl8htpmf97faiv",
        last_name="Samkov",
        first_name="Nikita",
        certificate_before_date=None,
        balance=0,
        breakfast=False,
        lunch=False,
        dinner=False,
    )

    session.add(child)
    await session.commit()
    await session.refresh(child)

    return child
