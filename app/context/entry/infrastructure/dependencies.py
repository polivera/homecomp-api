from typing import Annotated

from fastapi import Depends
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
from app.shared.infrastructure.database import get_db
from app.shared.infrastructure.dependencies import get_logger


# Repository
def get_entry_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> EntryRepositoryContract:
    """Get entry repository"""
    from app.context.entry.infrastructure.repositories import EntryRepository

    return EntryRepository(db)


# Services
def get_create_entry_service(
    repository: Annotated[EntryRepositoryContract, Depends(get_entry_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> CreateEntryServiceContract:
    """Get create entry service"""
    from app.context.entry.domain.services import CreateEntryService

    return CreateEntryService(repository, logger)


def get_update_entry_service(
    repository: Annotated[EntryRepositoryContract, Depends(get_entry_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> UpdateEntryServiceContract:
    """Get update entry service"""
    from app.context.entry.domain.services import UpdateEntryService

    return UpdateEntryService(repository, logger)


# Handlers
def get_create_entry_handler(
    service: Annotated[CreateEntryServiceContract, Depends(get_create_entry_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> CreateEntryHandlerContract:
    """Get create entry handler"""
    from app.context.entry.application.handlers import CreateEntryHandler

    return CreateEntryHandler(service, logger)


def get_find_entry_by_id_handler(
    repository: Annotated[EntryRepositoryContract, Depends(get_entry_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> FindEntryByIdHandlerContract:
    """Get find entry by ID handler"""
    from app.context.entry.application.handlers import FindEntryByIdHandler

    return FindEntryByIdHandler(repository, logger)


def get_find_entries_by_account_month_handler(
    repository: Annotated[EntryRepositoryContract, Depends(get_entry_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> FindEntriesByAccountMonthHandlerContract:
    """Get find entries by account and month handler"""
    from app.context.entry.application.handlers import FindEntriesByAccountMonthHandler

    return FindEntriesByAccountMonthHandler(repository, logger)


def get_update_entry_handler(
    service: Annotated[UpdateEntryServiceContract, Depends(get_update_entry_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> UpdateEntryHandlerContract:
    """Get update entry handler"""
    from app.context.entry.application.handlers import UpdateEntryHandler

    return UpdateEntryHandler(service, logger)


def get_delete_entry_handler(
    repository: Annotated[EntryRepositoryContract, Depends(get_entry_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> DeleteEntryHandlerContract:
    """Get delete entry handler"""
    from app.context.entry.application.handlers import DeleteEntryHandler

    return DeleteEntryHandler(repository, logger)
