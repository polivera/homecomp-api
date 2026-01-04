from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.household.application.commands import RemoveMemberCommand
from app.context.household.application.dto import RemoveMemberErrorCode
from app.context.household.interface.schemas import RemoveMemberResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.delete("/{household_id}/members/{member_user_id}", status_code=200)
async def remove_member(
    household_id: int,
    member_user_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> RemoveMemberResponse:
    """Remove a member from a household"""
    logger = app_container.logger
    handler = app_container.get_remove_member_handler()

    logger.info(
        "Remove member request",
        remover_user_id=user_id,
        household_id=household_id,
        member_user_id=member_user_id,
    )

    command = RemoveMemberCommand(
        remover_user_id=user_id,
        household_id=household_id,
        member_user_id=member_user_id,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            RemoveMemberErrorCode.ONLY_OWNER_CAN_REMOVE: 403,  # Forbidden
            RemoveMemberErrorCode.CANNOT_REMOVE_SELF: 400,  # Bad Request
            RemoveMemberErrorCode.MEMBER_NOT_FOUND: 404,  # Not Found
            RemoveMemberErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)
        logger.warning("Remove member failed", household_id=household_id, error_code=result.error_code.value)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    logger.info("Member removed successfully", household_id=household_id, member_user_id=member_user_id)
    return RemoveMemberResponse(
        success=True,
        message="Member removed successfully",
    )
