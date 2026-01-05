from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.entry.application.commands import CreateEntryCommand
from app.context.entry.application.dto import CreateEntryErrorCode
from app.context.entry.interface.schemas import CreateEntryRequest, CreateEntryResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/entries")


@router.post("", response_model=CreateEntryResponse, status_code=201)
async def create_entry(
    request: CreateEntryRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Create a new entry"""
    logger = app_container.logger
    handler = app_container.get_create_entry_handler()

    logger.info("Create entry request", user_id=user_id, account_id=request.account_id)

    command = CreateEntryCommand(
        user_id=user_id,
        account_id=request.account_id,
        category_id=request.category_id,
        entry_type=request.entry_type,
        entry_date=request.entry_date,
        amount=request.amount,
        description=request.description,
        household_id=request.household_id,
    )

    result = await handler.handle(command)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            CreateEntryErrorCode.ACCOUNT_NOT_BELONGS_TO_USER: 403,
            CreateEntryErrorCode.CATEGORY_NOT_FOUND: 404,
            CreateEntryErrorCode.CATEGORY_NOT_BELONGS_TO_USER: 403,
            CreateEntryErrorCode.MAPPER_ERROR: 500,
            CreateEntryErrorCode.UNEXPECTED_ERROR: 500,
        }

        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 403:
            logger.warning("Entry creation failed - forbidden", user_id=user_id, error=result.error_message)
        elif status_code == 404:
            logger.warning("Entry creation failed - not found", user_id=user_id, error=result.error_message)
        else:
            logger.error("Entry creation failed", user_id=user_id, error=result.error_message)

        raise HTTPException(status_code=status_code, detail=result.error_message)

    assert result.entry_id
    assert result.account_id
    assert result.category_id
    assert result.entry_type
    assert result.entry_date
    assert result.amount
    assert result.description

    logger.info("Entry created successfully", user_id=user_id, entry_id=result.entry_id)

    return CreateEntryResponse(
        entry_id=result.entry_id,
        account_id=result.account_id,
        category_id=result.category_id,
        entry_type=result.entry_type,
        entry_date=result.entry_date,
        amount=result.amount,
        description=result.description,
    )
