from app.context.entry.application.commands import CreateEntryCommand
from app.context.entry.application.contracts import CreateEntryHandlerContract
from app.context.entry.application.dto import (
    CreateEntryErrorCode,
    CreateEntryResult,
)
from app.context.entry.domain.contracts.services import CreateEntryServiceContract
from app.context.entry.domain.exceptions import (
    EntryAccountNotBelongsToUserError,
    EntryCategoryNotBelongsToUserError,
    EntryCategoryNotFoundError,
    EntryMapperError,
)
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryAmount,
    EntryCategoryID,
    EntryDate,
    EntryDescription,
    EntryHouseholdID,
    EntryType,
    EntryUserID,
)
from app.shared.domain.contracts import LoggerContract


class CreateEntryHandler(CreateEntryHandlerContract):
    """Handler for create entry command"""

    def __init__(
        self,
        service: CreateEntryServiceContract,
        logger: LoggerContract,
    ):
        self._service = service
        self._logger = logger

    async def handle(self, command: CreateEntryCommand) -> CreateEntryResult:
        """Execute the create entry command"""
        try:
            # Convert command primitives to value objects
            entry_dto = await self._service.create_entry(
                user_id=EntryUserID(command.user_id),
                account_id=EntryAccountID(command.account_id),
                category_id=EntryCategoryID(command.category_id),
                entry_type=EntryType(command.entry_type),
                entry_date=EntryDate(command.entry_date),
                amount=EntryAmount.from_float(command.amount),
                description=EntryDescription(command.description),
                household_id=(EntryHouseholdID(command.household_id) if command.household_id is not None else None),
            )

            # Validate operation succeeded
            if entry_dto.entry_id is None:
                self._logger.error("Entry creation returned None entry_id")
                return CreateEntryResult(
                    error_code=CreateEntryErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating entry",
                )

            # Return success result with primitives
            return CreateEntryResult(
                entry_id=entry_dto.entry_id.value,
                account_id=entry_dto.account_id.value,
                category_id=entry_dto.category_id.value,
                entry_type=entry_dto.entry_type.value,
                entry_date=entry_dto.entry_date.value.isoformat(),
                amount=float(entry_dto.amount.value),
                description=entry_dto.description.value,
            )

        except EntryAccountNotBelongsToUserError:
            return CreateEntryResult(
                error_code=CreateEntryErrorCode.ACCOUNT_NOT_BELONGS_TO_USER,
                error_message="Account does not belong to user",
            )
        except EntryCategoryNotFoundError:
            return CreateEntryResult(
                error_code=CreateEntryErrorCode.CATEGORY_NOT_FOUND,
                error_message="Category not found",
            )
        except EntryCategoryNotBelongsToUserError:
            return CreateEntryResult(
                error_code=CreateEntryErrorCode.CATEGORY_NOT_BELONGS_TO_USER,
                error_message="Category does not belong to user",
            )
        except EntryMapperError:
            return CreateEntryResult(
                error_code=CreateEntryErrorCode.MAPPER_ERROR,
                error_message="Error mapping entry data",
            )
        except Exception as e:
            self._logger.error("Unexpected error during entry creation", error=str(e))
            return CreateEntryResult(
                error_code=CreateEntryErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
