from sqlalchemy.ext.asyncio import AsyncSession

from app.context.entry.application.contracts import (
    CreateEntryHandlerContract,
    DeleteEntryHandlerContract,
    FindEntriesByAccountMonthHandlerContract,
    FindEntryByIdHandlerContract,
    UpdateEntryHandlerContract,
)
from app.context.entry.domain.contracts import (
    CreateEntryServiceContract,
    EntryRepositoryContract,
    UpdateEntryServiceContract,
)
from app.shared.domain.contracts import LoggerContract

# ─────────────────────────────────────────────────────────────────
# COMMAND HANDLERS (Write operations)
# ─────────────────────────────────────────────────────────────────


def create_entry_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> CreateEntryHandlerContract:
    """Factory for CreateEntryHandler with all dependencies"""
    from app.context.entry.application.handlers import CreateEntryHandler

    service = _get_create_entry_service(_get_entry_repository(db), logger)
    return CreateEntryHandler(service, logger)


def update_entry_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> UpdateEntryHandlerContract:
    """Factory for UpdateEntryHandler with all dependencies"""
    from app.context.entry.application.handlers import UpdateEntryHandler

    service = _get_update_entry_service(_get_entry_repository(db), logger)
    return UpdateEntryHandler(service, logger)


def delete_entry_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> DeleteEntryHandlerContract:
    """Factory for DeleteEntryHandler with all dependencies"""
    from app.context.entry.application.handlers import DeleteEntryHandler

    repository = _get_entry_repository(db)
    return DeleteEntryHandler(repository, logger)


# ─────────────────────────────────────────────────────────────────
# QUERY HANDLERS (Read operations)
# ─────────────────────────────────────────────────────────────────


def find_entry_by_id_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindEntryByIdHandlerContract:
    """Factory for FindEntryByIdHandler with all dependencies"""
    from app.context.entry.application.handlers import FindEntryByIdHandler

    repository = _get_entry_repository(db)
    return FindEntryByIdHandler(repository, logger)


def find_entries_by_account_month_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindEntriesByAccountMonthHandlerContract:
    """Factory for FindEntriesByAccountMonthHandler with all dependencies"""
    from app.context.entry.application.handlers import FindEntriesByAccountMonthHandler

    repository = _get_entry_repository(db)
    return FindEntriesByAccountMonthHandler(repository, logger)


# ─────────────────────────────────────────────────────────────────
# Private helper functions
# ─────────────────────────────────────────────────────────────────


def _get_entry_repository(db: AsyncSession) -> EntryRepositoryContract:
    """Get entry repository instance"""
    from app.context.entry.infrastructure.repositories import EntryRepository

    return EntryRepository(db)


def _get_create_entry_service(
    repository: EntryRepositoryContract,
    logger: LoggerContract,
) -> CreateEntryServiceContract:
    """Get create entry service instance"""
    from app.context.entry.domain.services import CreateEntryService

    return CreateEntryService(repository, logger)


def _get_update_entry_service(
    repository: EntryRepositoryContract,
    logger: LoggerContract,
) -> UpdateEntryServiceContract:
    """Get update entry service instance"""
    from app.context.entry.domain.services import UpdateEntryService

    return UpdateEntryService(repository, logger)
