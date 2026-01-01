from datetime import datetime
from typing import Any, cast

from sqlalchemy import select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.reminder.domain.contracts.infrastructure import (
    ReminderRepositoryContract,
)
from app.context.reminder.domain.dto import ReminderDTO
from app.context.reminder.domain.value_objects import (
    ReminderID,
    ReminderStartDate,
    ReminderUserID,
)
from app.context.reminder.infrastructure.mappers import ReminderMapper
from app.context.reminder.infrastructure.models import ReminderModel


class ReminderRepository(ReminderRepositoryContract):
    """Repository implementation for reminder operations"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save_reminder(self, reminder: ReminderDTO) -> ReminderDTO:
        """Create a new reminder"""
        try:
            model = ReminderMapper.to_model(reminder)
            self._db.add(model)
            await self._db.commit()
            await self._db.refresh(model)
            return ReminderMapper.to_dto_or_fail(model)
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise ValueError(f"Database error while saving reminder: {str(e)}") from e

    async def find_reminder(
        self,
        reminder_id: ReminderID | None = None,
        user_id: ReminderUserID | None = None,
    ) -> ReminderDTO | None:
        """Find a reminder by ID or user_id"""
        try:
            stmt = select(ReminderModel)

            if reminder_id is not None:
                stmt = stmt.where(ReminderModel.id == reminder_id.value)
            elif user_id is not None:
                stmt = stmt.where(ReminderModel.user_id == user_id.value)
            else:
                raise ValueError("Must provide either reminder_id or user_id")

            result = await self._db.execute(stmt)
            model = result.scalar_one_or_none()

            return ReminderMapper.to_dto(model) if model else None
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while finding reminder: {str(e)}") from e

    async def find_user_reminders(
        self,
        user_id: ReminderUserID,
        reminder_id: ReminderID | None = None,
        only_active: bool | None = True,
    ) -> list[ReminderDTO]:
        """Find all reminders for a user"""
        try:
            stmt = select(ReminderModel).where(ReminderModel.user_id == user_id.value)

            if only_active:
                now = ReminderStartDate.now().value
                stmt = stmt.where(
                    (ReminderModel.start_date <= now)
                    & ((ReminderModel.end_date.is_(None)) | (ReminderModel.end_date > now))
                )

            if reminder_id is not None:
                stmt = stmt.where(ReminderModel.id == reminder_id.value)

            models = (await self._db.execute(stmt)).scalars()
            return [ReminderMapper.to_dto_or_fail(model) for model in models] if models else []
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while finding user reminders: {str(e)}") from e

    async def find_user_reminder_by_id(
        self,
        user_id: ReminderUserID,
        reminder_id: ReminderID,
        only_active: bool | None = True,
    ) -> ReminderDTO | None:
        """Find a specific reminder by ID for a user"""
        try:
            stmt = select(ReminderModel).where(
                ReminderModel.id == reminder_id.value,
                ReminderModel.user_id == user_id.value,
            )

            if only_active:
                now = datetime.utcnow()
                stmt = stmt.where(
                    (ReminderModel.start_date <= now)
                    & ((ReminderModel.end_date.is_(None)) | (ReminderModel.end_date > now))
                )

            model = (await self._db.execute(stmt)).scalar_one_or_none()
            return ReminderMapper.to_dto(model)
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while finding reminder by ID: {str(e)}") from e

    async def update_reminder(self, reminder: ReminderDTO) -> ReminderDTO:
        """Update an existing reminder"""
        if reminder.reminder_id is None:
            raise ValueError("Reminder ID not given")

        try:
            stmt = (
                update(ReminderModel)
                .where(ReminderModel.id == reminder.reminder_id.value)
                .values(
                    entry_type=reminder.entry_type.value,
                    currency=reminder.currency.value,
                    frequency=reminder.frequency.value,
                    start_date=reminder.start_date.value,
                    end_date=reminder.end_date.value if reminder.end_date else None,
                    description=reminder.description.value,
                )
            )

            result = cast(CursorResult[Any], await self._db.execute(stmt))
            if result.rowcount == 0:
                raise ValueError(f"Reminder with ID {reminder.reminder_id.value} not found")

            await self._db.commit()

            return reminder
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise ValueError(f"Database error while updating reminder: {str(e)}") from e

    async def delete_reminder(
        self,
        reminder_id: ReminderID,
        user_id: ReminderUserID,
    ) -> bool:
        """Delete a reminder"""
        try:
            stmt = (
                update(ReminderModel)
                .where(
                    ReminderModel.id == reminder_id.value,
                    ReminderModel.user_id == user_id.value,
                )
                .values(deleted_at=datetime.utcnow())
            )

            result = cast(CursorResult[Any], await self._db.execute(stmt))
            await self._db.commit()

            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise ValueError(f"Database error while deleting reminder: {str(e)}") from e

    async def find_active_reminders_due_before(
        self,
        before: datetime,
    ) -> list[ReminderDTO]:
        """Find all active reminders with start_date before the given datetime"""
        try:
            now = datetime.utcnow()
            stmt = select(ReminderModel).where(
                (ReminderModel.start_date <= before)
                & (ReminderModel.start_date >= now)
                & ((ReminderModel.end_date.is_(None)) | (ReminderModel.end_date > now))
            )

            models = (await self._db.execute(stmt)).scalars()
            return [ReminderMapper.to_dto_or_fail(model) for model in models] if models else []
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while finding active reminders: {str(e)}") from e
