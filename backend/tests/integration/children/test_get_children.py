from datetime import datetime

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import JWTSettings
from app.legacy.cancel_meal_periods import CancelMealPeriod
from app.legacy.children.db.child.model import Child
from app.legacy.pupils.db.pupil.model import Pupil
from app.legacy.school_classes.db import Teacher
from app.legacy.school_classes.db.school_class import SchoolClass
from app.legacy.schools.db.school import School
from app.legacy.users.db.user.model import User
from tests.integration.auth.conftest import create_access_token
from tests.integration.children.conftest import CHILDREN_PREFIX
from tests.integration.conftest import BearerAuth
from tests.integration.utils import date_to_str, datetime_to_str


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
    pupil: Pupil,
    teacher: User,
    cancel_meal_period: CancelMealPeriod,
    jwt_settings: JWTSettings,
):
    response = await get_children(client, parent, jwt_settings)

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": pupil.id,
            "lastName": pupil.last_name,
            "firstName": pupil.first_name,
            "certificateBeforeDate": datetime_to_str(pupil.certificate_before_date),
            "balance": pupil.balance,
            "breakfast": pupil.breakfast,
            "lunch": pupil.lunch,
            "dinner": pupil.dinner,
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
                "school": {
                    "id": school.id,
                    "name": school.name,
                },
            },
            "cancelMealPeriods": [
                {
                    "id": cancel_meal_period.id,
                    "startDate": date_to_str(cancel_meal_period.start_date),
                    "endDate": date_to_str(cancel_meal_period.end_date),
                    "comment": cancel_meal_period.comment,
                }
            ],
        }
    ]


async def test_get_without_class_and_periods(
    client: AsyncClient,
    session: AsyncSession,
    parent: User,
    pupil: Pupil,
    cancel_meal_period: CancelMealPeriod,
    jwt_settings: JWTSettings,
):
    pupil.class_id = None
    session.add(pupil)
    await session.delete(cancel_meal_period)
    await session.commit()

    response = await get_children(client, parent, jwt_settings)

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": pupil.id,
            "lastName": pupil.last_name,
            "firstName": pupil.first_name,
            "certificateBeforeDate": datetime_to_str(pupil.certificate_before_date),
            "balance": pupil.balance,
            "breakfast": pupil.breakfast,
            "lunch": pupil.lunch,
            "dinner": pupil.dinner,
            "schoolClass": None,
            "cancelMealPeriods": [],
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
async def cancel_meal_period(session: AsyncSession, pupil: Pupil) -> CancelMealPeriod:
    period = CancelMealPeriod(
        pupil_id=pupil.id,
        start_date=datetime.utcnow(),
        end_date=None,
        comment="Comment",
    )
    session.add(period)
    await session.commit()
    await session.refresh(period)

    return period


@pytest.fixture(autouse=True)
async def prepare_data(session: AsyncSession, parent: User, pupil: Pupil, teacher: User, school_class: SchoolClass):
    session.add(Child(parent_id=parent.id, pupil_id=pupil.id))
    session.add(Teacher(class_id=school_class.id, user_id=teacher.id))
    pupil.class_id = school_class.id
    pupil.balance = 0.15
    session.add(pupil)
    await session.commit()
