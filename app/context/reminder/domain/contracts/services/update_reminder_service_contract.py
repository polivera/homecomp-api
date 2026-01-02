"""Contract for update reminder service"""

from abc import ABC, abstractmethod

from app.context.reminder.domain.dto import ReminderDTO
from app.context.reminder.domain.value_objects import (
    ReminderCategoryID,
    ReminderCurrency,
    ReminderDescription,
    ReminderEndDate,
    ReminderEntryType,
    ReminderFrequency,
    ReminderID,
    ReminderStartDate,
    ReminderUserID,
)


class UpdateReminderServiceContract(ABC):
    """Service contract for updating reminders"""

    @abstractmethod
    async def update(
        self,
        reminder_id: ReminderID,
        user_id: ReminderUserID,
        description: ReminderDescription | None = None,
        entry_type: ReminderEntryType | None = None,
        currency: ReminderCurrency | None = None,
        frequency: ReminderFrequency | None = None,
        start_date: ReminderStartDate | None = None,
        end_date: ReminderEndDate | None = None,
        category_id: ReminderCategoryID | None = None,
    ) -> ReminderDTO:
        """
        Update an existing reminder and regenerate occurrences if needed

        Args:
            reminder_id: ID of reminder to update
            user_id: User who owns the reminder (for ownership validation)
            description: New description
            entry_type: New entry type
            currency: New currency
            frequency: New frequency
            start_date: New start date
            end_date: New end date
            category_id: New category ID

        Returns:
            Updated reminder DTO

        Raises:
            ReminderNotFoundError: If reminder doesn't exist
            ReminderNotBelongsToUserError: If reminder doesn't belong to user
            InvalidReminderDateRangeError: If end_date is before start_date
        """
        pass
