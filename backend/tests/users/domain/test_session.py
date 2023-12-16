from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.users.domain.session import Session, SessionIsAlreadyRevoked


def test_revoke(session: Session):
    session.revoke()

    assert session.revoked is True


def test_revoke_revoked_session(session: Session):
    session.revoke()

    with pytest.raises(SessionIsAlreadyRevoked):
        session.revoke()


@pytest.fixture
def session() -> Session:
    return Session(
        id=uuid4(),
        device_id=uuid4(),
        jti=uuid4(),
        user_id=uuid4(),
        revoked=False,
        created_at=datetime.now(tz=timezone.utc),
    )
