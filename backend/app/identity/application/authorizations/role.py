import re
from functools import lru_cache

from app.identity.application.authorizations.abc import IAuthorization
from app.identity.domain.jwt import Payload
from app.identity.domain.rest import Method
from app.identity.domain.user import Role


class RoleAuthorization(IAuthorization):
    _ENDPOINTS = {
        "/mobile/v1/feedbacks": {
            Method.POST: {Role.PARENT},
        },
        "/mobile/v1/pupils": {
            Method.GET: {Role.PARENT},
        },
        "/mobile/v1/pupils/{pupil_id}": {
            Method.GET: {Role.PARENT},
        },
        "/mobile/v1/pupils/{pupil_id}/resume": {
            Method.POST: {Role.PARENT},
        },
        "/mobile/v1/pupils/{pupil_id}/cancel": {
            Method.POST: {Role.PARENT},
        },
        "/mobile/v1/pupils/{pupil_id}/mealtimes": {
            Method.PATCH: {Role.PARENT},
        },
        "/mobile/v1/pupils/{pupil_id}/attach": {
            Method.POST: {Role.PARENT},
        },
        "/web/v1/school-classes/{class_id}/requests/prefill": {
            Method.GET: {Role.TEACHER},
        },
        "/web/v1/portions": {
            Method.GET: {Role.STAFF},
        },
        "/web/v1/school-classes/{class_id}/requests": {
            Method.POST: {Role.TEACHER},
        },
        "/web/v1/school-classes": {
            Method.GET: {Role.TEACHER},
        },
    }

    def authorize(self, payload: Payload, uri: str, method: Method) -> bool:
        pattern = self._make_pattern(uri)

        for endpoint, methods in self._ENDPOINTS.items():
            if not pattern.match(endpoint):
                continue

            return payload.role in methods.get(method, set())

        return False

    @lru_cache
    def _make_pattern(self, uri: str) -> re.Pattern[str]:
        query_pattern = r"(\?.*)?"
        path_pattern = uri.replace("{", "(?P<").replace("}", ">[^/]+)")
        pattern = f"^{path_pattern}{query_pattern}$"
        return re.compile(pattern)
