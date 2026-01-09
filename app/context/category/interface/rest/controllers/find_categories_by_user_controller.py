from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.category.application.dto import FindCategoriesByUserErrorCode
from app.context.category.application.queries import FindCategoriesByUserQuery
from app.context.category.interface.rest.schemas import CategoryListResponse, CategoryResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/categories")


@router.get("", response_model=CategoryListResponse, status_code=200)
async def find_categories_by_user(
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Find all categories for the current user"""
    logger = app_container.logger
    handler = app_container.get_find_categories_by_user_handler()

    logger.info("Find categories by user request", user_id=user_id)

    query = FindCategoriesByUserQuery(user_id=user_id)

    result = await handler.handle(query)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            FindCategoriesByUserErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }
        status_code = status_code_map.get(result.error_code, 500)

        logger.error(
            "Find categories by user failed - server error",
            user_id=user_id,
            error_code=result.error_code.value,
        )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    if result.categories is None:
        logger.error("Find categories by user failed - missing categories", user_id=user_id)
        raise HTTPException(status_code=500, detail="categories are not present")

    logger.info("Categories found successfully", user_id=user_id, count=len(result.categories))

    # Convert application DTOs to REST response schemas
    categories = [
        CategoryResponse(
            category_id=cat.category_id,
            user_id=cat.user_id,
            name=cat.name,
            color=cat.color,
        )
        for cat in result.categories
    ]

    return CategoryListResponse(categories=categories)
