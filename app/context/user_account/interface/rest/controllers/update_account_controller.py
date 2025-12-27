from fastapi import APIRouter, Depends, HTTPException

from app.context.user_account.application.commands.update_account_command import (
    UpdateAccountCommand,
)
from app.context.user_account.application.contracts.update_account_handler_contract import (
    UpdateAccountHandlerContract,
)
from app.context.user_account.infrastructure.dependencies import (
    get_update_account_handler,
)
from app.context.user_account.interface.schemas.update_account_response import (
    UpdateAccountResponse,
)
from app.context.user_account.interface.schemas.update_account_schema import (
    UpdateAccountRequest,
)
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.put("/{account_id}", response_model=UpdateAccountResponse)
async def update_account(
    account_id: int,
    request: UpdateAccountRequest,
    handler: UpdateAccountHandlerContract = Depends(get_update_account_handler),
    user_id: int = Depends(get_current_user_id),
):
    """Update a user account (full update - all fields required)"""
    try:
        command = UpdateAccountCommand(
            account_id=account_id,
            user_id=user_id,
            name=request.name,
            currency=request.currency,
            balance=request.balance,
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
