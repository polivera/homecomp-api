from app.context.entry.domain.contracts.infrastructure import EntryRepositoryContract
from app.context.entry.domain.contracts.services import CreateEntryServiceContract
from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import (
    EntryAccountNotBelongsToUserError,
    EntryCategoryNotFoundError,
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


class CreateEntryService(CreateEntryServiceContract):
    """Service for creating entries with validation"""

    def __init__(
        self,
        repository: EntryRepositoryContract,
        logger: LoggerContract,
    ):
        self._repository = repository
        self._logger = logger

    async def create_entry(
        self,
        user_id: EntryUserID,
        account_id: EntryAccountID,
        category_id: EntryCategoryID,
        entry_type: EntryType,
        entry_date: EntryDate,
        amount: EntryAmount,
        description: EntryDescription,
        household_id: EntryHouseholdID | None = None,
    ) -> EntryDTO:
        """Create a new entry with validation"""
        self._logger.debug(
            "Creating entry",
            user_id=user_id.value,
            account_id=account_id.value,
            category_id=category_id.value,
            entry_type=entry_type.value,
        )

        # Verify account belongs to user
        account_valid = await self._repository.verify_account_belongs_to_user(
            account_id=account_id,
            user_id=user_id,
        )
        if not account_valid:
            self._logger.warning(
                "Account does not belong to user",
                user_id=user_id.value,
                account_id=account_id.value,
            )
            raise EntryAccountNotBelongsToUserError(
                f"Account {account_id.value} does not belong to user {user_id.value}"
            )

        # Verify category belongs to user
        category_valid = await self._repository.verify_category_belongs_to_user(
            category_id=category_id,
            user_id=user_id,
        )
        if not category_valid:
            self._logger.warning(
                "Category not found or does not belong to user",
                user_id=user_id.value,
                category_id=category_id.value,
            )
            raise EntryCategoryNotFoundError(f"Category {category_id.value} not found or does not belong to user")

        # Create entry DTO
        entry_dto = EntryDTO(
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
            household_id=household_id,
        )

        # Save entry
        created_entry = await self._repository.save_entry(entry_dto)

        if created_entry.entry_id:
            self._logger.debug(
                "Entry created successfully",
                user_id=user_id.value,
                entry_id=created_entry.entry_id.value,
            )

        return created_entry
