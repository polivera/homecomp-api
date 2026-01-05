from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.user_account.application.commands import (
    DeleteAccountCommand,
)
from app.context.user_account.application.dto import (
    DeleteAccountErrorCode,
)
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.delete("/{account_id}", status_code=204)
async def delete_account(
    account_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Delete a user account (soft delete)"""
    logger = app_container.logger
    handler = app_container.get_delete_account_handler()

    logger.info("Account deletion request", user_id=user_id, account_id=account_id)

    command = DeleteAccountCommand(
        account_id=account_id,
        user_id=user_id,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            DeleteAccountErrorCode.NOT_FOUND: 404,  # Not Found
            DeleteAccountErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 404:
            logger.warning(
                "Account deletion failed - not found",
                user_id=user_id,
                account_id=account_id,
                error_code=result.error_code.value,
            )
        else:
            logger.error(
                "Account deletion failed",
                user_id=user_id,
                account_id=account_id,
                error_code=result.error_code.value,
                error_message=result.error_message,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return 204 No Content on success
    logger.info("Account deleted successfully", user_id=user_id, account_id=account_id)
    return
