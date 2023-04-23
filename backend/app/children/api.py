from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from app.auth.presentation.middlewares import JWTAuth
from app.children.domain.services import ChildService
from app.children.presentation.handlers import ChildrenHandlers
from app.children.presentation.routers import ChildrenRouter


class ChildrenAPI(DeclarativeContainer):
    jwt_auth = Dependency(instance_of=JWTAuth)

    child_service = Factory(ChildService)

    children_handlers = Factory(ChildrenHandlers, child_service=child_service)

    router = Factory(ChildrenRouter, children_handlers=children_handlers, jwt_auth=jwt_auth)
