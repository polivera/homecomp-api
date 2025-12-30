from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.contracts import GetHouseholdHandlerContract
from app.context.household.application.dto import GetHouseholdErrorCode
from app.context.household.application.queries import GetHouseholdQuery
from app.context.household.infrastructure.dependencies import get_get_household_handler
from app.context.household.interface.schemas import HouseholdResponse
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.get("/{household_id}", response_model=HouseholdResponse)
async def get_household(
    household_id: int,
    handler: Annotated[GetHouseholdHandlerContract, Depends(get_get_household_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    """Get household by ID (owner or active member only)"""

    logger.info("Get household request", household_id=household_id, user_id=user_id)

    query = GetHouseholdQuery(household_id=household_id, user_id=user_id)

    result = await handler.handle(query)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            GetHouseholdErrorCode.NOT_FOUND: 404,
            GetHouseholdErrorCode.UNAUTHORIZED_ACCESS: 403,
            GetHouseholdErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        logger.warning("Get household failed", household_id=household_id, error_code=result.error_code.value)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    logger.info("Household retrieved successfully", household_id=household_id, user_id=user_id)
    return HouseholdResponse(
        id=result.household_id,
        name=result.household_name,
        owner_user_id=result.owner_user_id,
        created_at=result.created_at,
    )
