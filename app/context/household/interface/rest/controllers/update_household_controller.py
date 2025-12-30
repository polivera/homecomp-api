from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import UpdateHouseholdCommand
from app.context.household.application.contracts import UpdateHouseholdHandlerContract
from app.context.household.application.dto import UpdateHouseholdErrorCode
from app.context.household.infrastructure.dependencies import get_update_household_handler
from app.context.household.interface.schemas import HouseholdResponse, UpdateHouseholdRequest
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.put("/{household_id}", response_model=HouseholdResponse)
async def update_household(
    household_id: int,
    request: UpdateHouseholdRequest,
    handler: Annotated[UpdateHouseholdHandlerContract, Depends(get_update_household_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Update household name (owner only)"""
    command = UpdateHouseholdCommand(
        household_id=household_id,
        user_id=user_id,
        name=request.name,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            UpdateHouseholdErrorCode.NOT_FOUND: 404,
            UpdateHouseholdErrorCode.NOT_OWNER: 403,
            UpdateHouseholdErrorCode.NAME_ALREADY_EXISTS: 409,
            UpdateHouseholdErrorCode.MAPPER_ERROR: 500,
            UpdateHouseholdErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    return HouseholdResponse(
        id=result.household_id,
        name=result.household_name,
        owner_user_id=result.owner_user_id,
        created_at="",  # Not returned from update
    )
