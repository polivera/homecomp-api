"""Contract for create reminder service"""

from abc import ABC, abstractmethod

from app.context.reminder.domain.dto import ReminderDTO
from app.context.reminder.domain.value_objects import (
    ReminderCategoryID,
    ReminderCurrency,
    ReminderDescription,
    ReminderEndDate,
    ReminderEntryType,
    ReminderFrequency,
    ReminderOccurrenceAmount,
    ReminderStartDate,
    ReminderUserID,
)


class CreateReminderServiceContract(ABC):
    """Service contract for creating reminders"""

    @abstractmethod
    async def create(
        self,
        user_id: ReminderUserID,
        amount: ReminderOccurrenceAmount,
        description: ReminderDescription,
        entry_type: ReminderEntryType,
        currency: ReminderCurrency,
        frequency: ReminderFrequency,
        start_date: ReminderStartDate,
        category_id: ReminderCategoryID,
        end_date: ReminderEndDate | None = None,
    ) -> ReminderDTO:
        """
        Create a new reminder and generate initial occurrences

        Args:
            user_id: User who owns the reminder
            description: Reminder description
            entry_type: Type of entry (income/expense)
            currency: Currency for amounts
            frequency: Recurrence frequency
            start_date: When the reminder starts
            end_date: Optional end date for the reminder
            category_id: Optional category ID

        Returns:
            Created reminder DTO

        Raises:
            InvalidReminderDateRangeError: If end_date is before start_date
            InvalidReminderFrequencyError: If frequency is invalid
        """
        pass
