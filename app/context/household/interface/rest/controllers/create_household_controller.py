from typing import Annotated

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
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.post("/", status_code=201)
async def create_household(
    request: CreateHouseholdRequest,
    handler: Annotated[CreateHouseholdHandlerContract, Depends(get_create_household_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> CreateHouseholdResponse:
    """Create a new household"""

    logger.info("Create household request", user_id=user_id, name=request.name)

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
        logger.warning("Create household failed", user_id=user_id, error_code=result.error_code.value)
        raise HTTPException(status_code=status_code, detail=result.error_message)
    elif not result.household_id or not result.household_name:
        logger.error("Create household failed - missing data", user_id=user_id)
        raise HTTPException(status_code=500, detail="unexpected server error")

    # Return success response
    logger.info("Household created successfully", user_id=user_id, household_id=result.household_id)
    return CreateHouseholdResponse(
        id=result.household_id,
        name=result.household_name,
    )
