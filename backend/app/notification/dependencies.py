from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.notification.infrastructure.dao import AlchemyNotificationRepository, AlchemyUserRepository


class NotificationContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        from_package="app.notification", packages=[".api", ".application"], auto_wire=False
    )

    alchemy = providers.DependenciesContainer()

    user_repository = providers.Singleton(AlchemyUserRepository, session_factory=alchemy.session.provider)
    notification_repository = providers.Singleton(
        AlchemyNotificationRepository, session_factory=alchemy.session.provider
    )
