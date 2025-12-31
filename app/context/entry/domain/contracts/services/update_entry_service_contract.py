from abc import ABC, abstractmethod

from app.context.entry.domain.dto import EntryDTO
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


class UpdateEntryServiceContract(ABC):
    """Contract for update entry service"""

    @abstractmethod
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
        """
        Update an existing entry with validation

        Args:
            entry_id: Entry identifier
            user_id: User identifier
            account_id: Account identifier
            category_id: Category identifier
            entry_type: Type of entry (income/expense)
            entry_date: Date of entry
            amount: Amount (non-negative)
            description: Entry description

        Returns:
            Updated entry DTO

        Raises:
            EntryNotFoundError: If entry doesn't exist
            EntryNotBelongsToUserError: If entry doesn't belong to user
            EntryAccountNotBelongsToUserError: If account doesn't belong to user
            EntryCategoryNotFoundError: If category doesn't exist
            EntryCategoryNotBelongsToUserError: If category doesn't belong to user
            EntryMapperError: If mapping fails
        """
        pass
