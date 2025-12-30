from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.contracts import ListUserHouseholdsHandlerContract
from app.context.household.application.queries import ListUserHouseholdsQuery
from app.context.household.infrastructure.dependencies import (
    get_list_user_households_handler,
)
from app.context.household.interface.schemas import HouseholdResponse, ListHouseholdsResponse
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.get("/", response_model=ListHouseholdsResponse)
async def list_user_households(
    handler: Annotated[ListUserHouseholdsHandlerContract, Depends(get_list_user_households_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    """List all households for the authenticated user"""

    logger.info("List user households request", user_id=user_id)

    query = ListUserHouseholdsQuery(user_id=user_id)

    result = await handler.handle(query)

    # Check for errors
    if result.error_code:
        logger.error("List user households failed", user_id=user_id)
        raise HTTPException(status_code=500, detail=result.error_message)

    # Convert summaries to response objects
    households = [
        HouseholdResponse(
            id=h.household_id,
            name=h.household_name,
            owner_user_id=h.owner_user_id,
            created_at=h.created_at,
        )
        for h in (result.households if result.households else [])
    ]

    logger.info("User households retrieved successfully", user_id=user_id, count=len(households))
    return ListHouseholdsResponse(households=households)
