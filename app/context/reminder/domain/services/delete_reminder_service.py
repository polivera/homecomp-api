"""Service for deleting reminders"""

from app.context.reminder.domain.contracts.infrastructure import (
    ReminderOccurrenceRepositoryContract,
    ReminderRepositoryContract,
)
from app.context.reminder.domain.contracts.services import DeleteReminderServiceContract
from app.context.reminder.domain.exceptions import ReminderNotBelongsToUserError, ReminderNotFoundError
from app.context.reminder.domain.value_objects import ReminderID, ReminderUserID


class DeleteReminderService(DeleteReminderServiceContract):
    """Service for deleting reminders and their occurrences"""

    def __init__(
        self,
        reminder_repo: ReminderRepositoryContract,
        occurrence_repo: ReminderOccurrenceRepositoryContract,
    ):
        self._reminder_repo = reminder_repo
        self._occurrence_repo = occurrence_repo

    async def delete(self, reminder_id: ReminderID, user_id: ReminderUserID) -> None:
        """Delete a reminder and all its occurrences"""

        # Verify reminder exists and belongs to user
        existing = await self._reminder_repo.find_user_reminder_by_id(reminder_id=reminder_id, user_id=user_id)

        if not existing:
            raise ReminderNotFoundError(f"Reminder {reminder_id.value} not found")

        if existing.user_id.value != user_id.value:
            raise ReminderNotBelongsToUserError(f"Reminder {reminder_id.value} does not belong to user")

        # Delete occurrences first (cascade delete)
        await self._occurrence_repo.delete_occurrences_by_reminder(reminder_id)

        # Delete reminder
        await self._reminder_repo.delete_reminder(reminder_id)
