from datetime import date
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from app.nutrition.api.dto import CancellationPeriodIn, Mealtimes
from app.nutrition.application.commands.attach_child_to_parent import (
    AttachChildToParentCommand,
    AttachChildToParentCommandHandler,
)
from app.nutrition.application.commands.cancel_nutrition import CancelNutritionCommand, CancelNutritionCommandHandler
from app.nutrition.application.commands.resume_nutrition import ResumeNutritionCommand, ResumeNutritionCommandHandler
from app.nutrition.application.commands.update_mealtimes import UpdateMealtimesCommand, UpdateMealtimesCommandHandler
from app.nutrition.application.dto import CancellationPeriodOut
from app.nutrition.application.queries.get_children import ChildOut, GetChildrenQuery, GetChildrenQueryExecutor
from app.nutrition.application.queries.get_menu_on_date import GetMenuOnDateQuery, GetMenuOnDateQueryExecutor, MenuOut
from app.nutrition.application.queries.get_nutrition_info import (
    GetNutritionInfoQuery,
    GetNutritionInfoQueryExecutor,
    NutritionOut,
)
from app.nutrition.application.queries.get_school_classes import (
    GetSchoolClassesQuery,
    GetSchoolClassesQueryExecutor,
    SchoolClassOut,
)
from app.nutrition.application.repositories import NotFoundMenu, NotFoundParent, NotFoundPupil
from app.nutrition.domain.parent import ChildIsAlreadyAttachedToParent
from app.nutrition.domain.periods import (
    EndCannotBeGreaterThanStart,
    ExceededMaxLengthReason,
    SpecifiedReasonCannotBeEmpty,
)
from app.nutrition.domain.pupil import CannotCancelNutritionAfterTime, CannotResumeNutritionAfterTime
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.fastapi import responses
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.errors import BadRequestError, NotFoundError
from app.shared.fastapi.schemas import OKSchema


router = APIRouter(tags=["Питание"])


@router.get(
    "/nutrition/{pupil_id}",
    summary="Получить информацию о питании ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
@inject
async def get_pupil_nutrition(
    pupil_id: str,
    executor: GetNutritionInfoQueryExecutor = Depends(Provide[NutritionContainer.get_nutrition_info_executor]),
) -> NutritionOut:
    try:
        return await executor.execute(query=GetNutritionInfoQuery(pupil_id=pupil_id))
    except NotFoundPupil as error:
        raise NotFoundError("Ученик не был найден") from error


@router.put(
    "/nutrition/{pupil_id}/plan",
    summary="Изменить план приёма пищи",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
@inject
async def change_plan(
    pupil_id: str,
    plan: Mealtimes,
    handler: UpdateMealtimesCommandHandler = Depends(Provide[NutritionContainer.change_plan_command_handler]),
) -> OKSchema:
    try:
        await handler.handle(
            command=UpdateMealtimesCommand(
                pupil_id=pupil_id,
                has_breakfast=plan.has_breakfast,
                has_dinner=plan.has_dinner,
                has_snacks=plan.has_snacks,
            )
        )

    except NotFoundPupil as error:
        raise NotFoundError("Ученик не найден") from error

    return OKSchema()


@router.post(
    "/nutrition/{pupil_id}/cancel",
    summary="Снять ребёнка с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
@inject
async def cancel_nutrition(
    pupil_id: str,
    period_in: CancellationPeriodIn,
    handler: CancelNutritionCommandHandler = Depends(Provide[NutritionContainer.cancel_nutrition_command_handler]),
) -> list[CancellationPeriodOut]:
    try:
        return await handler.handle(
            command=CancelNutritionCommand(
                pupil_id=pupil_id,
                starts_at=period_in.starts_at,
                ends_at=period_in.ends_at,
                reason=period_in.reason,
            )
        )

    except NotFoundPupil as error:
        raise NotFoundError("Ученик не найден") from error

    except SpecifiedReasonCannotBeEmpty as error:
        raise BadRequestError("Текст указанной причины должен содержать хотя бы один символ") from error

    except ExceededMaxLengthReason as error:
        raise BadRequestError("Превышена максимальная длина причины") from error

    except EndCannotBeGreaterThanStart as error:
        raise BadRequestError("Дата начала периода больше, чем конечная дата") from error

    except CannotCancelNutritionAfterTime as error:
        raise BadRequestError(f"Запрещено после {error.completed_at} снимать с питания") from error


@router.post(
    "/nutrition/{pupil_id}/resume",
    summary="Поставить ребёнка на питание в дату",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
@inject
async def resume_nutrition(
    pupil_id: str,
    date_in: Annotated[date, Body(embed=True, alias="date")],
    handler: ResumeNutritionCommandHandler = Depends(Provide[NutritionContainer.resume_nutrition_command_handler]),
) -> list[CancellationPeriodOut]:
    try:
        return await handler.handle(command=ResumeNutritionCommand(pupil_id=pupil_id, day=date_in))

    except NotFoundPupil as error:
        raise NotFoundError("Ученик не найден") from error

    except CannotResumeNutritionAfterTime as error:
        raise BadRequestError(f"Запрещено после {error.completed_at} ставить на питание") from error


@router.post(
    "/children/{child_id}",
    summary="Закрепить ученика за родителем",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
@inject
async def attach_child_to_parent(
    child_id: str,
    user: AuthorizedUserDep,
    handler: AttachChildToParentCommandHandler = Depends(
        Provide[NutritionContainer.attach_child_to_parent_command_handler]
    ),
) -> OKSchema:
    try:
        await handler.handle(command=AttachChildToParentCommand(parent_id=user.id, pupil_id=child_id))

    except NotFoundParent as error:
        raise BadRequestError("Родитель не зарегистрирован") from error

    except NotFoundPupil as error:
        raise NotFoundError("Ребёнка не существует") from error

    except ChildIsAlreadyAttachedToParent as error:
        raise BadRequestError("Ребёнок уже привязан к родителю") from error

    return OKSchema()


@router.get(
    "/children",
    summary="Получить список детей",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_children(
    user: AuthorizedUserDep,
    executor: GetChildrenQueryExecutor = Depends(Provide[NutritionContainer.get_children_query_executor]),
) -> list[ChildOut]:
    return await executor.execute(query=GetChildrenQuery(parent_id=user.id))


@router.get("/school-classes", summary="Получить информацию о классах", status_code=status.HTTP_200_OK)
@inject
async def get_school_classes(
    query: GetSchoolClassesQuery = Depends(),
    executor: GetSchoolClassesQueryExecutor = Depends(Provide[NutritionContainer.get_school_classes_executor]),
) -> list[SchoolClassOut]:
    return await executor.execute(query)


@router.get("/menu", summary="Получить меню на дату", status_code=status.HTTP_200_OK, responses=responses.NOT_FOUND)
@inject
async def get_menu_on_date(
    query: GetMenuOnDateQuery = Depends(),
    executor: GetMenuOnDateQueryExecutor = Depends(Provide[NutritionContainer.get_menus_query_executor]),
) -> MenuOut:
    try:
        return await executor.execute(query)
    except NotFoundMenu as error:
        raise NotFoundError(f"Не найдено меню на дату {query.on_date}") from error
