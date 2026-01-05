from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import DeclineInviteCommand
from app.context.household.application.dto import DeclineInviteErrorCode
from app.context.household.interface.schemas import DeclineInviteResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.post("/{household_id}/invites/decline", status_code=200)
async def decline_invite(
    household_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> DeclineInviteResponse:
    """Decline a household invitation"""
    logger = app_container.logger
    handler = app_container.get_decline_invite_handler()

    logger.info("Decline invite request", user_id=user_id, household_id=household_id)

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
        logger.warning("Decline invite failed", household_id=household_id, error_code=result.error_code.value)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    logger.info("Invite declined successfully", user_id=user_id, household_id=household_id)
    return DeclineInviteResponse(
        success=True,
        message="Invitation declined successfully",
    )
