from fastapi import APIRouter, Depends, HTTPException

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.application.commands.create_account_command import (
    CreateAccountCommand,
)
from app.context.user_account.application.contracts.create_account_handler_contract import (
    CreateAccountHandlerContract,
)
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.domain.value_objects.balance import Balance
from app.context.user_account.domain.value_objects.currency import Currency
from app.context.user_account.infrastructure.dependencies import (
    get_create_account_handler,
)
from app.context.user_account.interface.schemas.create_account_response import (
    CreateAccountResponse,
)
from app.context.user_account.interface.schemas.create_account_schema import (
    CreateAccountRequest,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=CreateAccountResponse, status_code=201)
async def create_account(
    request: CreateAccountRequest,
    handler: CreateAccountHandlerContract = Depends(get_create_account_handler),
):
    """Create a new user account"""

    try:
        # Convert request to command with value objects
        # TODO: user_id from cookie header
        command = CreateAccountCommand(
            user_id=UserID(1),
            name=AccountName(request.name),
            currency=Currency(request.currency),
            balance=Balance.from_float(request.balance),
        )

        # Handle the command
        result = await handler.handle(command)
        if result.error is not None:
            raise HTTPException(status_code=400, detail=result.error)

        # Return response
        return CreateAccountResponse(
            account_id=result.account_id,
            account_name=result.account_name,
            account_balance=result.account_balance,
        )

    except ValueError as e:
        # Business logic errors (duplicate account, validation errors, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
