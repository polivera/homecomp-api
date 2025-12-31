from app.context.entry.application.commands import UpdateEntryCommand
from app.context.entry.application.contracts import UpdateEntryHandlerContract
from app.context.entry.application.dto import (
    EntryResponseDTO,
    UpdateEntryErrorCode,
    UpdateEntryResult,
)
from app.context.entry.domain.contracts.services import UpdateEntryServiceContract
from app.context.entry.domain.exceptions import (
    EntryAccountNotBelongsToUserError,
    EntryCategoryNotFoundError,
    EntryMapperError,
    EntryNotFoundError,
)
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryAmount,
    EntryCategoryID,
    EntryDate,
    EntryDescription,
    EntryID,
    EntryType,
    EntryUserID,
)
from app.shared.domain.contracts import LoggerContract


class UpdateEntryHandler(UpdateEntryHandlerContract):
    """Handler for update entry command"""

    def __init__(
        self,
        service: UpdateEntryServiceContract,
        logger: LoggerContract,
    ):
        self._service = service
        self._logger = logger

    async def handle(self, command: UpdateEntryCommand) -> UpdateEntryResult:
        """Execute the update entry command"""
        try:
            # Convert command primitives to value objects
            updated_dto = await self._service.update_entry(
                entry_id=EntryID(command.entry_id),
                user_id=EntryUserID(command.user_id),
                account_id=EntryAccountID(command.account_id),
                category_id=EntryCategoryID(command.category_id),
                entry_type=EntryType.from_string(command.entry_type),
                entry_date=EntryDate(command.entry_date),
                amount=EntryAmount.from_float(command.amount),
                description=EntryDescription(command.description),
            )

            # Validate operation succeeded
            if updated_dto.entry_id is None:
                self._logger.error("Entry update returned None entry_id")
                return UpdateEntryResult(
                    error_code=UpdateEntryErrorCode.UNEXPECTED_ERROR,
                    error_message="Error updating entry",
                )

            # Return success result with primitives
            return UpdateEntryResult(
                entry=EntryResponseDTO(
                    entry_id=updated_dto.entry_id.value,
                    user_id=updated_dto.user_id.value,
                    account_id=updated_dto.account_id.value,
                    category_id=updated_dto.category_id.value,
                    entry_type=updated_dto.entry_type.value,
                    entry_date=updated_dto.entry_date.value.isoformat(),
                    amount=float(updated_dto.amount.value),
                    description=updated_dto.description.value,
                    household_id=updated_dto.household_id.value if updated_dto.household_id else None,
                )
            )

        except EntryNotFoundError:
            return UpdateEntryResult(
                error_code=UpdateEntryErrorCode.NOT_FOUND,
                error_message="Entry not found",
            )
        except EntryAccountNotBelongsToUserError:
            return UpdateEntryResult(
                error_code=UpdateEntryErrorCode.ACCOUNT_NOT_BELONGS_TO_USER,
                error_message="Account does not belong to user",
            )
        except EntryCategoryNotFoundError:
            return UpdateEntryResult(
                error_code=UpdateEntryErrorCode.CATEGORY_NOT_FOUND,
                error_message="Category not found",
            )
        except EntryMapperError:
            return UpdateEntryResult(
                error_code=UpdateEntryErrorCode.MAPPER_ERROR,
                error_message="Error mapping entry data",
            )
        except Exception as e:
            self._logger.error("Unexpected error during entry update", error=str(e))
            return UpdateEntryResult(
                error_code=UpdateEntryErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
