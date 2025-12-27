from fastapi import APIRouter, Depends, HTTPException

from app.context.user_account.application.commands.create_account_command import (
    CreateAccountCommand,
)
from app.context.user_account.application.contracts.create_account_handler_contract import (
    CreateAccountHandlerContract,
)
from app.context.user_account.domain.exceptions import (
    UserAccountMapperError,
    UserAccountNameAlreadyExistError,
)
from app.context.user_account.infrastructure.dependencies import (
    get_create_account_handler,
)
from app.context.user_account.interface.schemas.create_account_response import (
    CreateAccountResponse,
)
from app.context.user_account.interface.schemas.create_account_schema import (
    CreateAccountRequest,
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

    try:
        command = CreateAccountCommand(
            user_id=user_id,
            name=request.name,
            currency=request.currency,
            balance=request.balance,
        )

        result = await handler.handle(command)
        if result.error is not None:
            raise HTTPException(status_code=400, detail=result.error)

        return CreateAccountResponse(
            account_id=result.account_id,
            account_name=result.account_name,
            account_balance=result.account_balance,
        )
    except UserAccountNameAlreadyExistError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserAccountMapperError or Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
