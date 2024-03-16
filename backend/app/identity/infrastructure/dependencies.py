from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.identity.infrastructure.dao import AlchemySessionRepository, AlchemyUserRepository
from app.identity.infrastructure.env import AuthConfig


class IdentityContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(from_package="app.identity", packages=[".api", ".application"], auto_wire=False)

    alchemy = providers.DependenciesContainer()

    auth_config = providers.Singleton(AuthConfig)

    user_repository = providers.Singleton(AlchemyUserRepository, session_factory=alchemy.session.provider)
    session_repository = providers.Singleton(AlchemySessionRepository, session_factory=alchemy.session.provider)
