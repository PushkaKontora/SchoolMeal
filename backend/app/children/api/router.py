from fastapi import APIRouter, status

from app.children.api.dependencies import ChildrenRepositoryDep, ParentsRepositoryDep
from app.children.api.schemas import ChildOut
from app.children.application import use_cases
from app.children.application.repositories import NotFoundChild, NotFoundParent
from app.children.domain.parent import ChildIsAlreadyAssignedToParent
from app.shared.fastapi import responses
from app.shared.fastapi.dependencies.db import SessionDep
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.errors import BadRequestError, NotFoundError
from app.shared.fastapi.schemas import OKSchema


router = APIRouter(tags=["Родители и дети"])


@router.post(
    "/children/{child_id}",
    summary="Закрепить ученика за родителем",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
async def assign_pupil_to_parent(
    child_id: str,
    user: AuthorizedUserDep,
    session: SessionDep,
    parents_repository: ParentsRepositoryDep,
    children_repository: ChildrenRepositoryDep,
) -> OKSchema:
    try:
        async with session.begin():
            await use_cases.add_child_to_parent(
                parent_id=user.id,
                child_id=child_id,
                parents_repository=parents_repository,
                children_repository=children_repository,
            )
            await session.commit()

    except NotFoundParent as error:
        raise BadRequestError("Родитель не зарегистрирован") from error

    except NotFoundChild as error:
        raise NotFoundError("Ребёнка не существует") from error

    except ChildIsAlreadyAssignedToParent as error:
        raise BadRequestError("Ребёнок уже привязан к родителю") from error

    return OKSchema()


@router.get(
    "/children",
    summary="Получить список детей",
    status_code=status.HTTP_200_OK,
)
async def get_children(
    user: AuthorizedUserDep, parents_repository: ParentsRepositoryDep, children_repository: ChildrenRepositoryDep
) -> list[ChildOut]:
    try:
        children = await use_cases.get_children(
            parent_id=user.id, parents_repository=parents_repository, children_repository=children_repository
        )

    except NotFoundParent as error:
        raise BadRequestError("Родитель не зарегистрирован") from error

    return [ChildOut.from_model(child) for child in children]
