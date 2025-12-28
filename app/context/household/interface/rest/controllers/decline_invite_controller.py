from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import DeclineInviteCommand
from app.context.household.application.contracts import DeclineInviteHandlerContract
from app.context.household.application.dto import DeclineInviteErrorCode
from app.context.household.infrastructure.dependencies import get_decline_invite_handler
from app.context.household.interface.schemas import DeclineInviteResponse
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.post("/{household_id}/invites/decline", status_code=200)
async def decline_invite(
    household_id: int,
    handler: DeclineInviteHandlerContract = Depends(get_decline_invite_handler),
    user_id: int = Depends(get_current_user_id),
) -> DeclineInviteResponse:
    """Decline a household invitation"""

    command = DeclineInviteCommand(
        user_id=user_id,
        household_id=household_id,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            DeclineInviteErrorCode.NOT_INVITED: 404,  # Not Found
            DeclineInviteErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    return DeclineInviteResponse(
        success=True,
        message="Invitation declined successfully",
    )
