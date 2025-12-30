from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.user_account.application.commands import (
    UpdateAccountCommand,
)
from app.context.user_account.application.contracts import (
    UpdateAccountHandlerContract,
)
from app.context.user_account.application.dto import (
    UpdateAccountErrorCode,
)
from app.context.user_account.infrastructure.dependencies import (
    get_update_account_handler,
)
from app.context.user_account.interface.schemas import (
    UpdateAccountRequest,
    UpdateAccountResponse,
)
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.put("/{account_id}", response_model=UpdateAccountResponse)
async def update_account(
    account_id: int,
    request: UpdateAccountRequest,
    handler: Annotated[UpdateAccountHandlerContract, Depends(get_update_account_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    """Update a user account (full update - all fields required)"""
    logger.info("Account update request", user_id=user_id, account_id=account_id, name=request.name)

    command = UpdateAccountCommand(
        account_id=account_id,
        user_id=user_id,
        name=request.name,
        currency=request.currency,
        balance=request.balance,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            UpdateAccountErrorCode.NOT_FOUND: 404,  # Not Found
            UpdateAccountErrorCode.NAME_ALREADY_EXISTS: 409,  # Conflict
            UpdateAccountErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            UpdateAccountErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 404:
            logger.warning(
                "Account update failed - not found",
                user_id=user_id,
                account_id=account_id,
                error_code=result.error_code.value,
            )
        elif status_code == 409:
            logger.warning(
                "Account update failed - name already exists",
                user_id=user_id,
                account_id=account_id,
                name=request.name,
                error_code=result.error_code.value,
            )
        else:
            logger.error(
                "Account update failed",
                user_id=user_id,
                account_id=account_id,
                error_code=result.error_code.value,
                error_message=result.error_message,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    if not result.account_id or not result.account_name or not result.account_balance:
        logger.error(
            "Account update response missing required fields",
            user_id=user_id,
            account_id=account_id,
        )
        raise HTTPException(status_code=500, detail="error on required response fields")

    # Return success response
    logger.info(
        "Account updated successfully",
        user_id=user_id,
        account_id=account_id,
        name=request.name,
    )

    return UpdateAccountResponse(
        account_id=result.account_id,
        account_name=result.account_name,
        account_balance=result.account_balance,
    )
