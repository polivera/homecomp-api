"""REST controller for finding/listing reminders"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.reminder.application.contracts import (
    FindReminderHandlerContract,
    ListRemindersHandlerContract,
)
from app.context.reminder.application.dto import FindReminderErrorCode, ListRemindersErrorCode
from app.context.reminder.application.queries import FindReminderQuery, ListRemindersQuery
from app.context.reminder.infrastructure.dependencies import (
    get_find_reminder_handler,
    get_list_reminders_handler,
)
from app.context.reminder.interface.schemas import ReminderListResponse, ReminderResponse
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/reminders", tags=["reminders"])


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

    if not result.reminders:
        raise HTTPException(status_code=500, detail="Error in reminder create response")

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

    if not result.reminder or not result.reminder.reminder_id:
        raise HTTPException(status_code=500, detail="Error in find reminder by ID")

    # Return success response
    return ReminderResponse(
        id=result.reminder.reminder_id.value,
        description=result.reminder.description.value,
        entry_type=result.reminder.entry_type.value,
        currency=result.reminder.currency.value,
        frequency=result.reminder.frequency.value,
        start_date=result.reminder.start_date.value,
        category_id=result.reminder.category_id.value,
        end_date=result.reminder.end_date.value if result.reminder.end_date else None,
    )
