"""REST controller for updating reminders"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.reminder.application.commands import UpdateReminderCommand
from app.context.reminder.application.contracts import UpdateReminderHandlerContract
from app.context.reminder.application.dto import UpdateReminderErrorCode
from app.context.reminder.infrastructure.dependencies import get_update_reminder_handler
from app.context.reminder.interface.schemas import ReminderResponse, UpdateReminderRequest
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/reminders", tags=["reminders"])


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
