from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.gateway.dependencies import get_db_session
from app.user.application.repositories import IUserRepository
from app.user.application.services import UserService
from app.user.infrastructure.db.repositories import UserRepository


def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> IUserRepository:
    return UserRepository(session)


def get_user_service(user_repository: IUserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)
