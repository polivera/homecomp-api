"""REST controller for deleting reminders"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.reminder.application.commands import DeleteReminderCommand
from app.context.reminder.application.contracts import DeleteReminderHandlerContract
from app.context.reminder.application.dto import DeleteReminderErrorCode
from app.context.reminder.infrastructure.dependencies import get_delete_reminder_handler
from app.context.reminder.interface.schemas import DeleteReminderResponse
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/reminders", tags=["reminders"])


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
