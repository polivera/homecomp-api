from datetime import datetime
from typing import Any, cast

from sqlalchemy import select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.reminder.domain.contracts.infrastructure import (
    ReminderOccurrenceRepositoryContract,
)
from app.context.reminder.domain.dto import ReminderOccurrenceDTO
from app.context.reminder.domain.value_objects import (
    ReminderID,
    ReminderOccurrenceID,
    ReminderOccurrenceStatus,
)
from app.context.reminder.infrastructure.mappers import ReminderOccurrenceMapper
from app.context.reminder.infrastructure.models import ReminderModel, ReminderOccurrenceModel


class ReminderOccurrenceRepository(ReminderOccurrenceRepositoryContract):
    """Repository implementation for reminder occurrence operations"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save_occurrence(self, occurrence: ReminderOccurrenceDTO) -> ReminderOccurrenceDTO:
        """Create a new occurrence"""
        try:
            model = ReminderOccurrenceMapper.to_model(occurrence)
            self._db.add(model)
            await self._db.commit()
            await self._db.refresh(model)
            return ReminderOccurrenceMapper.to_dto_or_fail(model)
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise ValueError(f"Database error while saving occurrence: {str(e)}") from e

    async def save_occurrences(self, occurrences: list[ReminderOccurrenceDTO]) -> list[ReminderOccurrenceDTO]:
        """Create multiple occurrences in a single transaction"""
        try:
            models = [ReminderOccurrenceMapper.to_model(o) for o in occurrences]
            for model in models:
                self._db.add(model)
            await self._db.commit()

            saved_occurrences = []
            for model in models:
                await self._db.refresh(model)
                saved_occurrences.append(ReminderOccurrenceMapper.to_dto_or_fail(model))

            return saved_occurrences
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise ValueError(f"Database error while saving occurrences: {str(e)}") from e

    async def find_occurrence(
        self,
        occurrence_id: ReminderOccurrenceID | None = None,
        reminder_id: ReminderID | None = None,
    ) -> ReminderOccurrenceDTO | None:
        """Find an occurrence by ID or reminder_id"""
        try:
            stmt = select(ReminderOccurrenceModel)

            if occurrence_id is not None:
                stmt = stmt.where(ReminderOccurrenceModel.id == occurrence_id.value)
            elif reminder_id is not None:
                stmt = stmt.where(ReminderOccurrenceModel.reminder_id == reminder_id.value)
            else:
                raise ValueError("Must provide either occurrence_id or reminder_id")

            result = await self._db.execute(stmt)
            model = result.scalar_one_or_none()

            return ReminderOccurrenceMapper.to_dto(model) if model else None
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while finding occurrence: {str(e)}") from e

    async def find_occurrences_by_reminder(
        self,
        reminder_id: ReminderID,
    ) -> list[ReminderOccurrenceDTO]:
        """Find all occurrences for a reminder"""
        try:
            stmt = (
                select(ReminderOccurrenceModel)
                .where(ReminderOccurrenceModel.reminder_id == reminder_id.value)
                .order_by(ReminderOccurrenceModel.scheduled_date)
            )

            models = (await self._db.execute(stmt)).scalars()
            return [ReminderOccurrenceMapper.to_dto_or_fail(model) for model in models] if models else []
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while finding occurrences: {str(e)}") from e

    async def find_pending_occurrences_by_date(
        self,
        before: datetime,
    ) -> list[ReminderOccurrenceDTO]:
        """Find all pending occurrences scheduled before the given datetime"""
        try:
            stmt = (
                select(ReminderOccurrenceModel)
                .where(
                    ReminderOccurrenceModel.scheduled_date <= before,
                    ReminderOccurrenceModel.status == "pending",
                )
                .order_by(ReminderOccurrenceModel.scheduled_date)
            )

            models = (await self._db.execute(stmt)).scalars()
            return [ReminderOccurrenceMapper.to_dto_or_fail(model) for model in models] if models else []
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while finding pending occurrences: {str(e)}") from e

    async def find_pending_occurrences_by_user(
        self,
        user_id: int,
        before: datetime | None = None,
    ) -> list[ReminderOccurrenceDTO]:
        """Find all pending occurrences for a user's reminders"""
        try:
            from sqlalchemy import join

            stmt = (
                select(ReminderOccurrenceModel)
                .select_from(
                    join(
                        ReminderOccurrenceModel,
                        ReminderModel,
                        ReminderModel.id == ReminderOccurrenceModel.reminder_id,
                    )
                )
                .where(
                    ReminderModel.user_id == user_id,
                    ReminderOccurrenceModel.status == "pending",
                )
            )

            if before is not None:
                stmt = stmt.where(ReminderOccurrenceModel.scheduled_date <= before)

            stmt = stmt.order_by(ReminderOccurrenceModel.scheduled_date)

            models = (await self._db.execute(stmt)).scalars()
            return [ReminderOccurrenceMapper.to_dto_or_fail(model) for model in models] if models else []
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while finding user pending occurrences: {str(e)}") from e

    async def update_occurrence_status(
        self,
        occurrence_id: ReminderOccurrenceID,
        status: ReminderOccurrenceStatus,
        entry_id: int | None = None,
    ) -> bool:
        """Update occurrence status (e.g., mark as completed with entry_id)"""
        try:
            stmt = (
                update(ReminderOccurrenceModel)
                .where(ReminderOccurrenceModel.id == occurrence_id.value)
                .values(
                    status=status.value,
                    entry_id=entry_id,
                )
            )

            result = cast(CursorResult[Any], await self._db.execute(stmt))
            await self._db.commit()

            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise ValueError(f"Database error while updating occurrence status: {str(e)}") from e

    async def delete_occurrences_by_reminder(
        self,
        reminder_id: ReminderID,
    ) -> int:
        """Delete all occurrences for a reminder (when reminder is deleted)"""
        try:
            stmt = (
                update(ReminderOccurrenceModel)
                .where(ReminderOccurrenceModel.reminder_id == reminder_id.value)
                .values(deleted_at=datetime.utcnow())
            )

            result = cast(CursorResult[Any], await self._db.execute(stmt))
            await self._db.commit()

            return result.rowcount
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise ValueError(f"Database error while deleting occurrences: {str(e)}") from e
