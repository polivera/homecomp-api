from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.category.application.commands import CreateCategoryCommand
from app.context.category.application.dto import CreateCategoryErrorCode
from app.context.category.interface.rest.schemas import CreateCategoryRequest, CreateCategoryResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/categories")


@router.post("", response_model=CreateCategoryResponse, status_code=201)
async def create_category(
    request: CreateCategoryRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Create a new category"""
    logger = app_container.logger
    handler = app_container.get_create_category_handler()

    logger.info("Create category request", user_id=user_id, name=request.name, color=request.color)

    command = CreateCategoryCommand(
        user_id=user_id,
        name=request.name,
        color=request.color,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            CreateCategoryErrorCode.NAME_ALREADY_EXISTS: 409,  # Conflict
            CreateCategoryErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            CreateCategoryErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }
        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 409:
            logger.warning("Create category failed - name conflict", user_id=user_id, name=request.name)
        elif status_code == 500:
            logger.error(
                "Create category failed - server error", user_id=user_id, error_code=result.error_code.value
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    if result.category_id is None:
        logger.error("Create category failed - missing ID", user_id=user_id)
        raise HTTPException(status_code=500, detail="category id is not present")

    logger.info(
        "Category created successfully", user_id=user_id, category_id=result.category_id, name=request.name
    )

    return CreateCategoryResponse(
        category_id=result.category_id,
        name=request.name,
        color=request.color,
    )
