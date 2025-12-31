from app.context.entry.domain.contracts.infrastructure import EntryRepositoryContract
from app.context.entry.domain.contracts.services import UpdateEntryServiceContract
from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import (
    EntryAccountNotBelongsToUserError,
    EntryCategoryNotFoundError,
    EntryNotFoundError,
)
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryAmount,
    EntryCategoryID,
    EntryDate,
    EntryDescription,
    EntryHouseholdID,
    EntryID,
    EntryType,
    EntryUserID,
)
from app.shared.domain.contracts import LoggerContract


class UpdateEntryService(UpdateEntryServiceContract):
    """Service for updating entries with validation"""

    def __init__(
        self,
        repository: EntryRepositoryContract,
        logger: LoggerContract,
    ):
        self._repository = repository
        self._logger = logger

    async def update_entry(
        self,
        entry_id: EntryID,
        user_id: EntryUserID,
        account_id: EntryAccountID,
        category_id: EntryCategoryID,
        entry_type: EntryType,
        entry_date: EntryDate,
        amount: EntryAmount,
        description: EntryDescription,
        household_id: EntryHouseholdID | None = None,
    ) -> EntryDTO:
        """Update an existing entry with validation"""
        self._logger.debug(
            "Updating entry",
            entry_id=entry_id.value,
            user_id=user_id.value,
        )

        existing_entry = await self._repository.find_entry_by_id(
            entry_id=entry_id,
            user_id=user_id,
        )
        if not existing_entry:
            self._logger.warning(
                "Entry not found or does not belong to user",
                entry_id=entry_id.value,
                user_id=user_id.value,
            )
            raise EntryNotFoundError(f"Entry {entry_id.value} not found or does not belong to user")

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

        # Create updated entry DTO (preserve household_id from existing)
        updated_dto = EntryDTO(
            entry_id=entry_id,
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
            household_id=household_id,
        )

        # Update entry
        updated_entry = await self._repository.update_entry(updated_dto)

        self._logger.debug(
            "Entry updated successfully",
            entry_id=entry_id.value,
            user_id=user_id.value,
        )

        return updated_entry
