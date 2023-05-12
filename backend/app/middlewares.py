import hmac

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from app.config import RequestSignatureSettings


class RequestSignatureMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, settings: RequestSignatureSettings):
        super().__init__(app)
        self._settings = settings

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if self._verify(request):
            return await call_next(request)

        return JSONResponse(content={"msg": "The request signature is wrong or destroyed"}, status_code=400)

    def _verify(self, request: Request) -> bool:
        actual = request.headers.get(self._settings.signature_header)
        expected = hmac.new(
            key=self._settings.secret.get_secret_value().encode(self._settings.encoding),
            msg=self._get_message(request),
            digestmod=self._settings.digest_mod,
        ).hexdigest()

        return actual == expected

    def _get_message(self, request: Request) -> bytes:
        query_params = "".join(f"{k}={v}" for k, v in request.query_params.items())
        headers = "".join(f"{k}={v}" for k, v in request.headers.items() if k != self._settings.signature_header)

        return "\n".join(map(str, [request.method, request.url, query_params, headers])).encode(self._settings.encoding)
