from datetime import datetime, timedelta
from enum import Enum

import pytest
from bcrypt import gensalt, hashpw
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import now

from app.auth.db.sqlalchemy.models import Password
from app.config import JWTSettings
from app.users.db.sqlalchemy.models import User
from app.users.domain.entities import Role


PREFIX = "/auth"

OLD_PASSWORD, ACTUAL_PASSWORD = ["old_pass", "actual_pass"]
LOGIN = "metkij_strelok"
OLD_HASHED_PASSWORD, ACTUAL_HASHED_PASSWORD = [
    hashpw(p.encode("utf-8"), gensalt()) for p in [OLD_PASSWORD, ACTUAL_PASSWORD]
]


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def get_expected_payload(token_type: TokenType, user_id: int, role: Role, ttl: timedelta) -> dict:
    return {
        "type": token_type.value,
        "user_id": user_id,
        "role": role.value,
        "exp": int((datetime.utcnow() + ttl).timestamp()),
    }


@pytest.fixture
async def user(session: AsyncSession) -> User:
    user = User(
        last_name="Dykov",
        first_name="Lima",
        login=LOGIN,
        role=Role.PARENT,
        phone="+78005553535",
        email="email@email.com",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    old_password, new_password = [
        Password(user_id=user.id, value=p, created_at=now() + delta)
        for p, delta in {OLD_HASHED_PASSWORD: timedelta(0), ACTUAL_HASHED_PASSWORD: timedelta(days=10)}.items()
    ]

    session.add(old_password)
    session.add(new_password)
    await session.commit()

    yield user


@pytest.fixture(scope="session")
def auth_settings() -> JWTSettings:
    return JWTSettings()
