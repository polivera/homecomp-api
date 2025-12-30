from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import DeleteHouseholdCommand
from app.context.household.application.contracts import DeleteHouseholdHandlerContract
from app.context.household.application.dto import DeleteHouseholdErrorCode
from app.context.household.infrastructure.dependencies import get_delete_household_handler
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.delete("/{household_id}", status_code=204)
async def delete_household(
    household_id: int,
    handler: Annotated[DeleteHouseholdHandlerContract, Depends(get_delete_household_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Soft delete household (owner only)"""
    command = DeleteHouseholdCommand(
        household_id=household_id,
        user_id=user_id,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            DeleteHouseholdErrorCode.NOT_FOUND: 404,
            DeleteHouseholdErrorCode.NOT_OWNER: 403,
            DeleteHouseholdErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return 204 No Content on success
    return
