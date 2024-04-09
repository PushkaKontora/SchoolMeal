from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.user_management.application.authorizations.role import RoleAuthorization
from app.user_management.application.limiters import BruteForceLimiter
from app.user_management.infrastructure.config import Config
from app.user_management.infrastructure.dao import AlchemySessionRepository, AlchemyUserRepository


class IdentityContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        from_package="app.user_management", packages=[".api", ".application"], auto_wire=False
    )

    alchemy = providers.DependenciesContainer()

    config = providers.Singleton(Config)

    authorization = providers.Singleton(RoleAuthorization)
    limiter = providers.Singleton(BruteForceLimiter)

    user_repository = providers.Singleton(AlchemyUserRepository, session_factory=alchemy.session.provider)
    session_repository = providers.Singleton(AlchemySessionRepository, session_factory=alchemy.session.provider)
