"""Handler for listing occurrences"""

from app.context.reminder.application.contracts import ListOccurrencesHandlerContract
from app.context.reminder.application.dto import ListOccurrencesErrorCode, ListOccurrencesResult, OccurrenceListItem
from app.context.reminder.application.queries import ListOccurrencesQuery
from app.context.reminder.domain.contracts.infrastructure import ReminderOccurrenceRepositoryContract
from app.context.reminder.domain.value_objects import ReminderID, ReminderUserID


class ListOccurrencesHandler(ListOccurrencesHandlerContract):
    """Handler for list occurrences query"""

    def __init__(self, repository: ReminderOccurrenceRepositoryContract):
        self._repository = repository

    async def handle(self, query: ListOccurrencesQuery) -> ListOccurrencesResult:
        """Execute list occurrences query"""

        try:
            # Convert primitives to value objects
            user_id = ReminderUserID(query.user_id)
            reminder_id = ReminderID(query.reminder_id) if query.reminder_id else None

            # Query repository based on parameters
            if reminder_id:
                # Get occurrences for specific reminder
                occurrence_dtos = await self._repository.find_occurrences_by_reminder(reminder_id=reminder_id)
            else:
                # Get all pending occurrences for user
                occurrence_dtos = await self._repository.find_pending_occurrences_by_user(user_id=user_id)

            # Convert to list items
            items = [
                OccurrenceListItem(
                    occurrence_id=dto.occurrence_id.value if dto.occurrence_id else 0,
                    reminder_id=dto.reminder_id.value,
                    scheduled_date=dto.scheduled_date.value,
                    amount=dto.amount.value,
                    status=dto.status.value,
                    entry_id=dto.entry_id,
                    description=dto.description.value if dto.description else None,
                    entry_type=dto.entry_type.value if dto.entry_type else None,
                    currency=dto.currency.value if dto.currency else None,
                    category_id=dto.category_id.value if dto.category_id else None,
                )
                for dto in occurrence_dtos
            ]

            return ListOccurrencesResult(occurrences=items)

        except Exception:
            return ListOccurrencesResult(
                error_code=ListOccurrencesErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error listing occurrences",
            )
