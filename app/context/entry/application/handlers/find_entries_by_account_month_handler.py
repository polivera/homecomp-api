from app.context.entry.application.contracts import FindEntriesByAccountMonthHandlerContract
from app.context.entry.application.dto import (
    EntryResponseDTO,
    FindMultipleEntriesErrorCode,
    FindMultipleEntriesResult,
)
from app.context.entry.application.queries import FindEntriesByAccountMonthQuery
from app.context.entry.domain.contracts.infrastructure import EntryRepositoryContract
from app.context.entry.domain.value_objects import EntryAccountID, EntryDate, EntryMonth, EntryUserID, EntryYear
from app.shared.domain.contracts import LoggerContract


class FindEntriesByAccountMonthHandler(FindEntriesByAccountMonthHandlerContract):
    """Handler for find entries by account and month query"""

    def __init__(
        self,
        repository: EntryRepositoryContract,
        logger: LoggerContract,
    ):
        self._repository = repository
        self._logger = logger

    async def handle(self, query: FindEntriesByAccountMonthQuery) -> FindMultipleEntriesResult:
        """Execute the find entries by account and month query"""
        self._logger.debug(
            "Finding entries by account and month",
            user_id=query.user_id,
            account_id=query.account_id,
            month=query.month,
            year=query.year,
            last_row_date=query.last_entry_date.isoformat() if query.last_entry_date else None,
        )

        try:
            entries = await self._repository.find_entries_by_account_and_month(
                user_id=EntryUserID(query.user_id),
                account_id=EntryAccountID(query.account_id),
                month=EntryMonth(query.month),
                year=EntryYear(query.year),
                last_entry_date=EntryDate(query.last_entry_date) if query.last_entry_date else None,
            )

            # Return empty list if no entries found (not an error)
            if not entries:
                self._logger.debug("No entries found", user_id=query.user_id)
                return FindMultipleEntriesResult(entries=[])

            entry_dtos = [EntryResponseDTO.from_domain_dto(entry) for entry in entries]
            return FindMultipleEntriesResult(entries=entry_dtos)

        except Exception as e:
            self._logger.error("Unexpected error while finding entries", error=str(e))
            return FindMultipleEntriesResult(
                error_code=FindMultipleEntriesErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error while finding entries",
            )
