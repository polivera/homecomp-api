"""Contract for generate occurrences service"""

from abc import ABC, abstractmethod

from app.context.reminder.domain.dto import ReminderOccurrenceDTO
from app.context.reminder.domain.value_objects import (
    ReminderCategoryID,
    ReminderCurrency,
    ReminderDescription,
    ReminderEndDate,
    ReminderEntryType,
    ReminderFrequency,
    ReminderID,
    ReminderOccurrenceAmount,
    ReminderStartDate,
)


class GenerateOccurrencesServiceContract(ABC):
    """Service contract for generating reminder occurrences"""

    @abstractmethod
    async def generate(
        self,
        reminder_id: ReminderID,
        frequency: ReminderFrequency,
        start_date: ReminderStartDate,
        end_date: ReminderEndDate | None,
        amount: ReminderOccurrenceAmount,
        description: ReminderDescription,
        entry_type: ReminderEntryType,
        currency: ReminderCurrency,
        category_id: ReminderCategoryID | None,
    ) -> list[ReminderOccurrenceDTO]:
        """
        Generate occurrences for a reminder based on frequency and date range

        The generation logic handles:
        - daily: Every day
        - weekly: Same day of week
        - biweekly: Every 2 weeks, same day of week
        - monthly: Same day of month
        - quarterly: Every 3 months, same day
        - yearly: Same month and day

        Args:
            reminder_id: ID of the reminder
            frequency: How often the reminder recurs
            start_date: When occurrences start
            end_date: Optional end date (if None, generates up to 1 year ahead)
            amount: Amount for each occurrence
            description: Reminder description (copied to occurrences)
            entry_type: Entry type (copied to occurrences)
            currency: Currency (copied to occurrences)
            category_id: Optional category ID (copied to occurrences)

        Returns:
            List of generated occurrence DTOs

        Raises:
            InvalidReminderFrequencyError: If frequency is not supported
        """
        pass
