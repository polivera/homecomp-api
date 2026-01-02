from dataclasses import dataclass

from app.context.reminder.domain.value_objects import (
    ReminderID,
    ReminderOccurrenceAmount,
    ReminderOccurrenceID,
    ReminderOccurrenceScheduledDate,
    ReminderOccurrenceStatus,
)


@dataclass(frozen=True)
class ReminderOccurrenceDTO:
    reminder_id: ReminderID
    scheduled_date: ReminderOccurrenceScheduledDate
    amount: ReminderOccurrenceAmount
    status: ReminderOccurrenceStatus
    occurrence_id: ReminderOccurrenceID | None = None
    entry_id: int | None = None
