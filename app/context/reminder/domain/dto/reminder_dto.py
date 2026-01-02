from dataclasses import dataclass

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
    ReminderUserID,
)


@dataclass(frozen=True)
class ReminderDTO:
    user_id: ReminderUserID
    category_id: ReminderCategoryID
    entry_type: ReminderEntryType
    currency: ReminderCurrency
    amount: ReminderOccurrenceAmount
    frequency: ReminderFrequency
    start_date: ReminderStartDate
    description: ReminderDescription
    end_date: ReminderEndDate | None = None
    reminder_id: ReminderID | None = None
