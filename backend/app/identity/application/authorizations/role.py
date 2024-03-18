import re
from functools import lru_cache

from app.identity.application.authorizations.abc import IAuthorization
from app.identity.domain.jwt import Payload
from app.identity.domain.rest import Method
from app.identity.domain.user import Role


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
    }

    def authorize(self, payload: Payload, uri: str, method: Method) -> bool:
        for endpoint, methods in self._ENDPOINTS.items():
            if not self._make_pattern(endpoint).match(uri):
                continue

            return payload.role in methods.get(method, set())

        return False

    @lru_cache
    def _make_pattern(self, uri: str) -> re.Pattern[str]:
        query_pattern = r"(\?.*)?"
        path_pattern = uri.replace("{", "(?P<").replace("}", ">[^/]+)")
        pattern = f"^{path_pattern}{query_pattern}$"
        return re.compile(pattern)
