from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.structure.infrastructure.dao.parents import AlchemyParentRepository
from app.structure.infrastructure.dao.pupils import AlchemyPupilRepository


class StructureContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(from_package="app.structure", packages=[".api"])

    alchemy = providers.DependenciesContainer()

    pupil_repository = providers.Singleton(AlchemyPupilRepository, session_factory=alchemy.session.provider)
    parent_repository = providers.Singleton(AlchemyParentRepository, session_factory=alchemy.session.provider)
