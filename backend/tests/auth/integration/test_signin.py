from datetime import timedelta

import freezegun
import jwt
import pytest
from httpx import AsyncClient, Response

from app.config import JWTSettings
from app.users.db.sqlalchemy.models import User
from app.users.domain.entities import Role
from tests.auth.conftest import ACTUAL_PASSWORD, LOGIN, OLD_PASSWORD, PREFIX, TokenType, get_expected_payload
from tests.responses import UNAUTHORIZED
from tests.utils import get_set_cookies


pytestmark = [pytest.mark.integration]

URL = PREFIX + "/signin"


@pytest.mark.parametrize(
    ["login", "password", "expected_authenticated"],
    [
        [LOGIN, ACTUAL_PASSWORD, True],
        [LOGIN, OLD_PASSWORD, False],
        [LOGIN, "incorrect password", False],
        ["unknown login", ACTUAL_PASSWORD, False],
    ],
    ids=[
        "correct credentials",
        "password was changed by user",
        "incorrect password",
        "unknown login",
    ],
)
@freezegun.freeze_time()
async def test_signin(
    client: AsyncClient,
    user: User,
    auth_settings: JWTSettings,
    login: str,
    password: str,
    expected_authenticated: bool,
):
    response = await client.post(URL, json={"login": login, "password": password})

    if expected_authenticated:
        assert_complete_authentication(response, user, auth_settings)
    else:
        assert_bad_credentials(response)


def assert_complete_authentication(
    response: Response,
    user: User,
    auth_settings: JWTSettings,
):
    assert response.status_code == 200
    assert_payload_contains_valid_access_token(response, user, auth_settings.access_token_ttl)
    assert_response_contains_cookie_with_refresh_token(response, user, auth_settings.refresh_token_ttl)


def assert_payload_contains_valid_access_token(
    response: Response, user: User, ttl: timedelta, field_name: str = "accessToken"
):
    body: dict = response.json()
    assert list(body.keys()) == [field_name]
    validate_token(body[field_name], TokenType.ACCESS, user.id, user.role, ttl)


def assert_response_contains_cookie_with_refresh_token(
    response: Response, user: User, ttl: timedelta, cookie_name: str = "refresh_token"
):
    cookies = get_set_cookies(response.headers)

    assert cookie_name in cookies
    validate_token(cookies[cookie_name], TokenType.REFRESH, user.id, user.role, ttl)


def validate_token(
    token: str, expected_type: TokenType, expected_user_id, expected_user_role: Role, expected_ttl: timedelta
):
    payload = jwt.decode(token, options={"verify_signature": False})
    assert payload == get_expected_payload(expected_type, expected_user_id, expected_user_role, expected_ttl)


def assert_bad_credentials(response: Response):
    assert response.status_code == 401
    assert response.json() == UNAUTHORIZED
