"""Handler for listing reminders"""

from app.context.reminder.application.contracts import ListRemindersHandlerContract
from app.context.reminder.application.dto import ListRemindersErrorCode, ListRemindersResult, ReminderListItem
from app.context.reminder.application.queries import ListRemindersQuery
from app.context.reminder.domain.contracts.infrastructure import ReminderRepositoryContract
from app.context.reminder.domain.value_objects import ReminderUserID


class ListRemindersHandler(ListRemindersHandlerContract):
    """Handler for list reminders query"""

    def __init__(self, repository: ReminderRepositoryContract):
        self._repository = repository

    async def handle(self, query: ListRemindersQuery) -> ListRemindersResult:
        """Execute list reminders query"""

        try:
            # Convert primitives to value objects
            user_id = ReminderUserID(query.user_id)

            # Query repository
            reminder_dtos = await self._repository.find_user_reminders(user_id=user_id, active_only=query.active_only)

            # Convert to list items
            items = [
                ReminderListItem(
                    reminder_id=dto.reminder_id.value if dto.reminder_id else 0,
                    description=dto.description.value,
                    entry_type=dto.entry_type.value,
                    currency=dto.currency.value,
                    frequency=dto.frequency.value,
                    start_date=dto.start_date.value,
                    end_date=dto.end_date.value if dto.end_date else None,
                    category_id=dto.category_id.value if dto.category_id else None,
                )
                for dto in reminder_dtos
            ]

            return ListRemindersResult(reminders=items)

        except Exception:
            return ListRemindersResult(
                error_code=ListRemindersErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error listing reminders",
            )
