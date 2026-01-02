"""Handler for finding a reminder"""

from app.context.reminder.application.contracts import FindReminderHandlerContract
from app.context.reminder.application.dto import FindReminderErrorCode, FindReminderResult
from app.context.reminder.application.queries import FindReminderQuery
from app.context.reminder.domain.contracts.infrastructure import ReminderRepositoryContract
from app.context.reminder.domain.value_objects import ReminderID, ReminderUserID


class FindReminderHandler(FindReminderHandlerContract):
    """Handler for find reminder query"""

    def __init__(self, repository: ReminderRepositoryContract):
        self._repository = repository

    async def handle(self, query: FindReminderQuery) -> FindReminderResult:
        """Execute find reminder query"""

        try:
            # Convert primitives to value objects
            reminder_id = ReminderID(query.reminder_id)
            user_id = ReminderUserID(query.user_id)

            # Query repository
            reminder_dto = await self._repository.find_user_reminder_by_id(reminder_id=reminder_id, user_id=user_id)

            if not reminder_dto:
                return FindReminderResult(
                    error_code=FindReminderErrorCode.REMINDER_NOT_FOUND,
                    error_message="Reminder not found",
                )

            # Verify ownership
            if reminder_dto.user_id.value != user_id.value:
                return FindReminderResult(
                    error_code=FindReminderErrorCode.REMINDER_NOT_BELONGS_TO_USER,
                    error_message="Reminder does not belong to user",
                )

            # Convert to result DTO
            return FindReminderResult(
                reminder_id=reminder_dto.reminder_id.value if reminder_dto.reminder_id else None,
                description=reminder_dto.description.value,
                entry_type=reminder_dto.entry_type.value,
                currency=reminder_dto.currency.value,
                frequency=reminder_dto.frequency.value,
                start_date=reminder_dto.start_date.value,
                end_date=reminder_dto.end_date.value if reminder_dto.end_date else None,
                category_id=reminder_dto.category_id.value if reminder_dto.category_id else None,
            )

        except Exception:
            return FindReminderResult(
                error_code=FindReminderErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error finding reminder",
            )
