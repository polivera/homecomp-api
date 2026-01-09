from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.context.category.application.commands import DeleteCategoryCommand
from app.context.category.application.dto import DeleteCategoryErrorCode
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/categories")


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Delete a category (soft delete)"""
    logger = app_container.logger
    handler = app_container.get_delete_category_handler()

    logger.info("Delete category request", user_id=user_id, category_id=category_id)

    command = DeleteCategoryCommand(
        user_id=user_id,
        category_id=category_id,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            DeleteCategoryErrorCode.NOT_FOUND: 404,  # Not Found
            DeleteCategoryErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }
        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 404:
            logger.warning("Delete category failed - not found", user_id=user_id, category_id=category_id)
        elif status_code == 500:
            logger.error(
                "Delete category failed - server error",
                user_id=user_id,
                category_id=category_id,
                error_code=result.error_code.value,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    logger.info("Category deleted successfully", user_id=user_id, category_id=category_id)
