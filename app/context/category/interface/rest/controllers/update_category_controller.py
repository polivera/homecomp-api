from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.category.application.commands import UpdateCategoryCommand
from app.context.category.application.dto import UpdateCategoryErrorCode
from app.context.category.interface.rest.schemas import UpdateCategoryRequest, UpdateCategoryResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/categories")


@router.put("/{category_id}", response_model=UpdateCategoryResponse, status_code=200)
async def update_category(
    category_id: int,
    request: UpdateCategoryRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Update an existing category"""
    logger = app_container.logger
    handler = app_container.get_update_category_handler()

    logger.info(
        "Update category request", user_id=user_id, category_id=category_id, name=request.name, color=request.color
    )

    command = UpdateCategoryCommand(
        user_id=user_id,
        category_id=category_id,
        name=request.name,
        color=request.color,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            UpdateCategoryErrorCode.NOT_FOUND: 404,  # Not Found
            UpdateCategoryErrorCode.NAME_ALREADY_EXISTS: 409,  # Conflict
            UpdateCategoryErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            UpdateCategoryErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }
        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 404:
            logger.warning("Update category failed - not found", user_id=user_id, category_id=category_id)
        elif status_code == 409:
            logger.warning("Update category failed - name conflict", user_id=user_id, category_id=category_id)
        elif status_code == 500:
            logger.error(
                "Update category failed - server error",
                user_id=user_id,
                category_id=category_id,
                error_code=result.error_code.value,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    if result.category_id is None:
        logger.error("Update category failed - missing ID", user_id=user_id, category_id=category_id)
        raise HTTPException(status_code=500, detail="category id is not present")

    logger.info(
        "Category updated successfully", user_id=user_id, category_id=result.category_id, name=request.name
    )

    return UpdateCategoryResponse(
        category_id=result.category_id,
        name=request.name,
        color=request.color,
    )
