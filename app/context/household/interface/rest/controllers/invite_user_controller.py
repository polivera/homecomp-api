from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import InviteUserCommand
from app.context.household.application.contracts import InviteUserHandlerContract
from app.context.household.application.dto import InviteUserErrorCode
from app.context.household.infrastructure.dependencies import get_invite_user_handler
from app.context.household.interface.schemas import (
    InviteUserRequest,
    InviteUserResponse,
)
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.post("/{household_id}/invites", status_code=201)
async def invite_user(
    household_id: int,
    request: InviteUserRequest,
    handler: Annotated[InviteUserHandlerContract, Depends(get_invite_user_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> InviteUserResponse:
    """Invite a user to a household"""

    logger.info(
        "Invite user request",
        inviter_user_id=user_id,
        household_id=household_id,
        invitee_user_id=request.invitee_user_id,
    )

    command = InviteUserCommand(
        inviter_user_id=user_id,
        household_id=household_id,
        invitee_user_id=request.invitee_user_id,
        role=request.role,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            InviteUserErrorCode.ONLY_OWNER_CAN_INVITE: 403,  # Forbidden
            InviteUserErrorCode.ALREADY_ACTIVE_MEMBER: 409,  # Conflict
            InviteUserErrorCode.ALREADY_INVITED: 409,  # Conflict
            InviteUserErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            InviteUserErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)
        logger.warning("Invite user failed", household_id=household_id, error_code=result.error_code.value)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    if not result.member_id:
        logger.error("Invite user failed - missing member ID", household_id=household_id)
        raise HTTPException(status_code=500, detail="Unexpected server error")

    logger.info("User invited successfully", household_id=household_id, invitee_user_id=request.invitee_user_id)
    return InviteUserResponse(
        member_id=result.member_id,
        household_id=result.household_id,
        user_id=result.user_id,
        role=result.role,
    )
