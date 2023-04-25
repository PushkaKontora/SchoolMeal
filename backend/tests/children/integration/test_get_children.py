from datetime import datetime

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.children.db.models import ParentPupil
from app.config import JWTSettings
from app.pupils.db.models import CancelMealPeriod, Pupil
from app.school_classes.db.models import SchoolClass, Teacher
from app.schools.db.models import School
from app.users.db.models import User
from tests.auth.integration.conftest import create_access_token
from tests.children.integration.conftest import CHILDREN_PREFIX
from tests.conftest import BearerAuth
from tests.utils import dt_to_str


URL = CHILDREN_PREFIX


async def get_children(client: AsyncClient, parent: User, jwt_settings: JWTSettings) -> Response:
    token = create_access_token(parent.id, parent.role, jwt_settings)
    return await client.get(URL, auth=BearerAuth(token))


async def test_getting_children(
    client: AsyncClient,
    session: AsyncSession,
    parent: User,
    school: School,
    school_class: SchoolClass,
    child: Pupil,
    teacher: User,
    cancel_meal_period: CancelMealPeriod,
    jwt_settings: JWTSettings,
):
    response = await get_children(client, parent, jwt_settings)

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": child.id,
            "lastName": child.last_name,
            "firstName": child.first_name,
            "certificateBeforeDate": dt_to_str(child.certificate_before_date),
            "balance": float(child.balance),
            "breakfast": child.breakfast,
            "lunch": child.lunch,
            "dinner": child.dinner,
            "schoolClass": {
                "id": school_class.id,
                "number": school_class.number,
                "letter": school_class.letter,
                "hasBreakfast": school_class.has_breakfast,
                "hasLunch": school_class.has_lunch,
                "hasDinner": school_class.has_dinner,
                "teachers": [
                    {
                        "id": teacher.id,
                        "lastName": teacher.last_name,
                        "firstName": teacher.first_name,
                        "phone": teacher.phone,
                        "email": teacher.email,
                    }
                ],
            },
            "school": {
                "id": school.id,
                "name": school.name,
            },
            "cancelMealPeriods": [
                {
                    "id": cancel_meal_period.id,
                    "startDate": str(cancel_meal_period.start_date),
                    "endDate": str(cancel_meal_period.end_date) if cancel_meal_period.end_date is not None else None,
                    "comment": cancel_meal_period.comment,
                }
            ],
        }
    ]


@pytest.fixture
async def school_class(session: AsyncSession, school: School) -> SchoolClass:
    school_class = SchoolClass(
        school_id=school.id,
        number=10,
        letter="И",
        has_breakfast=False,
        has_lunch=False,
        has_dinner=False,
    )

    session.add(school_class)
    await session.commit()
    await session.refresh(school_class)

    return school_class


@pytest.fixture
async def school(session: AsyncSession) -> School:
    school = School(name="ABC")
    session.add(school)
    await session.commit()
    await session.refresh(school)

    return school


@pytest.fixture
async def cancel_meal_period(session: AsyncSession, child: Pupil) -> CancelMealPeriod:
    period = CancelMealPeriod(
        pupil_id=child.id,
        start_date=datetime.utcnow(),
        end_date=None,
        comment="Comment",
    )
    session.add(period)
    await session.commit()
    await session.refresh(period)

    return period


@pytest.fixture(autouse=True)
async def prepare_data(session: AsyncSession, parent: User, child: Pupil, teacher: User, school_class: SchoolClass):
    session.add(ParentPupil(parent_id=parent.id, pupil_id=child.id))
    session.add(Teacher(class_id=school_class.id, user_id=teacher.id))
    child.class_id = school_class.id
    session.add(child)
    await session.commit()
