from abc import ABC, abstractmethod
from datetime import datetime

from app.context.reminder.domain.dto import ReminderOccurrenceDTO
from app.context.reminder.domain.value_objects import (
    ReminderID,
    ReminderOccurrenceID,
    ReminderOccurrenceStatus,
)


class ReminderOccurrenceRepositoryContract(ABC):
    """Contract for reminder occurrence repository operations"""

    @abstractmethod
    async def save_occurrence(self, occurrence: ReminderOccurrenceDTO) -> ReminderOccurrenceDTO:
        """Create a new occurrence"""
        pass

    @abstractmethod
    async def save_occurrences(self, occurrences: list[ReminderOccurrenceDTO]) -> list[ReminderOccurrenceDTO]:
        """Create multiple occurrences in a single transaction"""
        pass

    @abstractmethod
    async def find_occurrence(
        self,
        occurrence_id: ReminderOccurrenceID | None = None,
        reminder_id: ReminderID | None = None,
    ) -> ReminderOccurrenceDTO | None:
        """Find an occurrence by ID or reminder_id"""
        pass

    @abstractmethod
    async def find_occurrences_by_reminder(
        self,
        reminder_id: ReminderID,
    ) -> list[ReminderOccurrenceDTO]:
        """Find all occurrences for a reminder"""
        pass

    @abstractmethod
    async def find_pending_occurrences_by_date(
        self,
        before: datetime,
    ) -> list[ReminderOccurrenceDTO]:
        """Find all pending occurrences scheduled before the given datetime"""
        pass

    @abstractmethod
    async def find_pending_occurrences_by_user(
        self,
        user_id: int,
        before: datetime | None = None,
    ) -> list[ReminderOccurrenceDTO]:
        """Find all pending occurrences for a user's reminders"""
        pass

    @abstractmethod
    async def update_occurrence_status(
        self,
        occurrence_id: ReminderOccurrenceID,
        status: ReminderOccurrenceStatus,
        entry_id: int | None = None,
    ) -> bool:
        """Update occurrence status (e.g., mark as completed with entry_id)"""
        pass

    @abstractmethod
    async def delete_occurrences_by_reminder(
        self,
        reminder_id: ReminderID,
    ) -> int:
        """Delete all occurrences for a reminder (when reminder is deleted)"""
        pass
