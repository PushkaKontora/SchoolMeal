from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.structure.infrastructure.dao.parents import AlchemyParentRepository
from app.structure.infrastructure.dao.pupils import AlchemyPupilRepository
from app.structure.infrastructure.dao.school import AlchemySchoolDAO
from app.structure.infrastructure.dao.school_classes import AlchemySchoolClassRepository


class StructureContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(from_package="app.structure", packages=[".api"])

    alchemy = providers.DependenciesContainer()

    pupil_repository = providers.Singleton(AlchemyPupilRepository, session_factory=alchemy.session.provider)
    parent_repository = providers.Singleton(AlchemyParentRepository, session_factory=alchemy.session.provider)
    class_repository = providers.Singleton(AlchemySchoolClassRepository, session_factory=alchemy.session.provider)
    school_dao = providers.Singleton(AlchemySchoolDAO, session_factory=alchemy.session.provider)
