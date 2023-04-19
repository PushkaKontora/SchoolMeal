from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

from app.auth.domain.entities import JWTPayload
from app.auth.domain.services import JWTService
from app.auth.presentation.exceptions import InvalidBearerCredentialsException, UnauthorizedException


class JWTAuth:
    def __init__(self, jwt_service: JWTService, header: str = "Authorization", scheme: str = "Bearer"):
        self._jwt_service = jwt_service
        self._header = header
        self._scheme = scheme

    async def __call__(self, request: Request) -> JWTPayload:
        authorization = request.headers.get(self._header)
        scheme, access_token = get_authorization_scheme_param(authorization)

        if not (authorization and scheme and access_token) or scheme.lower() != self._scheme.lower():
            raise InvalidBearerCredentialsException

        payload = self._jwt_service.decode_access_token(access_token)

        if not self.authorize(payload):
            raise UnauthorizedException

        return payload

    def authorize(self, payload: JWTPayload) -> bool:
        return True
