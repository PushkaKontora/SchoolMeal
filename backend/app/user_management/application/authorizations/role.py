import re
from functools import lru_cache

from app.user_management.application.authorizations.abc import IAuthorization
from app.user_management.domain.jwt import AccessToken
from app.user_management.domain.rest import Method
from app.user_management.domain.user import Role


class RoleAuthorization(IAuthorization):
    _ENDPOINTS = {
        "/nutrition/v1/school-classes": {
            Method.GET: {Role.TEACHER},
        },
        "/nutrition/v1/pupils": {
            Method.GET: {Role.PARENT, Role.TEACHER},
        },
        "/nutrition/v1/pupils/{pupil_id}": {
            Method.GET: {Role.PARENT, Role.TEACHER},
        },
        "/nutrition/v1/pupils/{pupil_id}/resume": {
            Method.POST: {Role.PARENT},
        },
        "/nutrition/v1/pupils/{pupil_id}/cancel": {
            Method.POST: {Role.PARENT},
        },
        "/nutrition/v1/mealtimes": {
            Method.PATCH: {Role.PARENT, Role.TEACHER},
        },
        "/nutrition/v1/requests": {
            Method.GET: {Role.TEACHER},
            Method.POST: {Role.TEACHER},
        },
        "/nutrition/v1/requests/prefill": {
            Method.GET: {Role.TEACHER},
        },
        "/nutrition/v1/portions": {
            Method.GET: {Role.STAFF},
        },
        "/feedbacks/v1/feedbacks": {
            Method.POST: {Role.PARENT},
        },
        "/notification/v1/notifications": {
            Method.GET: {Role.TEACHER},
        },
        "/notification/v1/notifications/read": {
            Method.POST: {Role.TEACHER},
        },
    }

    def authorize(self, token: AccessToken, uri: str, method: Method) -> bool:
        for endpoint, methods in self._ENDPOINTS.items():
            if not self._make_pattern(endpoint).match(uri):
                continue

            return token.payload.role in methods.get(method, set())

        return False

    @lru_cache
    def _make_pattern(self, uri: str) -> re.Pattern[str]:
        query_pattern = r"(\?.*)?"
        path_pattern = uri.replace("{", "(?P<").replace("}", ">[^/]+)")
        pattern = f"^{path_pattern}{query_pattern}$"
        return re.compile(pattern)
