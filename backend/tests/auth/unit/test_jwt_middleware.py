from datetime import datetime, timedelta
from unittest.mock import Mock

import freezegun
import pytest

from app.auth.domain.entities import JWTPayload
from app.auth.domain.errors import InvalidTokenSignatureError, TokenExpirationError
from app.auth.presentation.errors import InvalidAuthorizationHeaderError, UnauthorizedError
from app.auth.presentation.middlewares import JWTAuth
from app.config import JWTSettings
from app.users.db.user.model import Role
from tests.auth.integration.conftest import TokenType, create_access_token, generate_token, get_expected_payload


class Auth(JWTAuth):
    payload: JWTPayload

    def authorize(self, payload: JWTPayload) -> bool:
        return payload.user_id == 0


def get_request(token: str, schema: str = "Bearer") -> Mock:
    request = Mock()
    request.headers = {"Authorization": f"{schema} {token}"}

    return request


@pytest.mark.parametrize(
    ["schema", "delta"],
    [["Bearer", timedelta(seconds=-1)], ["bearer", timedelta(seconds=-2)], ["bEaRer", timedelta(seconds=-3)]],
)
async def test_correct_authentication(
    jwt_auth: JWTAuth,
    auth_settings: JWTSettings,
    schema: str,
    delta: timedelta,
    user_id: int = 0,
    role: Role = Role.PARENT,
):
    with freezegun.freeze_time(datetime.utcnow() - auth_settings.access_token_ttl - delta):
        token = create_access_token(user_id, role, auth_settings)
        request = get_request(token, schema)

        payload = await jwt_auth(request)
        assert payload.dict() == get_expected_payload(TokenType.ACCESS, user_id, role, auth_settings.access_token_ttl)


@freezegun.freeze_time()
async def test_invalid_signature_processing(jwt_auth: JWTAuth, auth_settings: JWTSettings):
    token = create_access_token(0, Role.PARENT, auth_settings)[:-2]

    with pytest.raises(InvalidTokenSignatureError):
        await jwt_auth(get_request(token))


@freezegun.freeze_time()
async def test_invalid_token_type_processing(jwt_auth: JWTAuth, jwt_settings: JWTSettings):
    payload = get_expected_payload(TokenType.REFRESH, 0, Role.PARENT, jwt_settings.access_token_ttl)
    token = generate_token(payload, jwt_settings.secret.get_secret_value(), jwt_settings.algorithm)

    with pytest.raises(InvalidTokenSignatureError):
        await jwt_auth(get_request(token))


@pytest.mark.parametrize(["delta"], [[timedelta(0)], [timedelta(seconds=1)]])
@freezegun.freeze_time()
async def test_expiration_processing(jwt_auth: JWTAuth, auth_settings: JWTSettings, delta: timedelta):
    with freezegun.freeze_time(datetime.utcnow() - auth_settings.access_token_ttl - delta):
        token = create_access_token(0, Role.PARENT, auth_settings)

    with pytest.raises(TokenExpirationError):
        await jwt_auth(get_request(token))


@pytest.mark.parametrize(
    ["header", "schema", "token"],
    [
        ["Unknown header", "Bearer", "123"],
        ["authorization", "Bearer", "123"],
        ["Authorization", "Token", "123"],
        ["Authorization", "", "123"],
        ["Authorization", "Bearer", ""],
    ],
    ids=[
        "expected header name Authorization",
        "a header should start with a capital letter",
        "a schema should be bearer",
        "a schema should be",
        "a token should be",
    ],
)
async def test_invalid_header_processing(jwt_auth: JWTAuth, header: str, schema: str, token: str):
    request = Mock()
    request.headers = {header: f"{schema} {token}".lstrip()}

    with pytest.raises(InvalidAuthorizationHeaderError):
        await jwt_auth(request)


@pytest.mark.parametrize(["user_id", "is_authorized"], [[0, True], [1, False]])
async def test_authorization(
    jwt_auth: JWTAuth, user_id: int, is_authorized: bool, auth_settings: JWTSettings, role: Role = Role.PARENT
):
    auth = Auth()
    token = create_access_token(user_id, role, auth_settings)

    if is_authorized:
        payload = await auth(get_request(token))
        assert payload.dict() == get_expected_payload(TokenType.ACCESS, user_id, role, auth_settings.access_token_ttl)
    else:
        with pytest.raises(UnauthorizedError):
            await auth(get_request(token))
