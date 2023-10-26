from datetime import timedelta
from uuid import UUID

from app.users.domain.tokens import AccessToken, RefreshToken


def validate_tokens(access: AccessToken, refresh: RefreshToken, expected_user_id: UUID) -> None:
    assert access.jti != refresh.jti
    assert access.device_id == refresh.device_id

    assert access.user_id == expected_user_id
    assert access.exp == access.iat + timedelta(minutes=15)

    assert refresh.user_id == expected_user_id
    assert refresh.exp == refresh.iat + timedelta(days=10)
