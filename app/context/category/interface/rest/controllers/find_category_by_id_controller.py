from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.category.application.dto import FindCategoryByIdErrorCode
from app.context.category.application.queries import FindCategoryByIdQuery
from app.context.category.interface.rest.schemas import CategoryResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/categories")


@router.get("/{category_id}", response_model=CategoryResponse, status_code=200)
async def find_category_by_id(
    category_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Find a category by ID"""
    logger = app_container.logger
    handler = app_container.get_find_category_by_id_handler()

    logger.info("Find category by ID request", user_id=user_id, category_id=category_id)

    query = FindCategoryByIdQuery(
        user_id=user_id,
        category_id=category_id,
    )

    result = await handler.handle(query)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            FindCategoryByIdErrorCode.NOT_FOUND: 404,  # Not Found
            FindCategoryByIdErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }
        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 404:
            logger.warning("Find category by ID failed - not found", user_id=user_id, category_id=category_id)
        elif status_code == 500:
            logger.error(
                "Find category by ID failed - server error",
                user_id=user_id,
                category_id=category_id,
                error_code=result.error_code.value,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    if result.category is None:
        logger.error("Find category by ID failed - missing category", user_id=user_id, category_id=category_id)
        raise HTTPException(status_code=500, detail="category is not present")

    logger.info("Category found successfully", user_id=user_id, category_id=result.category.category_id)

    return CategoryResponse(
        category_id=result.category.category_id,
        user_id=result.category.user_id,
        name=result.category.name,
        color=result.category.color,
    )
