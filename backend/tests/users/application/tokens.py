from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.users.domain.tokens import AccessToken, RefreshToken


def validate_tokens(access: AccessToken, refresh: RefreshToken, expected_user_id: UUID) -> None:
    assert access.jti != refresh.jti
    assert access.device_id == refresh.device_id

    assert access.user_id == expected_user_id
    assert access.iat == datetime.now(tz=timezone.utc)
    assert access.exp == datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    assert refresh.user_id == expected_user_id
    assert refresh.iat == datetime.now(tz=timezone.utc)
    assert refresh.exp == datetime.now(tz=timezone.utc) + timedelta(days=10)
