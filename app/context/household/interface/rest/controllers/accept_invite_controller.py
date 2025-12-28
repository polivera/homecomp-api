from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import AcceptInviteCommand
from app.context.household.application.contracts import AcceptInviteHandlerContract
from app.context.household.application.dto import AcceptInviteErrorCode
from app.context.household.infrastructure.dependencies import get_accept_invite_handler
from app.context.household.interface.schemas import AcceptInviteResponse
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.post("/{household_id}/invites/accept", status_code=200)
async def accept_invite(
    household_id: int,
    handler: AcceptInviteHandlerContract = Depends(get_accept_invite_handler),
    user_id: int = Depends(get_current_user_id),
) -> AcceptInviteResponse:
    """Accept a household invitation"""

    command = AcceptInviteCommand(
        user_id=user_id,
        household_id=household_id,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            AcceptInviteErrorCode.NOT_INVITED: 404,  # Not Found
            AcceptInviteErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            AcceptInviteErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    if not result.member_id:
        raise HTTPException(status_code=500, detail="Unexpected server error")

    return AcceptInviteResponse(
        member_id=result.member_id,
        household_id=result.household_id,
        user_id=result.user_id,
        role=result.role,
    )
