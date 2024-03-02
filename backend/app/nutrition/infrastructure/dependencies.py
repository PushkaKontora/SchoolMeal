from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.nutrition.infrastructure.api import NutritionAPI
from app.nutrition.infrastructure.dao import AlchemyPupilDAO, AlchemyRequestDAO, AlchemySchoolClassDAO


class NutritionContainer(DeclarativeContainer):
    alchemy = providers.DependenciesContainer()

    pupil_dao = providers.Singleton(AlchemyPupilDAO, session_factory=alchemy.session.provider)
    school_class_dao = providers.Singleton(AlchemySchoolClassDAO, session_factory=alchemy.session.provider)
    request_dao = providers.Singleton(AlchemyRequestDAO, session_factory=alchemy.session.provider)

    api = providers.Singleton(
        NutritionAPI, pupil_dao=pupil_dao, school_class_dao=school_class_dao, request_dao=request_dao
    )
