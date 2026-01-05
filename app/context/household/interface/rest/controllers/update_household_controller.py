from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import UpdateHouseholdCommand
from app.context.household.application.dto import UpdateHouseholdErrorCode
from app.context.household.interface.schemas import HouseholdResponse, UpdateHouseholdRequest
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.put("/{household_id}", response_model=HouseholdResponse)
async def update_household(
    household_id: int,
    request: UpdateHouseholdRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Update household name (owner only)"""
    logger = app_container.logger
    handler = app_container.get_update_household_handler()

    logger.info("Update household request", household_id=household_id, user_id=user_id, name=request.name)

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
        logger.warning("Update household failed", household_id=household_id, error_code=result.error_code.value)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    logger.info("Household updated successfully", household_id=household_id, user_id=user_id)
    return HouseholdResponse(
        id=result.household_id,
        name=result.household_name,
        owner_user_id=result.owner_user_id,
        created_at="",  # Not returned from update
    )
