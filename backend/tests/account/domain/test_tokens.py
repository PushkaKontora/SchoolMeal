from datetime import datetime, timezone
from uuid import uuid4

import pytest
from freezegun import freeze_time

from app.account.domain.tokens import AccessToken, ExpirationSignatureError, InvalidSignatureError, RefreshToken, Token


ACCESS = AccessToken(jti=uuid4(), device_id=uuid4(), credential_id=uuid4(), iat=datetime.now(tz=timezone.utc))
REFRESH = RefreshToken(jti=uuid4(), device_id=uuid4(), credential_id=uuid4(), iat=datetime.now(tz=timezone.utc))


@pytest.mark.parametrize("token", [ACCESS, REFRESH])
def test_encoding_and_decoding(token: Token, secret: str):
    encoded = token.encode(secret)
    decoded = token.__class__.decode(encoded, secret)

    assert token == decoded


@pytest.mark.parametrize("token", [ACCESS, REFRESH])
def test_decoding_with_invalid_signature(token: Token, secret: str):
    broken = token.encode(secret)[:-3]

    with pytest.raises(InvalidSignatureError):
        token.__class__.decode(broken, secret)


@pytest.mark.parametrize("token", [ACCESS, REFRESH])
@freeze_time()
def test_decoding_with_expired_signature(token: Token, secret: str):
    encoded = token.encode(secret)

    with freeze_time(token.exp):
        with pytest.raises(ExpirationSignatureError):
            Token.decode(encoded, secret)


def test_decoding_access_as_refresh(secret: str):
    access = ACCESS.encode(secret)

    with pytest.raises(InvalidSignatureError):
        RefreshToken.decode(access, secret)


def test_decoding_refresh_as_access(secret: str):
    refresh = REFRESH.encode(secret)

    with pytest.raises(InvalidSignatureError):
        AccessToken.decode(refresh, secret)


@pytest.fixture(scope="module")
def secret() -> str:
    return "a" * 10
