from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import CreateHouseholdCommand
from app.context.household.application.contracts import CreateHouseholdHandlerContract
from app.context.household.application.dto import CreateHouseholdErrorCode
from app.context.household.infrastructure.dependencies import (
    get_create_household_handler,
)
from app.context.household.interface.schemas import (
    CreateHouseholdRequest,
    CreateHouseholdResponse,
)
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.post("/", status_code=201)
async def create_household(
    request: CreateHouseholdRequest,
    handler: CreateHouseholdHandlerContract = Depends(get_create_household_handler),
    user_id: int = Depends(get_current_user_id),
) -> CreateHouseholdResponse:
    """Create a new household"""

    command = CreateHouseholdCommand(
        user_id=user_id,
        name=request.name,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        # Map error codes to status codes
        status_code_map = {
            CreateHouseholdErrorCode.NAME_ALREADY_EXISTS: 409,  # Conflict
            CreateHouseholdErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            CreateHouseholdErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)
    elif not result.household_id or not result.household_name:
        raise HTTPException(status_code=500, detail="unexpected server error")

    # Return success response
    return CreateHouseholdResponse(
        id=result.household_id,
        name=result.household_name,
    )
