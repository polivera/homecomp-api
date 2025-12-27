from fastapi import APIRouter, Depends, HTTPException

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.application.commands.delete_account_command import (
    DeleteAccountCommand,
)
from app.context.user_account.application.contracts.delete_account_handler_contract import (
    DeleteAccountHandlerContract,
)
from app.context.user_account.domain.value_objects.account_id import UserAccountID
from app.context.user_account.infrastructure.dependencies import (
    get_delete_account_handler,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.delete("/{account_id}", status_code=204)
async def delete_account(
    account_id: int,
    handler: DeleteAccountHandlerContract = Depends(get_delete_account_handler),
):
    """Delete a user account (soft delete)"""
    command = DeleteAccountCommand(
        account_id=UserAccountID(account_id),
        user_id=UserID(1),  # TODO: from cookie header
    )

    success = await handler.handle(command)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")

    return  # 204 No Content
