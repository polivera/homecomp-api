from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.reminder.application.contracts import (
    CreateReminderHandlerContract,
    DeleteReminderHandlerContract,
    FindReminderHandlerContract,
    ListOccurrencesHandlerContract,
    ListRemindersHandlerContract,
    UpdateReminderHandlerContract,
)
from app.context.reminder.domain.contracts.infrastructure import (
    ReminderOccurrenceRepositoryContract,
    ReminderRepositoryContract,
)
from app.context.reminder.domain.contracts.services import (
    CreateReminderServiceContract,
    DeleteReminderServiceContract,
    GenerateOccurrencesServiceContract,
    UpdateReminderServiceContract,
)
from app.shared.infrastructure.database import get_db

# ============================================================================
# Repository Dependencies
# ============================================================================


def get_reminder_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReminderRepositoryContract:
    """ReminderRepository dependency injection"""
    from app.context.reminder.infrastructure.repositories.reminder_repository import ReminderRepository

    return ReminderRepository(db)


def get_reminder_occurrence_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReminderOccurrenceRepositoryContract:
    """ReminderOccurrenceRepository dependency injection"""
    from app.context.reminder.infrastructure.repositories.reminder_occurrence_repository import (
        ReminderOccurrenceRepository,
    )

    return ReminderOccurrenceRepository(db)


# ============================================================================
# Service Dependencies
# ============================================================================


def get_generate_occurrences_service(
    occurrence_repo: Annotated[ReminderOccurrenceRepositoryContract, Depends(get_reminder_occurrence_repository)],
) -> GenerateOccurrencesServiceContract:
    """GenerateOccurrencesService dependency injection"""
    from app.context.reminder.domain.services import GenerateOccurrencesService

    return GenerateOccurrencesService(occurrence_repo)


def get_create_reminder_service(
    reminder_repo: Annotated[ReminderRepositoryContract, Depends(get_reminder_repository)],
    generate_occurrences_service: Annotated[
        GenerateOccurrencesServiceContract, Depends(get_generate_occurrences_service)
    ],
) -> CreateReminderServiceContract:
    """CreateReminderService dependency injection"""
    from app.context.reminder.domain.services import CreateReminderService

    return CreateReminderService(reminder_repo, generate_occurrences_service)


def get_update_reminder_service(
    reminder_repo: Annotated[ReminderRepositoryContract, Depends(get_reminder_repository)],
    occurrence_repo: Annotated[ReminderOccurrenceRepositoryContract, Depends(get_reminder_occurrence_repository)],
    generate_occurrences_service: Annotated[
        GenerateOccurrencesServiceContract, Depends(get_generate_occurrences_service)
    ],
) -> UpdateReminderServiceContract:
    """UpdateReminderService dependency injection"""
    from app.context.reminder.domain.services import UpdateReminderService

    return UpdateReminderService(reminder_repo, occurrence_repo, generate_occurrences_service)


def get_delete_reminder_service(
    reminder_repo: Annotated[ReminderRepositoryContract, Depends(get_reminder_repository)],
    occurrence_repo: Annotated[ReminderOccurrenceRepositoryContract, Depends(get_reminder_occurrence_repository)],
) -> DeleteReminderServiceContract:
    """DeleteReminderService dependency injection"""
    from app.context.reminder.domain.services import DeleteReminderService

    return DeleteReminderService(reminder_repo, occurrence_repo)


# ============================================================================
# Handler Dependencies
# ============================================================================


def get_create_reminder_handler(
    service: Annotated[CreateReminderServiceContract, Depends(get_create_reminder_service)],
) -> CreateReminderHandlerContract:
    """CreateReminderHandler dependency injection"""
    from app.context.reminder.application.handlers import CreateReminderHandler

    return CreateReminderHandler(service)


def get_update_reminder_handler(
    service: Annotated[UpdateReminderServiceContract, Depends(get_update_reminder_service)],
) -> UpdateReminderHandlerContract:
    """UpdateReminderHandler dependency injection"""
    from app.context.reminder.application.handlers import UpdateReminderHandler

    return UpdateReminderHandler(service)


def get_delete_reminder_handler(
    service: Annotated[DeleteReminderServiceContract, Depends(get_delete_reminder_service)],
) -> DeleteReminderHandlerContract:
    """DeleteReminderHandler dependency injection"""
    from app.context.reminder.application.handlers import DeleteReminderHandler

    return DeleteReminderHandler(service)


def get_find_reminder_handler(
    repository: Annotated[ReminderRepositoryContract, Depends(get_reminder_repository)],
) -> FindReminderHandlerContract:
    """FindReminderHandler dependency injection"""
    from app.context.reminder.application.handlers import FindReminderHandler

    return FindReminderHandler(repository)


def get_list_reminders_handler(
    repository: Annotated[ReminderRepositoryContract, Depends(get_reminder_repository)],
) -> ListRemindersHandlerContract:
    """ListRemindersHandler dependency injection"""
    from app.context.reminder.application.handlers import ListRemindersHandler

    return ListRemindersHandler(repository)


def get_list_occurrences_handler(
    repository: Annotated[ReminderOccurrenceRepositoryContract, Depends(get_reminder_occurrence_repository)],
) -> ListOccurrencesHandlerContract:
    """ListOccurrencesHandler dependency injection"""
    from app.context.reminder.application.handlers import ListOccurrencesHandler

    return ListOccurrencesHandler(repository)
