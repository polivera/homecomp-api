from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.user_account.application.contracts.find_account_by_id_handler_contract import (
    FindAccountByIdHandlerContract,
)
from app.context.user_account.application.contracts.find_accounts_by_user_handler_contract import (
    FindAccountsByUserHandlerContract,
)
from app.context.user_account.application.dto import (
    FindMultipleAccountsErrorCode,
    FindSingleAccountErrorCode,
)
from app.context.user_account.application.queries.find_account_by_id_query import (
    FindAccountByIdQuery,
)
from app.context.user_account.application.queries.find_accounts_by_user_query import (
    FindAccountsByUserQuery,
)
from app.context.user_account.infrastructure.dependencies import (
    get_find_account_by_id_handler,
    get_find_accounts_by_user_handler,
)
from app.context.user_account.interface.schemas.account_response import AccountResponse
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    handler: Annotated[FindAccountByIdHandlerContract, Depends(get_find_account_by_id_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get a specific user account by ID"""
    query = FindAccountByIdQuery(
        account_id=account_id,
        user_id=user_id,
    )

    result = await handler.handle(query)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            FindSingleAccountErrorCode.NOT_FOUND: 404,
            FindSingleAccountErrorCode.UNEXPECTED_ERROR: 500,
        }

        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    if not result.account:
        raise HTTPException(status_code=500, detail="error in response data")

    # Return success response
    return AccountResponse(
        account_id=result.account.account_id,
        name=result.account.name,
        currency=result.account.currency,
        balance=result.account.balance,
    )


@router.get("", response_model=list[AccountResponse])
async def get_all_accounts(
    handler: Annotated[FindAccountsByUserHandlerContract, Depends(get_find_accounts_by_user_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get all accounts for the authenticated user"""
    query = FindAccountsByUserQuery(user_id=user_id)
    result = await handler.handle(query)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            FindMultipleAccountsErrorCode.UNEXPECTED_ERROR: 500,
        }

        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return empty list if no accounts (not an error)
    if not result.accounts:
        return []

    # Return success response
    return [
        AccountResponse(
            account_id=r.account_id,
            name=r.name,
            currency=r.currency,
            balance=r.balance,
        )
        for r in result.accounts
    ]
