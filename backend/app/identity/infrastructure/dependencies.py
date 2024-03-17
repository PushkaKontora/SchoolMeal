from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.identity.application.authorizations.role import RoleAuthorization
from app.identity.infrastructure.config import JWTConfig
from app.identity.infrastructure.dao import AlchemySessionRepository, AlchemyUserRepository


class IdentityContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(from_package="app.identity", packages=[".api", ".application"], auto_wire=False)

    alchemy = providers.DependenciesContainer()

    jwt_config = providers.Singleton(JWTConfig)

    authorization = providers.Singleton(RoleAuthorization)

    user_repository = providers.Singleton(AlchemyUserRepository, session_factory=alchemy.session.provider)
    session_repository = providers.Singleton(AlchemySessionRepository, session_factory=alchemy.session.provider)
