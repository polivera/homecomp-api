from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

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
from app.context.user_account.interface.schemas.account_response import AccountResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get a specific user account by ID"""
    logger = app_container.logger
    handler = app_container.get_find_account_by_id_handler()

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

        if status_code != 404:
            logger.error(
                "Get account failed",
                user_id=user_id,
                account_id=account_id,
                error_code=result.error_code.value,
                error_message=result.error_message,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    if not result.account:
        logger.error(
            "Get account response missing account data",
            user_id=user_id,
            account_id=account_id,
        )
        raise HTTPException(status_code=500, detail="error in response data")

    return AccountResponse(
        account_id=result.account.account_id,
        name=result.account.name,
        currency=result.account.currency,
        balance=result.account.balance,
    )


@router.get("", response_model=list[AccountResponse])
async def get_all_accounts(
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get all accounts for the authenticated user"""
    logger = app_container.logger
    handler = app_container.get_find_accounts_by_user_handler()

    query = FindAccountsByUserQuery(user_id=user_id)
    result = await handler.handle(query)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            FindMultipleAccountsErrorCode.UNEXPECTED_ERROR: 500,
        }

        status_code = status_code_map.get(result.error_code, 500)

        logger.error(
            "Get all accounts failed",
            user_id=user_id,
            error_code=result.error_code.value,
            error_message=result.error_message,
        )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return empty list if no accounts (not an error)
    if not result.accounts:
        return []

    return [
        AccountResponse(
            account_id=r.account_id,
            name=r.name,
            currency=r.currency,
            balance=r.balance,
        )
        for r in result.accounts
    ]
