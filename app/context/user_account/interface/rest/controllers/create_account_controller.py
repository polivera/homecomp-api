from fastapi import APIRouter, Depends, HTTPException

from app.context.user_account.application.commands import (
    CreateAccountCommand,
)
from app.context.user_account.application.contracts import (
    CreateAccountHandlerContract,
)
from app.context.user_account.application.dto import (
    CreateAccountErrorCode,
)
from app.context.user_account.infrastructure.dependencies import (
    get_create_account_handler,
)
from app.context.user_account.interface.schemas import (
    CreateAccountRequest,
    CreateAccountResponse,
)
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=CreateAccountResponse, status_code=201)
async def create_account(
    request: CreateAccountRequest,
    handler: CreateAccountHandlerContract = Depends(get_create_account_handler),
    user_id: int = Depends(get_current_user_id),
):
    """Create a new user account"""
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
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    return CreateAccountResponse(
        account_id=result.account_id,
        account_name=result.account_name,
        account_balance=result.account_balance,
    )
