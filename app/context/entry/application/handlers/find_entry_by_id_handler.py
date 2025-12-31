from app.context.entry.application.contracts import FindEntryByIdHandlerContract
from app.context.entry.application.dto import (
    EntryResponseDTO,
    FindSingleEntryErrorCode,
    FindSingleEntryResult,
)
from app.context.entry.application.queries import FindEntryByIdQuery
from app.context.entry.domain.contracts.infrastructure import EntryRepositoryContract
from app.context.entry.domain.value_objects import EntryID, EntryUserID
from app.shared.domain.contracts import LoggerContract


class FindEntryByIdHandler(FindEntryByIdHandlerContract):
    """Handler for find entry by ID query"""

    def __init__(
        self,
        repository: EntryRepositoryContract,
        logger: LoggerContract,
    ):
        self._repository = repository
        self._logger = logger

    async def handle(self, query: FindEntryByIdQuery) -> FindSingleEntryResult:
        """Execute the find entry by ID query"""
        try:
            entry = await self._repository.find_entry_by_id(
                entry_id=EntryID(query.entry_id),
                user_id=EntryUserID(query.user_id),
            )

            if not entry:
                return FindSingleEntryResult(
                    error_code=FindSingleEntryErrorCode.NOT_FOUND,
                    error_message="Entry not found",
                )

            return FindSingleEntryResult(entry=EntryResponseDTO.from_domain_dto(entry))

        except Exception as e:
            self._logger.error("Unexpected error while finding entry", error=str(e))
            return FindSingleEntryResult(
                error_code=FindSingleEntryErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error while finding entry",
            )
