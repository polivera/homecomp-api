from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.context.entry.application.dto import (
    FindMultipleEntriesErrorCode,
    FindSingleEntryErrorCode,
)
from app.context.entry.application.queries import (
    FindEntriesByAccountMonthQuery,
    FindEntryByIdQuery,
)
from app.context.entry.interface.schemas import EntryResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/entries")


@router.get("/{entry_id}", response_model=EntryResponse)
async def get_entry(
    entry_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get a specific entry by ID"""
    logger = app_container.logger
    handler = app_container.get_find_entry_by_id_handler()

    query = FindEntryByIdQuery(entry_id=entry_id, user_id=user_id)
    result = await handler.handle(query)

    if result.error_code:
        status_code_map = {
            FindSingleEntryErrorCode.NOT_FOUND: 404,
            FindSingleEntryErrorCode.UNEXPECTED_ERROR: 500,
        }

        status_code = status_code_map.get(result.error_code, 500)

        if status_code != 404:
            logger.error("Get entry failed", user_id=user_id, entry_id=entry_id, error=result.error_message)

        raise HTTPException(status_code=status_code, detail=result.error_message)

    if not result.entry:
        logger.error("Get entry response missing entry data", user_id=user_id, entry_id=entry_id)
        raise HTTPException(status_code=500, detail="Error in response data")

    return EntryResponse(
        entry_id=result.entry.entry_id,
        user_id=result.entry.user_id,
        account_id=result.entry.account_id,
        category_id=result.entry.category_id,
        entry_type=result.entry.entry_type,
        entry_date=result.entry.entry_date,
        amount=result.entry.amount,
        description=result.entry.description,
        household_id=result.entry.household_id,
    )


@router.get("", response_model=list[EntryResponse])
async def list_entries(
    account_id: Annotated[int, Query(gt=0, description="Account ID (required)")],
    month: Annotated[int, Query(ge=1, le=12, description="Month (1-12, required)")],
    year: Annotated[int, Query(ge=1900, le=2100, description="Year (e.g., 2025, required)")],
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get all entries for a specific account in a given month/year"""
    logger = app_container.logger
    handler = app_container.get_find_entries_by_account_month_handler()

    query = FindEntriesByAccountMonthQuery(
        user_id=user_id,
        account_id=account_id,
        month=month,
        year=year,
    )
    result = await handler.handle(query)

    if result.error_code:
        status_code_map = {
            FindMultipleEntriesErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        logger.error("List entries failed", user_id=user_id, error=result.error_message)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return empty list if no entries (not an error)
    if not result.entries:
        return []

    return [
        EntryResponse(
            entry_id=e.entry_id,
            user_id=e.user_id,
            account_id=e.account_id,
            category_id=e.category_id,
            entry_type=e.entry_type,
            entry_date=e.entry_date,
            amount=e.amount,
            description=e.description,
            household_id=e.household_id,
        )
        for e in result.entries
    ]
