from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.user_account.application.commands import (
    CreateAccountCommand,
)
from app.context.user_account.application.dto import (
    CreateAccountErrorCode,
)
from app.context.user_account.interface.schemas import (
    CreateAccountRequest,
    CreateAccountResponse,
)
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=CreateAccountResponse, status_code=201)
async def create_account(
    request: CreateAccountRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Create a new user account"""
    logger = app_container.logger
    handler = app_container.get_create_account_handler()

    logger.info("Account creation request", user_id=user_id, name=request.name, currency=request.currency)

    command = CreateAccountCommand(
        user_id=user_id,
        name=request.name,
        currency=request.currency,
        balance=request.balance,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            CreateAccountErrorCode.NAME_ALREADY_EXISTS: 409,  # Conflict
            CreateAccountErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            CreateAccountErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }

        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 409:
            logger.warning(
                "Account creation failed - name already exists",
                user_id=user_id,
                name=request.name,
                error_code=result.error_code.value,
            )
        else:
            logger.error(
                "Account creation failed",
                user_id=user_id,
                name=request.name,
                error_code=result.error_code.value,
                error_message=result.error_message,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    logger.info(
        "Account created successfully",
        user_id=user_id,
        account_id=result.account_id,
        name=request.name,
    )

    return CreateAccountResponse(
        account_id=result.account_id,
        account_name=result.account_name,
        account_balance=result.account_balance,
    )
