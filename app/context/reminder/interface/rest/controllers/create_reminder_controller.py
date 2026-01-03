"""REST controller for creating reminders"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.reminder.application.commands import CreateReminderCommand
from app.context.reminder.application.contracts import CreateReminderHandlerContract
from app.context.reminder.application.dto import CreateReminderErrorCode
from app.context.reminder.infrastructure.dependencies import get_create_reminder_handler
from app.context.reminder.interface.schemas import CreateReminderRequest, ReminderResponse
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
        amount=request.amount,
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

    if not result.reminder or not result.reminder.reminder_id:
        raise HTTPException(status_code=500, detail="Invalid success result")

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
