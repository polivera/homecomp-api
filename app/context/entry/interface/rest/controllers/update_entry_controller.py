from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.entry.application.commands import UpdateEntryCommand
from app.context.entry.application.contracts import UpdateEntryHandlerContract
from app.context.entry.application.dto import UpdateEntryErrorCode
from app.context.entry.infrastructure.dependencies import get_update_entry_handler
from app.context.entry.interface.schemas import UpdateEntryRequest, UpdateEntryResponse
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/entries")


@router.put("/{entry_id}", response_model=UpdateEntryResponse)
async def update_entry(
    entry_id: int,
    request: UpdateEntryRequest,
    handler: Annotated[UpdateEntryHandlerContract, Depends(get_update_entry_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    """Update an entry (full update - all fields required)"""
    logger.info("Update entry request", user_id=user_id, entry_id=entry_id)

    command = UpdateEntryCommand(
        entry_id=entry_id,
        user_id=user_id,
        account_id=request.account_id,
        category_id=request.category_id,
        entry_type=request.entry_type,
        entry_date=request.entry_date,
        amount=request.amount,
        description=request.description,
    )

    result = await handler.handle(command)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            UpdateEntryErrorCode.NOT_FOUND: 404,
            UpdateEntryErrorCode.ACCOUNT_NOT_BELONGS_TO_USER: 403,
            UpdateEntryErrorCode.CATEGORY_NOT_FOUND: 404,
            UpdateEntryErrorCode.CATEGORY_NOT_BELONGS_TO_USER: 403,
            UpdateEntryErrorCode.MAPPER_ERROR: 500,
            UpdateEntryErrorCode.UNEXPECTED_ERROR: 500,
        }

        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 404:
            logger.warning("Entry update failed - not found", user_id=user_id, entry_id=entry_id)
        elif status_code == 403:
            logger.warning("Entry update failed - forbidden", user_id=user_id, entry_id=entry_id)
        else:
            logger.error("Entry update failed", user_id=user_id, entry_id=entry_id, error=result.error_message)

        raise HTTPException(status_code=status_code, detail=result.error_message)

    if not result.entry:
        raise HTTPException(status_code=500, detail="Unexpected error on response values")

    logger.info("Entry updated successfully", user_id=user_id, entry_id=entry_id)

    return UpdateEntryResponse(
        entry_id=result.entry.entry_id,
        account_id=result.entry.account_id,
        category_id=result.entry.category_id,
        entry_type=result.entry.entry_type,
        entry_date=result.entry.entry_date,
        amount=result.entry.amount,
        description=result.entry.description,
    )
