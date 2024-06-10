from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from result import Err

from app.notification.api.rest.v1.schemas import NewNotificationCountOut, NotificationOut, ReadNotificationBody
from app.notification.application import services
from app.notification.application.dao import INotificationRepository, IUserRepository
from app.notification.application.errors import NotFoundUser
from app.notification.dependencies import NotificationContainer
from app.notification.domain.notification import NotificationID
from app.shared.api import responses
from app.shared.api.errors import NotFound, UnprocessableEntity
from app.shared.api.headers import AuthorizedUserDep
from app.shared.api.schemas import OKSchema
from app.shared.domain.user import UserID


router = APIRouter()


@router.get(
    "/notifications",
    summary="Получить уведомления для авторизованного пользователя",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND,
)
@inject
async def get_notifications(
    authorized_user: AuthorizedUserDep,
    user_repository: IUserRepository = Depends(Provide[NotificationContainer.user_repository]),
    notification_repository: INotificationRepository = Depends(Provide[NotificationContainer.notification_repository]),
) -> list[NotificationOut]:
    try:
        user_id = UserID(authorized_user.id)
    except ValueError as error:
        raise UnprocessableEntity(str(error))

    user = await user_repository.get(user_id)

    if not user:
        raise NotFound(f"Не найден пользователь id={user_id.value}")

    notifications_out = [
        NotificationOut.from_model(user, notification)
        async for notification in notification_repository.all_by_user_id(user_id)
    ]
    notifications_out.sort(key=lambda x: (x.is_read, -x.created_at.timestamp()))

    return notifications_out


@router.get(
    "/notifications/count",
    summary="Количество непрочитанных уведомлений пользователя",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_new_notification_count(
    authorized_user: AuthorizedUserDep,
    user_repository: IUserRepository = Depends(Provide[NotificationContainer.user_repository]),
    notification_repository: INotificationRepository = Depends(Provide[NotificationContainer.notification_repository]),
) -> NewNotificationCountOut:
    user_id = UserID(authorized_user.id)

    if not (user := await user_repository.get(user_id)):
        raise NotFound(f"Не найден пользователь id={user_id.value}")

    notifications = notification_repository.all_by_user_id(user_id)

    return await NewNotificationCountOut.from_model(user, notifications)


@router.post(
    "/notifications/read",
    summary="Прочитать уведомления авторизованного пользователя",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND,
)
@inject
async def read_notifications(
    body: Annotated[ReadNotificationBody, Body()],
    authorized_user: AuthorizedUserDep,
    user_repository: IUserRepository = Depends(Provide[NotificationContainer.user_repository]),
    notification_repository: INotificationRepository = Depends(Provide[NotificationContainer.notification_repository]),
) -> OKSchema:
    try:
        user_id = UserID(authorized_user.id)
        notification_ids = {NotificationID(id_) for id_ in body.ids}
    except ValueError as error:
        raise UnprocessableEntity(str(error))

    result = await services.read_notifications(
        user_id=user_id,
        notification_ids=notification_ids,
        user_repository=user_repository,
        notification_repository=notification_repository,
    )

    match result:
        case Err(NotFoundUser()):
            raise NotFound(f"Не найден пользователь id={user_id.value}")

    return OKSchema()
