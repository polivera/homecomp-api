from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.contracts import ListUserHouseholdsHandlerContract
from app.context.household.application.queries import ListUserHouseholdsQuery
from app.context.household.infrastructure.dependencies import (
    get_list_user_households_handler,
)
from app.context.household.interface.schemas import HouseholdResponse, ListHouseholdsResponse
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.get("/", response_model=ListHouseholdsResponse)
async def list_user_households(
    handler: Annotated[ListUserHouseholdsHandlerContract, Depends(get_list_user_households_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """List all households for the authenticated user"""
    query = ListUserHouseholdsQuery(user_id=user_id)

    result = await handler.handle(query)

    # Check for errors
    if result.error_code:
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

    return ListHouseholdsResponse(households=households)
