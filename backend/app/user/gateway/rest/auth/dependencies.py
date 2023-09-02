from ipaddress import IPv4Address

from starlette.requests import Request

from app import config
from app.user.gateway.rest.auth.errors import LostRefreshTokenError


async def get_remote_ip(request: Request) -> IPv4Address:
    return IPv4Address(request.headers[config.headers.real_ip_header])


async def get_refresh_token_from_cookies(request: Request) -> str:
    token = request.cookies.get(config.jwt.refresh_cookie)

    if not token:
        raise LostRefreshTokenError

    return token
