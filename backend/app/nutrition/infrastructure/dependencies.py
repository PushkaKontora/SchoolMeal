from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.nutrition import api
from app.nutrition.infrastructure.dao.parent_repositories import AlchemyParentRepository
from app.nutrition.infrastructure.dao.pupil_repositories import AlchemyPupilRepository
from app.nutrition.infrastructure.dao.request_repositories import AlchemyRequestRepository
from app.nutrition.infrastructure.dao.school_class_repositories import AlchemySchoolClassRepository


class NutritionContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[api], auto_wire=False)

    alchemy = providers.DependenciesContainer()

    pupil_repository = providers.Singleton(AlchemyPupilRepository, session_factory=alchemy.session.provider)
    class_repository = providers.Singleton(AlchemySchoolClassRepository, session_factory=alchemy.session.provider)
    request_repository = providers.Singleton(AlchemyRequestRepository, session_factory=alchemy.session.provider)
    parent_repository = providers.Singleton(AlchemyParentRepository, session_factory=alchemy.session.provider)
