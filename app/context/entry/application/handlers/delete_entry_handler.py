from app.context.entry.application.commands import DeleteEntryCommand
from app.context.entry.application.contracts import DeleteEntryHandlerContract
from app.context.entry.application.dto import (
    DeleteEntryErrorCode,
    DeleteEntryResult,
)
from app.context.entry.domain.contracts.infrastructure import EntryRepositoryContract
from app.context.entry.domain.value_objects import EntryID, EntryUserID
from app.shared.domain.contracts import LoggerContract


class DeleteEntryHandler(DeleteEntryHandlerContract):
    """Handler for delete entry command"""

    def __init__(
        self,
        repository: EntryRepositoryContract,
        logger: LoggerContract,
    ):
        self._repository = repository
        self._logger = logger

    async def handle(self, command: DeleteEntryCommand) -> DeleteEntryResult:
        """Execute the delete entry command (hard delete)"""
        try:
            success = await self._repository.delete_entry(
                entry_id=EntryID(command.entry_id),
                user_id=EntryUserID(command.user_id),
            )

            if not success:
                return DeleteEntryResult(
                    error_code=DeleteEntryErrorCode.NOT_FOUND,
                    error_message="Entry not found",
                )

            return DeleteEntryResult(success=True)

        except Exception as e:
            self._logger.error("Unexpected error during entry deletion", error=str(e))
            return DeleteEntryResult(
                error_code=DeleteEntryErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
