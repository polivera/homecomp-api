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
from app.shared.domain.contracts import LoggerContract

# ─────────────────────────────────────────────────────────────────
# COMMAND HANDLERS (Write operations)
# ─────────────────────────────────────────────────────────────────


def get_create_reminder_handler(
    db: AsyncSession,
    logger: LoggerContract,
) -> CreateReminderHandlerContract:
    """CreateReminderHandler dependency injection"""
    from app.context.reminder.application.handlers import CreateReminderHandler

    reminder_repo = _get_reminder_repository(db)
    reminder_occurrence_repo = _get_reminder_occurrence_repository(db)

    generate_occurrences_service = _get_generate_occurrences_service(reminder_occurrence_repo)
    service = _get_create_reminder_service(reminder_repo, generate_occurrences_service)

    return CreateReminderHandler(service)


def get_update_reminder_handler(
    db: AsyncSession,
    logger: LoggerContract,
) -> UpdateReminderHandlerContract:
    """UpdateReminderHandler dependency injection"""
    from app.context.reminder.application.handlers import UpdateReminderHandler

    reminder_repo = _get_reminder_repository(db)
    reminder_occurrence_repo = _get_reminder_occurrence_repository(db)
    gen_occurrence_service = _get_generate_occurrences_service(reminder_occurrence_repo)

    service = _get_update_reminder_service(reminder_repo, reminder_occurrence_repo, gen_occurrence_service)

    return UpdateReminderHandler(service)


def get_delete_reminder_handler(
    db: AsyncSession,
    logger: LoggerContract,
) -> DeleteReminderHandlerContract:
    """DeleteReminderHandler dependency injection"""
    from app.context.reminder.application.handlers import DeleteReminderHandler

    reminder_repo = _get_reminder_repository(db)
    reminder_occurrence_repo = _get_reminder_occurrence_repository(db)
    service = _get_delete_reminder_service(reminder_repo, reminder_occurrence_repo)

    return DeleteReminderHandler(service)


# ─────────────────────────────────────────────────────────────────
# QUERY HANDLERS (Read operations)
# ─────────────────────────────────────────────────────────────────


def get_find_reminder_handler(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindReminderHandlerContract:
    """FindReminderHandler dependency injection"""
    from app.context.reminder.application.handlers import FindReminderHandler

    repository = _get_reminder_repository(db)

    return FindReminderHandler(repository)


def get_list_reminders_handler(
    db: AsyncSession,
    logger: LoggerContract,
) -> ListRemindersHandlerContract:
    """ListRemindersHandler dependency injection"""
    from app.context.reminder.application.handlers import ListRemindersHandler

    repository = _get_reminder_repository(db)

    return ListRemindersHandler(repository)


def get_list_occurrences_handler(
    db: AsyncSession,
    logger: LoggerContract,
) -> ListOccurrencesHandlerContract:
    """ListOccurrencesHandler dependency injection"""
    from app.context.reminder.application.handlers import ListOccurrencesHandler

    repository = _get_reminder_occurrence_repository(db)

    return ListOccurrencesHandler(repository)


# ─────────────────────────────────────────────────────────────────
# Private helper functions
# ─────────────────────────────────────────────────────────────────


def _get_reminder_repository(
    db: AsyncSession,
) -> ReminderRepositoryContract:
    """ReminderRepository dependency injection"""
    from app.context.reminder.infrastructure.repositories.reminder_repository import ReminderRepository

    return ReminderRepository(db)


def _get_reminder_occurrence_repository(
    db: AsyncSession,
) -> ReminderOccurrenceRepositoryContract:
    """ReminderOccurrenceRepository dependency injection"""
    from app.context.reminder.infrastructure.repositories.reminder_occurrence_repository import (
        ReminderOccurrenceRepository,
    )

    return ReminderOccurrenceRepository(db)


def _get_generate_occurrences_service(
    occurrence_repo: ReminderOccurrenceRepositoryContract,
) -> GenerateOccurrencesServiceContract:
    """GenerateOccurrencesService dependency injection"""
    from app.context.reminder.domain.services import GenerateOccurrencesService

    return GenerateOccurrencesService(occurrence_repo)


def _get_create_reminder_service(
    reminder_repo: ReminderRepositoryContract,
    generate_occurrences_service: GenerateOccurrencesServiceContract,
) -> CreateReminderServiceContract:
    """CreateReminderService dependency injection"""
    from app.context.reminder.domain.services import CreateReminderService

    return CreateReminderService(reminder_repo, generate_occurrences_service)


def _get_update_reminder_service(
    reminder_repo: ReminderRepositoryContract,
    occurrence_repo: ReminderOccurrenceRepositoryContract,
    generate_occurrences_service: GenerateOccurrencesServiceContract,
) -> UpdateReminderServiceContract:
    """UpdateReminderService dependency injection"""
    from app.context.reminder.domain.services import UpdateReminderService

    return UpdateReminderService(reminder_repo, occurrence_repo, generate_occurrences_service)


def _get_delete_reminder_service(
    reminder_repo: ReminderRepositoryContract,
    occurrence_repo: ReminderOccurrenceRepositoryContract,
) -> DeleteReminderServiceContract:
    """DeleteReminderService dependency injection"""
    from app.context.reminder.domain.services import DeleteReminderService

    return DeleteReminderService(reminder_repo, occurrence_repo)
