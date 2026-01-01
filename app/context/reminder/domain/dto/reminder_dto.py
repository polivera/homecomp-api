from dataclasses import dataclass

from app.context.reminder.domain.value_objects import (
    ReminderCurrency,
    ReminderDescription,
    ReminderEndDate,
    ReminderEntryType,
    ReminderFrequency,
    ReminderID,
    ReminderStartDate,
    ReminderUserID,
)


@dataclass(frozen=True)
class ReminderDTO:
    user_id: ReminderUserID
    entry_type: ReminderEntryType
    currency: ReminderCurrency
    frequency: ReminderFrequency
    start_date: ReminderStartDate
    end_date: ReminderEndDate | None
    description: ReminderDescription
    reminder_id: ReminderID | None = None
