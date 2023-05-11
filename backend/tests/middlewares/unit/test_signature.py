import hmac
import json
from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import SecretStr

from app.config import RequestSignatureSettings
from app.middlewares import RequestSignatureMiddleware


pytestmark = [pytest.mark.unit]


async def test_correct_verification(middleware: RequestSignatureMiddleware, request_: Mock):
    call_next = AsyncMock()
    await middleware.dispatch(request_, call_next)

    call_next.assert_called_once()


async def test_wrong_signature_processing(
    middleware: RequestSignatureMiddleware, request_: Mock, settings: RequestSignatureSettings
):
    request_.headers[settings.signature_header] = "wrong signature"

    call_next = Mock()
    response = await middleware.dispatch(request_, call_next)

    assert response.status_code == 400
    assert json.loads(response.body) == {"msg": "The request signature is wrong or destroyed"}
    call_next.assert_not_called()


async def test_debug_mode(middleware: RequestSignatureMiddleware):
    middleware._settings.debug = True
    call_next = AsyncMock()
    await middleware.dispatch(Mock(), call_next)

    call_next.assert_called_once()


@pytest.fixture
def middleware(settings: RequestSignatureSettings) -> RequestSignatureMiddleware:
    return RequestSignatureMiddleware(AsyncMock(), settings)


@pytest.fixture
def request_(settings: RequestSignatureSettings) -> Mock:
    request = Mock()
    request.method = "POST"
    request.url = "http://localhost:8000/collection"
    request.query_params = {
        "param_1": "value_1",
        "param_2": "value_2",
    }
    request.headers = {
        "header_1": "value_1",
        "header_2": "value_2",
    }

    msg = b"""POST
http://localhost:8000/collection
param_1=value_1param_2=value_2
header_1=value_1header_2=value_2"""
    signature = hmac.new(
        settings.secret.get_secret_value().encode(settings.encoding), msg, settings.digest_mod
    ).hexdigest()
    request.headers[settings.signature_header] = signature

    return request


@pytest.fixture
def settings() -> RequestSignatureSettings:
    return RequestSignatureSettings(
        _env_file=None,
        secret=SecretStr("secret"),
        signature_header="X-Signature",
        encoding="utf-8",
        digest_mod="sha256",
        debug=False,
    )
