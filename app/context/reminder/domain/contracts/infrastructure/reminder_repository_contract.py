from abc import ABC, abstractmethod
from datetime import datetime

from app.context.reminder.domain.dto import ReminderDTO
from app.context.reminder.domain.value_objects import (
    ReminderID,
    ReminderUserID,
)


class ReminderRepositoryContract(ABC):
    """Contract for reminder repository operations"""

    @abstractmethod
    async def save_reminder(self, reminder: ReminderDTO) -> ReminderDTO:
        """Create a new reminder"""
        pass

    @abstractmethod
    async def find_reminder(
        self,
        reminder_id: ReminderID | None = None,
        user_id: ReminderUserID | None = None,
    ) -> ReminderDTO | None:
        """Find a reminder by ID or user_id"""
        pass

    @abstractmethod
    async def find_user_reminders(
        self,
        user_id: ReminderUserID,
        reminder_id: ReminderID | None = None,
        only_active: bool | None = True,
    ) -> list[ReminderDTO]:
        """Find all reminders for a user"""
        pass

    @abstractmethod
    async def find_user_reminder_by_id(
        self,
        user_id: ReminderUserID,
        reminder_id: ReminderID,
        only_active: bool | None = True,
    ) -> ReminderDTO | None:
        """Find a specific reminder by ID for a user"""
        pass

    @abstractmethod
    async def update_reminder(self, reminder: ReminderDTO) -> ReminderDTO:
        """Update an existing reminder"""
        pass

    @abstractmethod
    async def delete_reminder(
        self,
        reminder_id: ReminderID,
        user_id: ReminderUserID,
    ) -> bool:
        """Delete a reminder"""
        pass

    @abstractmethod
    async def find_active_reminders_due_before(
        self,
        before: datetime,
    ) -> list[ReminderDTO]:
        """Find all active reminders with start_date before the given datetime"""
        pass
