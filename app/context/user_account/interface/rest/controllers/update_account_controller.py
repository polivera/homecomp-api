from fastapi import APIRouter, Depends, HTTPException

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.application.commands.update_account_command import (
    UpdateAccountCommand,
)
from app.context.user_account.application.contracts.update_account_handler_contract import (
    UpdateAccountHandlerContract,
)
from app.context.user_account.domain.value_objects.account_id import AccountID
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.domain.value_objects.balance import Balance
from app.context.user_account.domain.value_objects.currency import Currency
from app.context.user_account.infrastructure.dependencies import (
    get_update_account_handler,
)
from app.context.user_account.interface.schemas.update_account_response import (
    UpdateAccountResponse,
)
from app.context.user_account.interface.schemas.update_account_schema import (
    UpdateAccountRequest,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.put("/{account_id}", response_model=UpdateAccountResponse)
async def update_account(
    account_id: int,
    request: UpdateAccountRequest,
    handler: UpdateAccountHandlerContract = Depends(get_update_account_handler),
):
    """Update a user account (full update - all fields required)"""
    try:
        command = UpdateAccountCommand(
            account_id=AccountID(account_id),
            user_id=UserID(1),  # TODO: from cookie header
            name=AccountName(request.name),
            currency=Currency(request.currency),
            balance=Balance.from_float(request.balance),
        )

        result = await handler.handle(command)

        return UpdateAccountResponse(
            account_id=result.account_id.value, message=result.message
        )
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
