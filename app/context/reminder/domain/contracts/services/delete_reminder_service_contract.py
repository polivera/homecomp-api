"""Contract for delete reminder service"""

from abc import ABC, abstractmethod

from app.context.reminder.domain.value_objects import ReminderID, ReminderUserID


class DeleteReminderServiceContract(ABC):
    """Service contract for deleting reminders"""

    @abstractmethod
    async def delete(self, reminder_id: ReminderID, user_id: ReminderUserID) -> None:
        """
        Delete a reminder and all its occurrences

        Args:
            reminder_id: ID of reminder to delete
            user_id: User who owns the reminder (for ownership validation)

        Raises:
            ReminderNotFoundError: If reminder doesn't exist
            ReminderNotBelongsToUserError: If reminder doesn't belong to user
        """
        pass
