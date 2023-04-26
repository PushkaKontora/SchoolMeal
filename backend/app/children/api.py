from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from app.auth.presentation.middlewares import JWTAuth
from app.children.domain.services import ChildService
from app.children.presentation.handlers import ChildHandlers, ChildrenHandlers
from app.children.presentation.routers import ChildrenRouter, ChildRouter


class ChildrenAPI(DeclarativeContainer):
    jwt_auth = Dependency(instance_of=JWTAuth)

    child_service = Factory(ChildService)

    child_handlers = Factory(ChildHandlers, child_service=child_service)
    children_handlers = Factory(ChildrenHandlers, child_service=child_service)

    child_router = Factory(ChildRouter, child_handlers=child_handlers)
    router = Factory(ChildrenRouter, children_handlers=children_handlers, child_router=child_router, jwt_auth=jwt_auth)
