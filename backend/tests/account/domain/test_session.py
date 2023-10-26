from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.account.domain.session import AlreadySessionRevokedError, Session


def test_revoke(session: Session):
    session.revoke()

    assert session.revoked is True


def test_revoke_revoked_session(session: Session):
    session.revoke()

    with pytest.raises(AlreadySessionRevokedError):
        session.revoke()


@pytest.fixture
def session() -> Session:
    return Session(
        id=uuid4(),
        device_id=uuid4(),
        jti=uuid4(),
        credential_id=uuid4(),
        revoked=False,
        created_at=datetime.now(tz=timezone.utc),
    )
