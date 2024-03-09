from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.nutrition.infrastructure.dao.pupils import AlchemyPupilRepository
from app.nutrition.infrastructure.dao.requests import AlchemyRequestRepository
from app.nutrition.infrastructure.dao.school_classes import AlchemySchoolClassRepository


class NutritionContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(from_package="app.nutrition", packages=[".application"], auto_wire=False)

    alchemy = providers.DependenciesContainer()

    pupil_repository = providers.Singleton(AlchemyPupilRepository, session_factory=alchemy.session.provider)
    class_repository = providers.Singleton(AlchemySchoolClassRepository, session_factory=alchemy.session.provider)
    request_repository = providers.Singleton(AlchemyRequestRepository, session_factory=alchemy.session.provider)
