"""REST controllers for reminder endpoints"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.reminder.application.commands import (
    CreateReminderCommand,
    DeleteReminderCommand,
    UpdateReminderCommand,
)
from app.context.reminder.application.contracts import (
    CreateReminderHandlerContract,
    DeleteReminderHandlerContract,
    FindReminderHandlerContract,
    ListRemindersHandlerContract,
    UpdateReminderHandlerContract,
)
from app.context.reminder.application.dto import (
    CreateReminderErrorCode,
    DeleteReminderErrorCode,
    FindReminderErrorCode,
    ListRemindersErrorCode,
    UpdateReminderErrorCode,
)
from app.context.reminder.application.queries import FindReminderQuery, ListRemindersQuery
from app.context.reminder.infrastructure.dependencies import (
    get_create_reminder_handler,
    get_delete_reminder_handler,
    get_find_reminder_handler,
    get_list_reminders_handler,
    get_update_reminder_handler,
)
from app.context.reminder.interface.rest.schemas import (
    CreateReminderRequest,
    DeleteReminderResponse,
    ReminderListResponse,
    ReminderResponse,
    UpdateReminderRequest,
)
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.post("", status_code=201, response_model=ReminderResponse)
async def create_reminder(
    request: CreateReminderRequest,
    handler: Annotated[CreateReminderHandlerContract, Depends(get_create_reminder_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Create a new reminder"""

    command = CreateReminderCommand(
        user_id=user_id,
        description=request.description,
        entry_type=request.entry_type,
        currency=request.currency,
        frequency=request.frequency,
        start_date=request.start_date,
        end_date=request.end_date,
        category_id=request.category_id,
    )

    result = await handler.handle(command)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            CreateReminderErrorCode.INVALID_DATE_RANGE: 400,
            CreateReminderErrorCode.INVALID_FREQUENCY: 400,
            CreateReminderErrorCode.MAPPER_ERROR: 500,
            CreateReminderErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    return ReminderResponse(
        id=result.reminder_id,
        description=result.description,
        entry_type=result.entry_type,
        currency=result.currency,
        frequency=result.frequency,
        start_date=result.start_date,
        end_date=result.end_date,
        category_id=result.category_id,
    )


@router.get("", response_model=ReminderListResponse)
async def list_reminders(
    handler: Annotated[ListRemindersHandlerContract, Depends(get_list_reminders_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    active_only: bool = True,
):
    """List all reminders for the authenticated user"""

    query = ListRemindersQuery(user_id=user_id, active_only=active_only)

    result = await handler.handle(query)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            ListRemindersErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Convert to response
    reminders = [
        ReminderResponse(
            id=item.reminder_id,
            description=item.description,
            entry_type=item.entry_type,
            currency=item.currency,
            frequency=item.frequency,
            start_date=item.start_date,
            end_date=item.end_date,
            category_id=item.category_id,
        )
        for item in result.reminders
    ]

    return ReminderListResponse(reminders=reminders)


@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(
    reminder_id: int,
    handler: Annotated[FindReminderHandlerContract, Depends(get_find_reminder_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Get a specific reminder by ID"""

    query = FindReminderQuery(reminder_id=reminder_id, user_id=user_id)

    result = await handler.handle(query)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            FindReminderErrorCode.REMINDER_NOT_FOUND: 404,
            FindReminderErrorCode.REMINDER_NOT_BELONGS_TO_USER: 403,
            FindReminderErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    return ReminderResponse(
        id=result.reminder_id,
        description=result.description,
        entry_type=result.entry_type,
        currency=result.currency,
        frequency=result.frequency,
        start_date=result.start_date,
        end_date=result.end_date,
        category_id=result.category_id,
    )


@router.patch("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: int,
    request: UpdateReminderRequest,
    handler: Annotated[UpdateReminderHandlerContract, Depends(get_update_reminder_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Update an existing reminder"""

    command = UpdateReminderCommand(
        reminder_id=reminder_id,
        user_id=user_id,
        description=request.description,
        entry_type=request.entry_type,
        currency=request.currency,
        frequency=request.frequency,
        start_date=request.start_date,
        end_date=request.end_date,
        category_id=request.category_id,
    )

    result = await handler.handle(command)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            UpdateReminderErrorCode.REMINDER_NOT_FOUND: 404,
            UpdateReminderErrorCode.REMINDER_NOT_BELONGS_TO_USER: 403,
            UpdateReminderErrorCode.INVALID_DATE_RANGE: 400,
            UpdateReminderErrorCode.INVALID_FREQUENCY: 400,
            UpdateReminderErrorCode.MAPPER_ERROR: 500,
            UpdateReminderErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    # Return success response
    return ReminderResponse(
        id=result.reminder_id,
        description=result.description,
        entry_type=result.entry_type,
        currency=result.currency,
        frequency=result.frequency,
        start_date=result.start_date,
        end_date=result.end_date,
        category_id=result.category_id,
    )


@router.delete("/{reminder_id}", response_model=DeleteReminderResponse)
async def delete_reminder(
    reminder_id: int,
    handler: Annotated[DeleteReminderHandlerContract, Depends(get_delete_reminder_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Delete a reminder"""

    command = DeleteReminderCommand(reminder_id=reminder_id, user_id=user_id)

    result = await handler.handle(command)

    # Map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            DeleteReminderErrorCode.REMINDER_NOT_FOUND: 404,
            DeleteReminderErrorCode.REMINDER_NOT_BELONGS_TO_USER: 403,
            DeleteReminderErrorCode.UNEXPECTED_ERROR: 500,
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    return DeleteReminderResponse(message="Reminder deleted successfully")
