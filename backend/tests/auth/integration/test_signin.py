import freezegun
import pytest
from httpx import AsyncClient

from app.config import JWTSettings
from app.users.db.sqlalchemy.models import User
from tests.auth.conftest import (
    ACTUAL_PASSWORD,
    LOGIN,
    OLD_PASSWORD,
    PREFIX,
    assert_payload_contains_valid_access_token,
    assert_response_contains_cookie_with_refresh_token,
)
from tests.responses import UNAUTHORIZED


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
        assert response.status_code == 200
        assert_payload_contains_valid_access_token(response, user, auth_settings.access_token_ttl)
        assert_response_contains_cookie_with_refresh_token(response, user, auth_settings.refresh_token_ttl)
    else:
        assert response.status_code == 401
        assert response.json() == UNAUTHORIZED
