from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.reminder.domain.contracts.infrastructure import (
    ReminderOccurrenceRepositoryContract,
    ReminderRepositoryContract,
)
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.database import get_db
from app.shared.infrastructure.dependencies import get_logger


def get_reminder_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReminderRepositoryContract:
    """ReminderRepository dependency injection"""
    from app.context.reminder.infrastructure.repositories.reminder_repository import (
        ReminderRepository,
    )

    return ReminderRepository(db)


def get_reminder_occurrence_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReminderOccurrenceRepositoryContract:
    """ReminderOccurrenceRepository dependency injection"""
    from app.context.reminder.infrastructure.repositories.reminder_occurrence_repository import (
        ReminderOccurrenceRepository,
    )

    return ReminderOccurrenceRepository(db)
