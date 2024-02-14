from pathlib import Path

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Dependency, Factory, Singleton
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition import application
from app.nutrition.infrastructure.dao import AlchemyPupilDAO, AlchemyRequestDAO, AlchemySchoolClassDAO
from app.shared.objects_storage.local import LocalObjectsStorage


class NutritionContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[application])

    object_storage_config = Configuration(strict=True)

    session = Dependency(instance_of=AsyncSession)

    objects_storage = Singleton(
        LocalObjectsStorage,
        base_path=Factory(Path, object_storage_config.base_path),
    )

    pupil_dao = Singleton(AlchemyPupilDAO, session_factory=session.provider)
    school_class_dao = Singleton(AlchemySchoolClassDAO, session_factory=session.provider)
    request_dao = Singleton(AlchemyRequestDAO, session_factory=session.provider)
