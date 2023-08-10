from ipaddress import IPv4Address

from starlette.requests import Request

from app.config import jwt
from app.user.gateway.rest.auth.errors import LostRefreshTokenError


async def get_remote_ip(request: Request) -> IPv4Address:
    return IPv4Address(request.headers["X-Real-IP"])


async def get_refresh_token_from_cookies(request: Request) -> str:
    token = request.cookies.get(jwt.refresh_token_cookie)

    if not token:
        raise LostRefreshTokenError

    return token
