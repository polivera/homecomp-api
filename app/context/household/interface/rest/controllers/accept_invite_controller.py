from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import AcceptInviteCommand
from app.context.household.application.dto import AcceptInviteErrorCode
from app.context.household.interface.schemas import AcceptInviteResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.post("/{household_id}/invites/accept", status_code=200)
async def accept_invite(
    household_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> AcceptInviteResponse:
    """Accept a household invitation"""
    logger = app_container.logger
    handler = app_container.get_accept_invite_handler()

    logger.info("Accept invite request", user_id=user_id, household_id=household_id)

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
        logger.warning("Accept invite failed", household_id=household_id, error_code=result.error_code.value)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    if not result.member_id:
        logger.error("Accept invite failed - missing member ID", household_id=household_id)
        raise HTTPException(status_code=500, detail="Unexpected server error")

    logger.info("Invite accepted successfully", user_id=user_id, household_id=household_id)
    return AcceptInviteResponse(
        member_id=result.member_id,
        household_id=result.household_id,
        user_id=result.user_id,
        role=result.role,
    )
