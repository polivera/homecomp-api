"""Handler for deleting reminders"""

from app.context.reminder.application.commands import DeleteReminderCommand
from app.context.reminder.application.contracts import DeleteReminderHandlerContract
from app.context.reminder.application.dto import DeleteReminderErrorCode, DeleteReminderResult
from app.context.reminder.domain.contracts.services import DeleteReminderServiceContract
from app.context.reminder.domain.exceptions import ReminderNotBelongsToUserError, ReminderNotFoundError
from app.context.reminder.domain.value_objects import ReminderID, ReminderUserID


class DeleteReminderHandler(DeleteReminderHandlerContract):
    """Handler for delete reminder command"""

    def __init__(self, service: DeleteReminderServiceContract):
        self._service = service

    async def handle(self, command: DeleteReminderCommand) -> DeleteReminderResult:
        """Execute delete reminder command"""

        try:
            # Convert primitives to value objects
            reminder_id = ReminderID(command.reminder_id)
            user_id = ReminderUserID(command.user_id)

            # Call domain service
            await self._service.delete(reminder_id=reminder_id, user_id=user_id)

            return DeleteReminderResult(deleted=True)

        except ReminderNotFoundError:
            return DeleteReminderResult(
                error_code=DeleteReminderErrorCode.REMINDER_NOT_FOUND,
                error_message="Reminder not found",
            )

        except ReminderNotBelongsToUserError:
            return DeleteReminderResult(
                error_code=DeleteReminderErrorCode.REMINDER_NOT_BELONGS_TO_USER,
                error_message="Reminder does not belong to user",
            )

        except Exception:
            return DeleteReminderResult(
                error_code=DeleteReminderErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error deleting reminder",
            )
